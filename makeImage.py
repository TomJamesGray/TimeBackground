from PIL import Image,ImageDraw
from helpers.getConfig import getConfigPart
from helpers.helpers import getArgsBy
from time import strftime
import random
import re
def makeImage(width,height):
    #Get config parts for startBox
    offsets = getConfigPart("main","offsetBoundingBox")
    #Work out  where current time falls in the sections
    sections = getArgsBy(getConfigPart("main","timeSections"),',',False)
    if len(sections) % 2 != 0:
        raise Exception("Invalid config file, not pairs of values provided in timeSection")
    #Get dims of startBox get rand num inside those vals
    startBox = []
    startBox.append(int(width*(1-int(getArgsBy(offsets,',')[0])/100)))
    startBox.append(int(height*(1-int(getArgsBy(offsets,',')[1])/100)))
    
    strandNum = 3
    startPoints = []
    for i in range(0,strandNum):
        cords =() 
        cords = cords + (random.randint(0,startBox[0])+int((width-startBox[0])/2),)
        cords = cords + (random.randint(0,startBox[1])+int((height-startBox[1])/2),)
        startPoints.append(cords)

    #Make a blank image
    img = Image.new('RGBA',(width,height),color=(255,255,255,255))
    draw = ImageDraw.Draw(img)
    branchDist = int(getConfigPart("lines","branchDist"))
    thickness = int(getConfigPart("lines","thickness"))
    branches = int(getConfigPart("lines","branches"))
    color = '#' + getConfigPart("lines","color")
    for i in range(0,strandNum):
        for j in range(0,branches):
            direction = random.randint(0,3)
            #0=up, 1 left, 2=down, 3=right
            if direction == 0:
                newCords = (startPoints[i][0],startPoints[i][1]+branchDist)
                draw.line([startPoints[i],newCords],color,thickness)
                startPoints[i] = newCords
            elif direction == 1:
                newCords = (startPoints[i][0]+branchDist,startPoints[i][1])
                draw.line([startPoints[i],newCords],color,thickness)
                startPoints[i] = newCords
            elif direction == 2:
                newCords = (startPoints[i][0],startPoints[i][1]-branchDist)
                draw.line([startPoints[i],newCords],color, thickness)
                startPoints[i] = newCords
            elif direction == 3:
                newCords = (startPoints[i][0]-branchDist,startPoints[i][1])
                draw.line([startPoints[i],newCords],color,thickness)
                startPoints[i] = newCords
    del draw
    img.save("img.png","PNG")

    print(startPoints)
    print(startBox)
    print(sections)


