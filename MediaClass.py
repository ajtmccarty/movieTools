class Media:
    def __init__(self,title="",year=None,mType='',link="",actors=[]):
        self.mDict = {}
        self.mDict["title"] = title
        self.mDict["year"] = year
        self.mDict["type"] = mType
        self.mDict["link"] = link
        self.mDict["actors"] = actors

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
