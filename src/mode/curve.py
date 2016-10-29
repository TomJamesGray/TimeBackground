import logging
import multiprocessing as mp
import random
from src.mode import default
from src.helpers.helpers import getArgsBy
from src.helpers.getConfig import getConfigPart

class CurveImage(default.DefaultImage):
    def retrieveThemeConfig(self):
        """
        Retrieve mode specific attributes from the config, ie,
        colors, background color and coverage
        """
        colorsTemp = getArgsBy(getConfigPart(self.theme,"colours"),",")
        self.colors = []
        for col in colorsTemp:
            tempList = []
            for val in col.split("-"):
                tempList.append(int(val))
            self.colors.append(tuple(tempList))
        self.bg = '#' + getConfigPart(self.theme,"bg")
        self.coverage = getArgsBy(getConfigPart(self.theme,"coverage"),",")

        self.superSamplingEnable()

    def strandWorker(self,queue,col,coverage):
        #Pick a point on the border of the startBox
        side = random.randint(0,3)
        # top = 0
        # right = 1
        # bottom = 2
        # right = 3
        if side == 0:
            startPoint = (random.randint(0,self.startBox[0]),0)
        elif side == 1:
            startPoint = (self.startBox[0],random.randint(0,self.startBox[1]))
        elif side == 2:
            startPoint = (random.randint(0,self.startBox[0]),self.startBox[1])
        else:
            startPoint = (0,random.randint(0,self.startBox[1]))

        logging.info("Start point: {}".format(startPoint))

        queue.put(True)

    def drawImage(self):
        self.retrieveThemeConfig()
        self.initImg()
        
        queue = mp.Queue()
        procs = []

        #Create new thread for each color
        for i,col in enumerate(self.colors):
            procs.append(mp.Process(target=self.strandWorker,args=(queue,col,
                self.coverage[i])))
            procs[i].start()

        self.allCords = []
        for i in procs:
            self.allCords.append(queue.get())

        logging.info("Co-ordinates: {}".format(self.allCords))
