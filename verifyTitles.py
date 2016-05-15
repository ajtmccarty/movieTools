#!/usr/bin/python

import os
import sys
#import re
#import PyMovies

#Default directory of movies
MOVIE_DIRECTORY = '/mnt2/Media/Movies'
#list of common movie file extensions
MOVIE_FILE_EXTENSIONS = ['avi','mov','wmv','mp4','m4p','m4v','mpg','mpeg', \
                         'mpe','mpv']

'''
INPUT: Directory containing names and directories of the Movies
OUTPUT: a dictionary in which
        the key is the unaltered name of the file or directory
        the value is the file name with the extension removed
'''
def getRawNames(directory):
    rawNames = {}
    try:
        files = os.listdir(directory)
    except OSError:
        sys.stderr.write('Invalid target directory: '+directory+'\n')
        sys.stderr.write('Either doesn\'t exist or cannot access \n')
        sys.stderr.write('Quitting...\n')
        sys.exit(0)
    for thisName in files:
        #perInd = period index
        perInd = thisName.rfind('.')
        #if there are no periods, then there is no file extensions
        #and we can move on
        if perInd == -1:
            rawNames[thisName] = thisName
            continue
        #save the raw name before we alter it
        rawName = thisName
        extension = thisName[perInd+1:]
        #if this name has a file extension
        if extension in MOVIE_FILE_EXTENSIONS:
            thisName = thisName[:perInd]
        rawNames[rawName] = thisName
    return rawNames
'''
def checkTitles(tFile):
    with open(tFile,'r') as f:
        for movie in f:
            leftPar = movie.rfind('(')
            rightPar = movie.rfind(')')
            if (leftPar > 0) and (rightPar > 0):
                title = movie[:leftPar].strip()
                year = movie[leftPar+1:rightPar]
            elif (leftPar > 0) or (rightPar > 0):
                print 'POTENTIAL ODD TITLE WARNING:'
                print movie
            else:
                year = ''
                period = movie.rfind('.')
                if period > 0:
                    title = movie[:period]
                else:
                    title = movie
            print title+'|'+year
'''

if __name__ == '__main__':
    rawTitles = getRawNames(MOVIE_DIRECTORY)
