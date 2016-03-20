from PIL import Image,ImageDraw
from helpers.getConfig import getConfigPart
from helpers.helpers import getArgsBy
from time import strftime
import random
import re
def makeImage(width,height,theme):
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
    img = Image.new('RGBA',(width,height),color='#' + getConfigPart(theme,"bg"))
    draw = ImageDraw.Draw(img)
    branchDist = int(getConfigPart(theme,"branchDist"))
    thickness = int(getConfigPart(theme,"thickness"))
    branches = int(getConfigPart(theme,"branches"))
    colors = getArgsBy(getConfigPart(theme,"colors"),',')
    colsDone = 1
    for i in range(0,strandNum):
        for j in range(0,branches):
            if colsDone*branches/len(colors) < j:
                color = '#' + colors[colsDone]
                print("Switching to color {} at branch no {}".format(colsDone,j))
                colsDone += 1
            else:
                color = '#' + colors[colsDone-1]
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
            #Check if coordinates have gone off the image and if so start a new strand and
            #abandon the strand which is off the page
            if (startPoints[i][0] > width or startPoints[i][0] < 0 or
                startPoints[i][1] > width or startPoints[i][1] < 0):
                    cords = ()
                    cords = cords + (random.randint(0,startBox[0])+int((width-startBox[0])/2),)
                    cords = cords + (random.randint(0,startBox[1])+int((height-startBox[1])/2),)
                    startPoints[i] = cords
    del draw
    img.save("img.png","PNG")

    print(startPoints)
    print(startBox)
    print(sections)


