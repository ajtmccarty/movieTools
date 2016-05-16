import re
import logging
import sys

#list of common movie file extensions
MOVIE_FILE_EXTENSIONS = ['avi','mov','wmv','mp4','m4p','m4v','mpg','mpeg', \
                         'mpe','mpv']

'''
class to store various pieces of information regarding a given
piece of Media
rawTitle = actual title of movie, including chars illegal in file names
fTitle = the fTitle is the title used in the file name, w/o illegal chars
year = year of release
mType = type of media
link = url to imdb page for media
actors = list of actors
fDirectory = file path
fName = file name w/o file extensions
fExt = file extension (mp4,avi...)
children = tree children of this Media Object, such as
           (TV episodes under a season or multi-part movies in a directory)
'''
class Media:
    def __init__(self,absolutePath):
        self.rawTitle = ""
        self.fTitle = ""
        self.year = None
        self.mType = ""
        self.link = ""
        self.actors = []
        self.fDirectory = ""
        self.fName = ""
        self.fExt = ""
        self.children = []
        self.extractFromPath(absolutePath)
        self.extractFromFName()

    '''
    INPUT: an absolute path to a file
    OUTPUT: initializes the Media Object with as much information as possible
            from the filename
    '''
    def extractFromPath(self,thisPath):
        [self.fDirectory,rawName] = thisPath.rsplit("/",1)
        #hasPer = has Period?
        hasPer = rawName.count('.')
        #if there are no periods, then there is no file extension
        #and the fName is identical to the path
        if not hasPer:
            self.fName = rawName
            self.fExt = ""
            return
        [name,ext] = rawName.rsplit(".",1)
        #if the path has a file extension, record it
        if ext in MOVIE_FILE_EXTENSIONS:
            self.fName = name
            self.fExt = ext
        else:
            self.fName = rawName
            self.fExt = ""
        return

    '''
    INPUT: None, but runs on the filename of the Media Object
    OUTPUT: tries to extract the title and year from the file name
    '''
    def extractFromFName(self):
        if self.fName == "":
            return
        hasPar = self.fName.count("(")
        #if there is no parenthesis, we assume there is no year
        if not hasPar:
            self.fTitle = self.fName
            return
        [title,year] = self.fName.rsplit("(")
        #check if year is 4 digits followed by a parenthesis
        if re.match("[0-9]{4}\)",year):
            self.year = int(year[:4])
            self.fTitle = title
        else:
            logging.warning("Malformed file name %s",self.fName)
            logging.warning("Has a parenthesis, but does not appear to contain a year")
            sys.stderr.write("Encountered a strange file name "+self.fName+"\n")
            sys.stderr.write("See log file for more information\n")

    def addRawTitle(self, title):
        self.rawTitle = title
        return

    def getRawTitle(self):
        return self.rawTitle

    def addFTitle(self, title):
        self.fTitle = title
        return

    def getFTitle(self):
        return self.fTitle

    def addYear(self, year):
        self.year = int(year)
        return

    def getYear(self):
        return self.year

    def addType(self,mType):
        self.mType = mType
        return

    def getType(self):
        return self.mType

    def addLink(self, link):
        self.link = str(link)
        return

    def getLink(self):
        return self.link

    def addActor(self, actor):
        self.actors.append(actor)
        return

    def getActors(self):
        return self.actors

    def addFDir(self,fDir):
        self.fDir = fDir
        return

    def getFDir(self):
        return self.fDir

    def addFName(self,fName):
        self.fName = fName
        return

    def getFName(self):
        return self.fName

    def addFExt(self,fExt):
        self.fExt = fExt
        return

    def getFExt(self):
        return self.fExt
