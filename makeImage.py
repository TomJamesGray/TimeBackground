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
    
    strandNum=3
    startPoints = []
    for i in range(0,strandNum):
        cords =() 
        cords = cords + (random.randint(0,startBox[0])+int((width-startBox[0])/2),)
        cords = cords + (random.randint(0,startBox[1])+int((height-startBox[1])/2),)
        startPoints.append(cords)

    #Make a blank image
    img = Image.new('RGBA',(width,height),color=(255,255,255,255))
    draw = ImageDraw.Draw(img)
    draw.line(startPoints,'#F00',1) 
    
    del draw
    img.save("img.png","PNG")

    print(startPoints)
    print(startBox)
    print(sections)


