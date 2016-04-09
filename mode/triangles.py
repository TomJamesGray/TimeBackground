#Import the DefaultImage class to allow the triangles class
#To inherit from it
from mode.default import DefaultImage
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
        for i in range(0,self.triangles):
            #Get a coordinate for each triangle, then get two more points from 
            #that are equal to the appropriate entry in sideSizes
            #self.cords.append(self.makeCords())
            startCord = self.makeCords()
        print(self.cords)
