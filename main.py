#!/usr/bin/env python
import argparse
import sys
from makeImageOOP import MainImage
def main(args):
    print(args)
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
    else:
        #makeImage(width,height,theme,superSampling)
        img = MainImage(width,height,theme,superSampling)
        img.drawImage()
    return 0
if __name__ == '__main__':
    main(sys.argv[1:])
