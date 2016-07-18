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

        #Calculate how many branches are needed per colour
        self.branchesPerColor = int((self.branches*self.strandNum)/len(self.colors))
        print("Branches per colour {}".format(self.branchesPerColor))
        self.colorsPerStrand = int((len(self.colors)/self.strandNum))
        #Make list of branch indexes when colour should be switched
        self.colSwitchIndexes = []
        for i in range(0,self.branches*self.strandNum):
            if i % self.branchesPerColor == 0:
                self.colSwitchIndexes.append(i)
        print("ColSwitchIndexes: {}".format(self.colSwitchIndexes)) 
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

    #Returns a list of dictionaries, with dictionaries in the format
    #This is quite messy, but I can't think of a better way to do it while
    #still having support for multi-threading
    #{ 'col':hexColourCode,
    #   'cords':[[]]
    #}
    def strandWorker(self,queue,strandNum,branchesForStrand):
        cords = []
        section = {'cords':[]}
        #Make slice of colSwitchIndexes for this strand
        colSwitchIndexesForStrand = self.colSwitchIndexes[
                self.colorsPerStrand*strandNum:self.colorsPerStrand*(strandNum+1)]
        print("indexes for strand {}".format(colSwitchIndexesForStrand))
        section['cords'].append([self.makeCords()])
        #The index for the current colour in colSwitchIndexesForStrand
        curCol = 0
        branchResetAt = 0
        for j in range(0,branchesForStrand):
            section['col'] = '#' + self.colors[self.colSwitchIndexes.index(
                colSwitchIndexesForStrand[curCol])]
            if not curCol + 1 >= len(colSwitchIndexesForStrand):
                if ((strandNum + 1) * (j+1)) >= colSwitchIndexesForStrand[curCol+1]:
                    #If a new color is needed append the existing section dict to
                    #cords and add the existing one to the cords list
                    cords.append(section)
                    section = {'cords':[[cords[-1]['cords'][-1][-1]]]}
                    curCol = curCol + 1
                    print("Switch at {} to {}".format((strandNum + 1) * j,curCol))
                    section['col'] = '#' + self.colors[self.colSwitchIndexes.index(
                        colSwitchIndexesForStrand[curCol])]
            direction = random.randint(0,3)
            #0=up, 1 left, 2=down, 3=right
            if direction == 0:
                section['cords'][-1].append((section['cords'][-1][-1][0],section['cords'][-1][-1][1]+self.branchDist))
            elif direction == 1:
                section['cords'][-1].append((section['cords'][-1][-1][0]+self.branchDist,section['cords'][-1][-1][1]))
            elif direction == 2:
                section['cords'][-1].append((section['cords'][-1][-1][0],section['cords'][-1][-1][1]-self.branchDist))
            elif direction == 3:
                section['cords'][-1].append((section['cords'][-1][-1][0]-self.branchDist,section['cords'][-1][-1][1]))
            
            if j-branchResetAt ==  self.maxBranchTurns:
                cords.append(self.makeCords())
                branchResetAt = j
            #Check if coordinates have gone off the image and if so start a new section dict
            #and append the existing one to the cords list
            if (section['cords'][-1][-1][0] > self.width or section['cords'][-1][-1][0] < 0 or
                section['cords'][-1][-1][1] > self.height or section['cords'][-1][-1][1] < 0):
                    cords.append(section)
                    section = {'cords':[]}
                    section['cords'].append([self.makeCords()])
                    #Assign a colour to this section now as if it is the last run
                    #then this section will be returned without a col
                    section['col'] = '#' + self.colors[self.colSwitchIndexes.index(
                        colSwitchIndexesForStrand[curCol])]
                    branchResetAt = j
        #Append final section to cords
        cords.append(section)
        #Return the value of cords to the queue
        queue.put(cords)
    def drawImage(self):
        #Draw the image, this will be over-ridden by class for other
        #image modes, so this will only be used for the default theme
    
        self.retrieveThemeConfig()
 
        #Generate the start points
        #self.startPoints = []
        #for i in range(0,self.strandNum):
        #    self.startPoints.append(self.makeCords())
 
        self.initImg()
        self.colsDone = 1
        #for i in range(0,self.strandNum):
        #    allCords.append(self.strandWorker(i,int(self.branches/self.strandNum)))
#            for j in range(0,self.branches):
        queue = mp.Queue()
        procs = []
        for i in range(0,self.strandNum):
            procs.append(mp.Process(target=self.strandWorker,args=(queue,i,
                self.branches)))
            procs[i].start()

        self.allCords = []
        for i in range(0,self.strandNum):
            self.allCords.append(queue.get())

        for p in procs:
            p.join()
        
        print("Strand workers finished")
        self.curCol = 0
        for k in range(0,len(self.allCords)):
            for l in range(0,len(self.allCords[k])):
                for m in range(0,len(self.allCords[k][l]['cords'])):
                    self.draw.line(self.allCords[k][l]['cords'][m],
                            self.allCords[k][l]['col'])
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

