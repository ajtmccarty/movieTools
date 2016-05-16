#!/usr/bin/python

import os
import sys
from MediaClass import Media
import logging
#import re

#Default directory of movies
MOVIE_DIRECTORY = '/mnt2/Media/Movies'

'''
INPUT: Directory containing names and directories of the Movies
OUTPUT: a list of MediaClass.Media objects holding the absolute path to the file
        and the name of the file with no extension
'''
def getRawNames(directory):
    rawMedia = []
    try:
        files = os.listdir(directory)
    except OSError:
        sys.stderr.write('Invalid target directory: '+directory+'\n')
        sys.stderr.write('Either doesn\'t exist or cannot access \n')
        sys.stderr.write('Quitting...\n')
        sys.exit(0)
    for thisPath in files:
        thisObject = Media()
        thisObject.addPath(directory+"/"+thisPath)
        rawMedia.append(thisObject)
    return rawMedia

'''
INPUT: Media Object with a defined rawName
OUTPUT: logging module records issues with rawName
        option to change rawName and path through commandLine
'''
def checkRawNameFormat(thisMedia):
    rawName = thisMedia.getRawName()
    #rawName should contain movie year between parentheses
    leftPar = rawName.rfind('(')
    rightPar = rawName.rfind(')')
    if (leftPar > 0) and (rightPar > 0):
        title = rawName[:leftPar].strip()
        year = rawName[leftPar+1:rightPar]
    #log if no parentheses
    elif (leftPar > 0) or (rightPar > 0):
        logging.warning("Movie %s does not have a year value",rawName)
    else:
        year = None
        title = rawName
    print title+'|'+year

if __name__ == '__main__':
    rawTitles = getRawNames(MOVIE_DIRECTORY)
