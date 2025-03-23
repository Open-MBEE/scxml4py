'''
    context module part of scxml4py.
    @authors: landolfa
    
'''


class Context(object):
    def __init__(self):
        self.mName = ""
        self.mSessionId = ""
        self.mLastEvent = None
        self.mElements = dict()
        
    def __str__(self):
        return self.mName.__str__() + "_" + self.mSessionId.__str__()

    def getName(self):
        return self.mName
    
    def getSessionId(self):
        return self.mSessionId

    def getLastEvent(self):
        return self.mLastEvent;
    
    def getElement(self, theName):
        if theName in self.mElements.keys():
            return self.mElements[theName]
        else:
            return None
        
    def setName(self, theName):
        self.mName = theName
        
    def setSessionId(self, theId):
        self.mSessionId = theId
            
    def setLastEvent(self, theEvent):
        self.mLastEvent = theEvent
    
    def addElement(self, theName, theElement):
        if theElement != None and theName != None:
            self.mElements[theName] = theElement
    
    def delElement(self, theName):
        if theName in self.mElements.keys():
            del self.mElements[theName]
        