#!/usr/bin/python
import sys
import os
from MediaClass import Media
import requests
import bs4
import logging

#Default directory of movies
MOVIE_DIRECTORY = '/mnt2/Media/Movies'

'''
Utility for selecting an option from a list
INPUT: the search term and the list of possible options
OUTPUT: the index of the selected option or None
'''
def titleSelector(searchTerm, options):
    print 'SEARCH TERM: ' + searchTerm
    print '---POTENTIAL MATCHES---'
    #print out all the possible matches in options with an index
    for tup in enumerate(options, 1):
        print '(' + str(tup[0]) + ') ' + tup[1]
    #add an option for no good match
    print '(N) No Good Match'
    isValid = False
    #handle user input
    while not isValid:
        selection = raw_input('Please select best match or (N) for none:').lower()
        #must be 'n' or a number
        if selection != 'n' and not selection.isdigit():
            print 'Input must be a number or (N)'
            continue
        if selection == 'n':
            return None
        #if it's not 'n' here, then it must be a number
        selection = int(selection)
        #make sure it's an appropriate number
        if selection < 1 or selection > len(options):
            print 'Input must be between 1 and ' + str(len(options))
            continue
        isValid = True

    #subtract 1 b/c options start at 1 but list is 0 indexed
    return selection - 1

'''
INPUT: Directory containing names and directories of the Movies
OUTPUT: a list of MediaClass.Media objects holding the absolute path to the file
        and the name of the file with no extension
'''
def scanDirectory(directory):
    rawMedia = []
    try:
        result = os.walk(directory)
    except OSError:
        sys.stderr.write('Invalid target directory: '+directory+'\n')
        sys.stderr.write('Either doesn\'t exist or cannot access \n')
        sys.stderr.write('Quitting...\n')
        sys.exit(0)
    (dirpath,dirnames,files) = next(result)
    for thisFile in files:
        thisObject = Media(dirpath+"/"+thisFile)
        rawMedia.append(thisObject)
    return rawMedia

def getMovieActors(title, year):
    #get list of possible Movie Objects
    optionList = imdbTitleSearch(title)
    #find index of correct Movie object, if it exists
    index = titleSelector(title + ' - ' + str(year), [ m.getTitle() + ' - ' + str(m.getYear()) for m in optionList ])
    #get the actors of the Movie object
    actors = imdbGetActors(optionList[index].getLink())
    for actor in actors:
        print actor[0]

def readCommand(argv):
    if len(argv) > 1:
        directory = argv[1]
    else:
        directory = MOVIE_DIRECTORY
    mediaList = scanDirectory(directory)
    for m in mediaList:
        print m.getFTitle()

if __name__ == '__main__':
    logging.basicConfig(filename='PyMovies.log',format='%(asctime)s %(message)s')
    readCommand(sys.argv)
