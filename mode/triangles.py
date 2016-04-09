#Import the DefaultImage class to allow the triangles class
#To inherit from it
from mode.default import DefaultImage
from PIL import Image,ImageDraw
from helpers.helpers import getArgsBy
from helpers.getConfig import getConfigPart
import math
class TrianglesImage(DefaultImage):
    def retrieveThemeConfig(self):
        self.colors = getArgsBy(getConfigPart(self.theme,"colors"),',')
        self.bg = '#' + getConfigPart(self.theme,"bg")
        self.sideSizes = getArgsBy(getConfigPart(self.theme,"sideSizes"),',')
        #Convert the strings for the side sizes to ints
        for i in range(0,len(self.sideSizes)):
            self.sideSizes[i] = int(self.sideSizes[i])
        self.joined = bool(getConfigPart(self.theme,"joined"))
        self.triangles = int(getConfigPart(self.theme,"triangles"))
    def drawImage(self):
        self.retrieveThemeConfig()

        self.initImg()

        #Check that the triangle provided in the config is possible to draw
        #according to the triangle inequality theorem
        print(self.sideSizes)
        if len(self.sideSizes) == 3:
            if not (self.sideSizes[0] + self.sideSizes[1] > self.sideSizes[2] and 
                    self.sideSizes[0] + self.sideSizes[2] > self.sideSizes[1] and
                    self.sideSizes[1] + self.sideSizes[2] > self.sideSizes[0]):
                raise ValueError("Triangle from sizes in config file is impossible to draw")
        else:
            raise ValueError("Insufficient/Too many triangles sizes provided in config file")
        self.cords = []
        #Get first angle required for the triangle with the cosine rule
        angle = math.acos((self.sideSizes[0]**2+self.sideSizes[1]**2-self.sideSizes[2]**2)/
                (2*self.sideSizes[0]*self.sideSizes[1]))
        print(angle)
        for i in range(0,self.triangles):
            #Get a coordinate for each triangle, then get two more points from 
            #that are equal to the appropriate entry in sideSizes
            #self.cords.append(self.makeCords())
            self.cords = []
            self.cords.append(self.makeCords())
            #Get the second pair of cords using Opposite=Sin(x)*Hypotenuse
            self.cords.append((int(self.cords[0][0]+self.sideSizes[0]*0.5),
                int(self.cords[0][1]+round(math.sin(angle)*self.sideSizes[2]))))
            #Get the final pair of cords
            self.cords.append((self.cords[0][0]+self.sideSizes[0],
                self.cords[0][1]))

        print(self.cords)
