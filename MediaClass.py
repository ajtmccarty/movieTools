#list of common movie file extensions
MOVIE_FILE_EXTENSIONS = ['avi','mov','wmv','mp4','m4p','m4v','mpg','mpeg', \
                         'mpe','mpv']

'''
class to store various pieces of information regarding a given
piece of Media
title = title
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
    def __init__(self,absolutePath=""):
        self.title = ""
        self.year = None
        self.mType = ""
        self.link = ""
        self.actors = []
        self.fDirectory = ""
        self.fName = ""
        self.fExt = ""
        self.children = []
        if absolutePath:
            self.extractFromPath(absolutePath)

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

    def extractFromRawName(self):
        pass

    def addTitle(self, title):
        self.title = str(title)
        return

    def addYear(self, year):
        self.year = int(year)
        return

    def addType(self,mType):
        self.mType = mType
        return

    def addLink(self, link):
        self.link = str(link)
        return

    def addActor(self, actor):
        self.actors.append(actor)
        return

    def addFDir(self,fDir):
        self.fDir = fDir
        return

    def addFName(self,fName):
        self.fName = fName
        return

    def addFExt(self,fExt):
        self.fExt = fExt
        return

    def getFDir(self):
        return self.fDir

    def getFName(self):
        return self.fName

    def getFExt(self):
        return self.fExt

    def getTitle(self):
        return self.title

    def getYear(self):
        return self.year

    def getType(self):
        return self.mType

    def getLink(self):
        return self.link

    def getActors(self):
        return self.actors
