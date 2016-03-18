from PIL import Image,ImageDraw
from helpers.getConfig import getConfigPart
from helpers.helpers import getArgsBy
from time import strftime
import random
import re
def makeImage(width,height):
    #Get config parts for startBox
    offsets = getConfigPart("main","offsetBoundingBox")
    thickness = getConfigPart("main","boundingBoxThickness")
    #Work out  where current time falls in the sections
    sections = getArgsBy(getConfigPart("main","timeSections"),',',False)
    if len(sections) % 2 != 0:
        raise Exception("Invalid config file, not pairs of values provided in timeSection")
    #Get dims of startBox get rand num inside those vals
    startBox = []
    startBox.append(int(width*(1-int(getArgsBy(offsets,',')[0])/100)))
    startBox.append(int(height*(1-int(getArgsBy(offsets,',')[1])/100)))
    
    strandNum=3
    startPoints = []
    for i in range(0,strandNum):
        cords = []
        cords.append(random.randint(0,startBox[0]))
        cords.append(random.randint(0,startBox[1]))
        startPoints.append(cords)

    print(startPoints)
    print(startBox)
    print(sections)


