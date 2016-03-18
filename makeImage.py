from PIL import Image,ImageDraw
from helpers.getConfig import getConfigPart
from helpers.helpers import getArgsBy
import re
def makeImage(width,height):
    #Get config parts for bounding box
    offsets = getConfigPart("main","offsetBoundingBox")
    thickness = getConfigPart("main","boundingBoxThickness")
    #Work out  where current time falls in the sections
    sections = getArgsBy(getConfigPart("main","timeSections"),',',False)
    if len(sections) % 2 != 0:
        raise Exception("Invalid config file, not pairs of values provided in timeSection")
    else:
       print("Ok") 
    print(sections)


