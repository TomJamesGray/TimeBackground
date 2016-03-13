#!/usr/bin/env python
import argparse
import sys
from makeImage import makeImage
def main(args):
    print(args)
    parser = argparse.ArgumentParser(description='timeBackground')
    #Define arguments
    parser.add_argument('width',action='store', type=int)
    parser.add_argument('height',action='store',type=int)

    results = parser.parse_args(args)
    width = results.width
    height = results.height

    if width <= 0 or height <= 0:
        print('Invalid height or width')
        return 1
    else:
        makeImage(width,height)
    return 0
if __name__ == '__main__':
    main(sys.argv[1:])
