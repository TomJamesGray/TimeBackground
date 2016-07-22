#!/usr/bin/env python
import argparse
import sys
from configparser import NoSectionError
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
    #Run the theme with the specified parameters
    try:
        runIt(results.width,results.height,results.fileName,
            results.theme,results.s)
    except Exception as e:
        print(e)
        return 1
    
def runIt(width,height,fileName,theme="theme-default",superSampling=False):
    if width <= 0 or height <= 0:
        print('Invalid height or width')
        return 1
    try:
        imageMode = getImageMode(theme)
    except NoSectionError as e:
        raise NoSectionError("Couldn't get theme mode for theme {}".format(theme))
    
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
