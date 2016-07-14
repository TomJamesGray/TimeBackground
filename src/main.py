#!/usr/bin/env python
import argparse
import sys
from src.helpers.getConfig import getConfigPart
from src.mode import default,triangles,timeMode
def main(args):
    parser = argparse.ArgumentParser(description='timeBackground')
    #Define arguments
    parser.add_argument('width',action='store', type=int)
    parser.add_argument('height',action='store',type=int)
    parser.add_argument('fileName',action='store',type=str)
    parser.add_argument('--theme',default="theme-default",action='store',type=str)
    parser.add_argument('-s',action='store_true')
    results = parser.parse_args(args)
    width = results.width
    height = results.height
    theme = results.theme
    superSampling = results.s
    fileName = results.fileName
    
    print(superSampling)
    if width <= 0 or height <= 0:
        print('Invalid height or width')
        return 1
    imageMode = getImageMode(theme)
    if imageMode == "default":
        img = default.DefaultImage(width,height,theme,superSampling,fileName)
    elif imageMode == "triangles":
        img = triangles.TrianglesImage(width,height,theme,superSampling,fileName)
    elif imageMode == "time":
        img = timeMode.TimeMode(width,height,theme,superSampling,fileName)
    img.drawImage()
    
    return 0
def getImageMode(theme):
    return getConfigPart(theme,"mode")
