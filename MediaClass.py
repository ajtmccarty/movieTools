
'''
class to store various pieces of information regarding a given
piece of Media
path = file path
rawName = file name w/o file extensions
title = title
year = year of release
mType = type of media
link = url to imdb page for media
actors = list of actors
'''
class Media:
    def __init__(self,path,rawName="",title="",year=None,mType='',link="",actors=[]):
        self.mDict = {}
        self.mDict["path"] = path
        self.mDict["rawName"] = rawName
        self.mDict["title"] = title
        self.mDict["year"] = year
        self.mDict["type"] = mType
        self.mDict["link"] = link
        self.mDict["actors"] = actors

    def addPath(self,newPath):
        self.mDict["path"] = newPath
        return

    def addRawName(self,rawName):
        self.mDict["rawName"] = rawName
        return

    def addTitle(self, title):
        self.mDict["title"] = str(title)
        return

    def addYear(self, year):
        self.mDict["year"] = int(year)
        return

    def addType(self,mType):
        self.mDict["type"] = mType
        return

    def addLink(self, link):
        self.mDict["link"] = str(link)
        return

    def addActor(self, actor):
        self.mDict["actors"].append(actor)
        return

    def getPath(self):
        return self.mDict["path"]

    def getRawName(self):
        return self.mDict["rawName"]

    def getTitle(self):
        return self.mDict["title"]

    def getYear(self):
        return self.mDict["year"]

    def getType(self):
        return self.mDict["type"]

    def getLink(self):
        return self.mDict["link"]

    def getActors(self):
        return self.mDict["actors"]
