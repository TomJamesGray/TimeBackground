import random,re
from PIL import Image,ImageDraw
from src.helpers.helpers import getArgsBy
from src.helpers.getConfig import getConfigPart
import multiprocessing as mp
class DefaultImage(object):
    def __init__(self,width,height,theme,superSampling,fileName):
        self.width = width
        self.height = height
        self.theme = theme
        self.superSampling = superSampling
        self.fileName = fileName

        self.offsets = getConfigPart(theme,"offsetBoundingBox")
        self.startBox = []
        self.startBox.append(int(width*(1-int(getArgsBy(self.offsets,',')[0])/100)))
        self.startBox.append(int(height*(1-int(getArgsBy(self.offsets,',')[1])/100)))
        
        print("startBox: {}".format(self.startBox))
    
    def retrieveThemeConfig(self):
        #This differs from the above fuction as these config keys are dependent
        #on the theme, so other themes may use different config keys
        self.branches = int(getConfigPart(self.theme,"branches"))
        self.colors = getArgsBy(getConfigPart(self.theme,"colors"),',')
        self.branchDist = int(getConfigPart(self.theme,"branchDist"))
        print(self.branchDist)
        self.strandNum = int(getConfigPart(self.theme,"strands"))
        self.thickness = int(getConfigPart(self.theme,"thickness"))
        self.maxBranchTurns = int(getConfigPart(self.theme,"maxBranchTurns"))

        #Enable superSampling if wanted
        self.superSamplingEnable()

    def superSamplingEnable(self):
        if self.superSampling:
            self.width *= 2
            self.height *= 2
            self.branchDist *= 2
            self.thickness *= 2
    
    #Exports the image and check if super sampling is enabled, if so
    #It will resize the exported image as needed
    def exportImg(self):
        if self.superSampling:
            print("Exporting with size adjusted")
            self.img = self.img.resize((int(self.width/2),int(self.height/2)),Image.NEAREST)
        self.img.save(self.fileName,"PNG")

    def strandWorker(self,strandNum,branchesForStrand):
        cords = []
        cords.append([self.makeCords()])
        #if self.colsDone*self.branches/len(self.colors) < j:
        #    self.color = '#' + self.colors[self.colsDone]
        #    print("Switching to color {} at branch no {}".format(self.colsDone,j))
        #    self.colsDone += 1

        branchResetAt = 0
        color = '#' + self.colors[strandNum]
        for j in range(0,branchesForStrand):
            direction = random.randint(0,3)
            #0=up, 1 left, 2=down, 3=right
            if direction == 0:
                cords[-1].append((cords[-1][-1][0],cords[-1][-1][1]+self.branchDist))
            elif direction == 1:
                cords[-1].append((cords[-1][-1][0]+self.branchDist,cords[-1][-1][1]))
            elif direction == 2:
                cords[-1].append((cords[-1][-1][0],cords[-1][-1][1]-self.branchDist))
            elif direction == 3:
                cords[-1].append((cords[-1][-1][0]-self.branchDist,cords[-1][-1][1]))
            
            if j-branchResetAt ==  self.maxBranchTurns:
                cords.append(self.makeCords())
                branchResetAt = j
            #Check if coordinates have gone off the image and if so start a new strand and
            #abandon the strand which is off the page
            if (cords[-1][-1][0] > self.width or cords[-1][-1][0] < 0 or
                cords[-1][-1][1] > self.height or cords[-1][-1][1] < 0):
                    cords.append([self.makeCords()])
                    branchResetAt = j
        return cords
    def drawImage(self):
        #Draw the image, this will be over-ridden by class for other
        #image modes, so this will only be used for the default theme
    
        self.retrieveThemeConfig()
 
        #Generate the start points
        #self.startPoints = []
        #for i in range(0,self.strandNum):
        #    self.startPoints.append(self.makeCords())
 
        self.initImg()
        allCords = []
        self.colsDone = 1
        for i in range(0,self.strandNum):
            allCords.append(self.strandWorker(i,int(self.branches/self.strandNum)))
#            for j in range(0,self.branches):
        print("Strand workers finished")
        for k in range(0,len(allCords)):
            for l in range(0,len(allCords[k])):
                self.draw.line(allCords[k][l])
        del self.draw
        self.exportImg()
        #print(startBox)
        #print(sections)

    def makeCords(self):
        cords = ()
        cords = cords + (random.randint(0,self.startBox[0])+int((self.width-self.startBox[0])/2),)
        cords = cords + (random.randint(0,self.startBox[1])+int((self.height-self.startBox[1])/2),)
        return cords
    def initImg(self):
        #Make a blank image
        self.img = Image.new('RGBA',(self.width,self.height),color='#' + getConfigPart(self.theme,"bg"))
        self.draw = ImageDraw.Draw(self.img)

