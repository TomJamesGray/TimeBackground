import logging
import multiprocessing as mp
from src.mode import default
from src.helpers.helpers import getArgsBy
from src.helpers.getConfig import getConfigPart

class CurveImage(default.DefaultImage):
    def retrieveThemeConfig(self):
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
