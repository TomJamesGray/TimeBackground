#!/usr/bin/env python
import argparse
from makeImage import makeImage
def main():
   parser = argparse.ArgumentParser(description='timeBackground')
   #Define arguments
   parser.add_argument('width',action='store', type=int)
   parser.add_argument('height',action='store',type=int)
   
   results = parser.parse_args()
   width = results.width
   height = results.height
    
   if width <= 0 or height <= 0:
       raise ValueError('Invalid height or width')
   else:
        makeImage(width,height)
if __name__ == '__main__':
    main()
