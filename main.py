#!/usr/bin/env python
import argparse
def main():
   parser = argparse.ArgumentParser(description='timeBackground')
   parser.add_argument('width',action='store', type=int)
   parser.add_argument('height',action='store',type=int)
   print(parser.parse_args())
    
if __name__ == '__main__':
    main()
