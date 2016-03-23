from PIL import Image,ImageDraw
from helpers.getConfig import getConfigPart
from helpers.helpers import getArgsBy
from time import strftime
import random
import re
class MainImage(object):
    def __init__(self,width,height,theme,superSampling):
        self.width = width
        self.height = height
        self.theme = theme
        self.superSampling = superSampling

        self.retrieveConfig()
        self.superSamplingEnable()
       
        self.startBox = []
        self.startBox.append(int(width*(1-int(getArgsBy(self.offsets,',')[0])/100)))
        self.startBox.append(int(height*(1-int(getArgsBy(self.offsets,',')[1])/100)))
        
        print("startBox: {}".format(self.startBox))
    def retrieveConfig(self):
        self.offsets = getConfigPart("main","offsetBoundingBox")
    
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

    def superSamplingEnable(self):
        if self.superSampling:
            self.width *= 2
            self.height *= 2
            self.branchDist *= 2
            self.thickness *= 2

    def drawImage(self):
        #Draw the image, this will be over-ridden by class for other
        #image modes, so this will only be used for the default theme
    
        self.retrieveThemeConfig()
 
        #Generate the start points
        self.startPoints = []
        for i in range(0,self.strandNum):
            self.startPoints.append(self.makeCords())
 

        #Make a blank image
        self.img = Image.new('RGBA',(self.width,self.height),color='#' + getConfigPart(self.theme,"bg"))
        self.draw = ImageDraw.Draw(self.img)
        self.colsDone = 1
        for i in range(0,self.strandNum):
            self.branchResetAt = 0 
            for j in range(0,self.branches):
                if self.colsDone*self.branches/len(self.colors) < j:
                    self.color = '#' + self.colors[self.colsDone]
                    print("Switching to color {} at branch no {}".format(self.colsDone,j))
                    self.colsDone += 1
                else:
                    self.color = '#' + self.colors[self.colsDone-1]

                self.direction = random.randint(0,3)
                #0=up, 1 left, 2=down, 3=right
                if self.direction == 0:
                    self.newCords = (self.startPoints[i][0],self.startPoints[i][1]+self.branchDist)
                    self.draw.line([self.startPoints[i],self.newCords],self.color,self.thickness)
                    self.startPoints[i] = self.newCords
                elif self.direction == 1:
                    self.newCords = (self.startPoints[i][0]+self.branchDist,self.startPoints[i][1])
                    self.draw.line([self.startPoints[i],self.newCords],self.color,self.thickness)
                    self.startPoints[i] = self.newCords
                elif self.direction == 2:
                    self.newCords = (self.startPoints[i][0],self.startPoints[i][1]-self.branchDist)
                    self.draw.line([self.startPoints[i],self.newCords],self.color, self.thickness)
                    self.startPoints[i] = self.newCords
                elif self.direction == 3:
                    self.newCords = (self.startPoints[i][0]-self.branchDist,self.startPoints[i][1])
                    self.draw.line([self.startPoints[i],self.newCords],self.color,self.thickness)
                    self.startPoints[i] = self.newCords
                if j-self.branchResetAt ==  self.maxBranchTurns:
                    self.startPoints[i] = self.makeCords()
                    self.branchResetAt = j
            #Check if coordinates have gone off the image and if so start a new strand and
            #abandon the strand which is off the page
            if (self.startPoints[i][0] > self.width or self.startPoints[i][0] < 0 or
                self.startPoints[i][1] > self.height or self.startPoints[i][1] < 0):
                    self.startPoints[i] = self.makeCords() 
                    self.branchResetAt = j
                    print("New cords")

        del self.draw
        if self.superSampling:
            self.img = img.resize((int(self.width/2),int(self.height/2)),Image.NEAREST)
        self.img.save("img.png","PNG")

        print(self.startPoints)
        #print(startBox)
        #print(sections)
       
    def makeCords(self):
        cords = ()
        cords = cords + (random.randint(0,self.startBox[0])+int((self.width-self.startBox[0])/2),)
        cords = cords + (random.randint(0,self.startBox[1])+int((self.height-self.startBox[1])/2),)
        print(cords)
        
        return cords

