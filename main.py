#!/usr/bin/env python
import argparse
import sys
from makeImage import MainImage
from helpers.getConfig import getConfigPart
def main(args):
    parser = argparse.ArgumentParser(description='timeBackground')
    #Define arguments
    parser.add_argument('width',action='store', type=int)
    parser.add_argument('height',action='store',type=int)
    parser.add_argument('--theme',default="theme-default",action='store',type=str)
    parser.add_argument('-s',action='store_true')
    results = parser.parse_args(args)
    width = results.width
    height = results.height
    theme = results.theme
    superSampling = results.s
    
    print(superSampling)
    if width <= 0 or height <= 0:
        print('Invalid height or width')
        return 1
    imageMode = getImageMode(theme)
    if imageMode == "default":
        img = MainImage(width,height,theme,superSampling)
    img.drawImage()
    
    return 0
def getImageMode(theme):
    return getConfigPart(theme,"mode")
if __name__ == '__main__':
    main(sys.argv[1:])
