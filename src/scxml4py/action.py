'''
    action module part of scxml4py
    @authors: landolfa

'''

import logging
from functools import total_ordering

@total_ordering
class Action(object):
    def __init__(self, theId, theEventQueue = None, theData = None):
        self.mId = theId
        self.mEventQueue = theEventQueue # queue to post internal events
        self.mData = theData # shared data with other actions and activities
        
    def __str__(self):
        return self.mId.__str__()

    def __lt__(self, other):
        if other == None:
            return False        
        return self.mId.__str__() < other.mId.__str__()

    def __eq__(self, other):
        if other == None:
            return False
        return self.mId.__str__() == other.mId.__str__()
    
    def getId(self):
        return self.mId
            
    def getData(self):
        return self.mData
    
    def setId(self, theId):
        self.mId = theId

    def setData(self, theData):
        self.mData = theData

    def sendInternalEvent(self, theEvent):
        if self.mEventQueue != None and theEvent != None:
            logging.getLogger("scxml4py").debug("Triggering internal event <" + theEvent.__str__() + ">") 
            self.mEventQueue.put(theEvent, True, 2)
        
    def execute(self, theCtx):
        pass
    
    def evaluate(self, theCtx):
        return False
    