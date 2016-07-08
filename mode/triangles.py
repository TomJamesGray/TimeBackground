#Import the DefaultImage class to allow the triangles class
#To inherit from it
from mode.default import DefaultImage
from PIL import Image,ImageDraw
from helpers.helpers import getArgsBy
from helpers.getConfig import getConfigPart
import math
import random
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
        self.trianglesPerColor = int(self.triangles/len(self.colors))
        self.colsDone = 0
        self.color = '#' + self.colors[self.colsDone]
        for i in range(0,self.triangles):
            if self.colsDone/self.trianglesPerColor <= i:
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
                        self.randCordNum = random.randrange(0,6,2)

                        print("new cordNum: {}".format(self.randCordNum))
                    elif self.oldRandCordNum != 0:
                        while self.oldRandCordNum != self.randCordNum:
                            #Use 'even' randCordNum on this triangle
                            self.randCordNum = random.randrange(0,6,2)
                else:
                    #Previous triangle was made with 0 (even)
                    #so make this randCordNum odd
                    self.randCordNum = random.randrange(1,7,2)
                #self.randCordNum = 5 
                #Dict to map which cord index should
                #be used for a specific 'randCordNum'
                self.cordIndexMap = {
                    0:0,
                    1:1,
                    2:2,
                    3:1,
                    4:1,
                    5:0
                }
                self.randCordNum = 5
                self.cords = [self.cords[self.cordIndexMap.get(self.randCordNum)]]
                # Random number creates triangle in position shown bellow:
                # 0 = leftBaseBottom
                # 1 = leftBaseTop
                # 2 = rightBaseBottom
                # 3 = rightBaseTop
                # 4 = upBaseBottom
                # 5 = downBaseTop
                print("randCordNum: {}".format(self.randCordNum))
                if self.randCordNum == 1:
                    self.cords.append((self.cords[0][0]-self.sideSizes[0],
                        self.cords[0][1])) 
                    self.cords.append((int(self.cords[0][0]-self.sideSizes[0]*0.5),
                        int(self.cords[0][1]+round(math.sin(angle)*self.sideSizes[2]))))
                    #Swap 0 and 1 around so they're in the expected order
                    self.cords[0], self.cords[1] = self.cords[1], self.cords[0]
                elif self.randCordNum == 3:
                    self.cords.append((self.cords[0][0]+self.sideSizes[0],
                        self.cords[0][1]))
                    self.cords.append((self.cords[0][0]+self.sideSizes[0]*0.5,
                        self.cords[0][1]+round(math.sin(angle)*self.sideSizes[2])))
                    #Swtich 0 and 2 to make the list of cords be in the same order of
                    #other triangles made using the 'odd' randCordNums
                    self.cords[0], self.cords[2] = self.cords[2], self.cords[0]
                elif self.randCordNum == 5:
                    self.cords.append((int(self.cords[0][0]+self.sideSizes[0]),
                        self.cords[0][1]))
                    self.cords.append((self.cords[0][0]+self.sideSizes[0]*0.5,
                        int(self.cords[0][1]+round(math.sin(angle)*self.sideSizes[0]))))
                  
            else:
                #Get a coordinate for each triangle, then get two more points from 
                #that are equal to the appropriate entry in sideSizes
                self.cords = []
                self.cords.append(self.makeCords())
                #Get the second pair of cords using Opposite=Sin(x)*Hypotenuse
                self.cords.append((int(self.cords[0][0]+self.sideSizes[0]*0.5),
                    int(self.cords[0][1]-round(math.sin(angle)*self.sideSizes[2]))))
                #Get the final pair of cords
                self.cords.append((self.cords[0][0]+self.sideSizes[0],
                    self.cords[0][1]))
            #Draw the triangle
            self.draw.polygon(self.cords,self.color)
            print(self.cords)
        self.img.save("img.png","PNG")
