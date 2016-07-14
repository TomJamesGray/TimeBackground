#Import the DefaultImage class to allow the triangles class
#To inherit from it
from src.mode.default import DefaultImage
from PIL import Image,ImageDraw
from src.helpers.helpers import getArgsBy
from src.helpers.getConfig import getConfigPart
import math
import random
class TrianglesImage(DefaultImage):
    def superSamplingEnable(self):
        if self.superSampling:
            print("Enabling super sampling")
            self.width *= 2
            self.height *= 2
            for i in range(0,len(self.sideSizes)):
                self.sideSizes[i] *= 2 
            

    def retrieveThemeConfig(self):
        self.colors = getArgsBy(getConfigPart(self.theme,"colors"),',')
        self.bg = '#' + getConfigPart(self.theme,"bg")
        self.sideSize = int(getConfigPart(self.theme,"sideSizes"))
        self.joined = bool(int(getConfigPart(self.theme,"joined")))
        self.triangles = int(getConfigPart(self.theme,"triangles"))
        self.outlineCol = getConfigPart(self.theme,"outline",True)
        if not self.outlineCol == None:
            self.outlineCol = '#' + self.outlineCol
        #Enable superSampling if asked
        self.superSamplingEnable()

    def drawImage(self):
        self.retrieveThemeConfig()

        self.initImg()
        print("Joined: {}".format(self.joined)) 
        self.cords = []
        #Get first angle required for the triangle with the cosine rule
        angle = math.acos((self.sideSize**2+self.sideSize**2-self.sideSize**2)/
                (2*self.sideSize*self.sideSize))
        self.trianglesPerColor = int(self.triangles/len(self.colors))
        self.colsDone = 0
        self.color = '#' + self.colors[self.colsDone]
        for i in range(0,self.triangles):
            if i % self.trianglesPerColor == 0:
                self.color = '#' + self.colors[self.colsDone]
                print("Switching to color {} at triangle no {}".format(self.colsDone,i))
                self.colsDone += 1
            
            if self.joined and i > 0:
                if i > 1:
                    self.oldRandCordNum = self.randCordNum
                    if self.oldRandCordNum % 2 == 0:
                        print("Finding odd num")
                        #Previous triangle was made with 'even' so this 
                        #triangle will be made with 'odd' numbers, I'll write docs later, I think....
                        #and 7 is used to make randrange go up to 5
                        self.randCordNum = random.randrange(1,7,2)
                    elif self.oldRandCordNum % 2 != 0:
                        print("Finding even num")
                        #Previos triangle made with odd so this triangle
                        #will be made with even numbers
                        if self.oldRandCordNum == 3:
                            self.randCordNum = random.randrange(2,6,2)
                        elif self.oldRandCordNum == 1:
                            #Get 0 or 6 as 3 would just cover the previous triangle
                            self.randCordNum = random.choice([0,4])
                        elif self.oldRandCordNum == 5:
                            #Get 0 or 2 as 4 would just cover the previous triangle
                            self.randCordNum = random.randrange(0,4,2)
                    elif self.oldRandCordNum != 0:
                        while self.oldRandCordNum != self.randCordNum:
                            #Use 'even' randCordNum on this triangle
                            self.randCordNum = random.randrange(0,6,2)
                else:
                    #Previous triangle was made with 0 (even)
                    #so make this randCordNum odd
                    print("Finding odd num (1st randCordNum)")
                    self.randCordNum = random.randrange(1,7,2)
                #self.randCordNum = 5 
                #Dict to map which cord index should
                #be used for a specific 'randCordNum'
                self.cordIndexMap = {
                    0:2,
                    1:2,
                    2:2,
                    3:2,
                    4:0,
                    5:0
                }
                self.cords = [self.cords[self.cordIndexMap.get(self.randCordNum)]]
                # Random number creates triangle in position shown bellow:
                # 0 = leftBaseBottom
                # 1 = leftBaseTop
                # 2 = rightBaseBottom
                # 3 = rightBaseTop
                # 4 = upBaseBottom
                # 5 = downBaseTop
                print("randCordNum: {}".format(self.randCordNum))
                if self.randCordNum == 0:
                    self.cords.append((self.cords[0][0]-self.sideSize,
                        self.cords[0][1]))
                    self.cords.append((int(self.cords[0][0]-self.sideSize*0.5),
                        int(self.cords[0][1]-round(math.sin(angle)*self.sideSize))))
                    #Swap 0 and 1 around so they're in the expected order
                    self.cords[0], self.cords[1] = self.cords[1], self.cords[0]
                elif self.randCordNum == 1:
                    self.cords.append((self.cords[0][0]-self.sideSize,
                        self.cords[0][1])) 
                    self.cords.append((int(self.cords[0][0]-self.sideSize*0.5),
                        int(self.cords[0][1]+round(math.sin(angle)*self.sideSize))))
                    #Swap 0 and 1 around so they're in the expected order
                    self.cords[0], self.cords[1] = self.cords[1], self.cords[0]
                elif self.randCordNum == 2:
                    self.cords.append((self.cords[0][0]+self.sideSize,
                        self.cords[0][1]))
                    self.cords.append((int(self.cords[0][0]+self.sideSize*0.5),
                        int(self.cords[0][1]-round(math.sin(angle)*self.sideSize))))
                elif self.randCordNum == 3:
                    self.cords.append((self.cords[0][0]+self.sideSize,
                        self.cords[0][1]))
                    self.cords.append((self.cords[0][0]+self.sideSize*0.5,
                        self.cords[0][1]+round(math.sin(angle)*self.sideSize)))
                elif self.randCordNum == 4:
                    self.cords.append((self.cords[0][0]+self.sideSize,
                        self.cords[0][1]))
                    self.cords.append((self.cords[0][0]+self.sideSize*0.5,
                        int(self.cords[0][1]-round(math.sin(angle)*self.sideSize))))
                elif self.randCordNum == 5:
                    self.cords.append((int(self.cords[0][0]+self.sideSize),
                        self.cords[0][1]))
                    self.cords.append((self.cords[0][0]+self.sideSize*0.5,
                        int(self.cords[0][1]+round(math.sin(angle)*self.sideSize))))

            # Not joined theme or first triangle      
            else:
                #Get a coordinate for each triangle, then get two more points from 
                #that are equal to the appropriate entry in sideSizes
                self.cords = []
                self.cords.append(self.makeCords())
                #Get the first pair of cords
                self.cords.append((self.cords[0][0]+self.sideSize,
                    self.cords[0][1]))
                #Get the second pair of cords using Opposite=Sin(x)*Hypotenuse
                self.cords.append((int(self.cords[0][0]+self.sideSize*0.5),
                    int(self.cords[0][1]-round(math.sin(angle)*self.sideSize))))
            
            #Draw the triangle
            self.draw.polygon(self.cords,self.color,self.outlineCol)
            print(self.cords)
            print("-----------------------------")
        self.exportImg()
