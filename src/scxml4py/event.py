'''
    event module part of scxml4py.
    @authors: landolfa

'''

from enum import Enum
from functools import total_ordering


class EventType(Enum):
    CALL_EVENT = 0 
    CHANGE_EVENT = 1
    SIGNAL_EVENT = 2
    TIME_EVENT = 3
    ERROR_EVENT = 4

class EventStatus(Enum):
    TOBEPROCESSED = 0 
    PROCESSED = 1
    IGNORED = 2
    REJECTED = 3
    DEFERRED = 4

@total_ordering
class Event(object):

    def __init__(self, theId, theType = EventType.CHANGE_EVENT, theStatus = EventStatus.TOBEPROCESSED):
        self.mId = theId
        self.mType = theType
        self.mStatus = theStatus
        
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
        
    def getType(self, theType):
        self.mType = theType
        
    def getStatus(self):
        return(self.mStatus)
            
    def setId(self, theId):
        self.mId = theId
    
    def setType(self, theType):
        assert (theType >= EventType.CALL_EVENT and theType <= EventType.ERROR_EVENT)
        self.mType = theType

    def setStatus(self, theStatus):
        # @TODO assertion doesn't work:
        # "TypeError: unorderable types: EventStatus() >= EventStatus()"
        #assert (theStatus >= EventStatus.TOBEPROCESSED and theStatus <= EventStatus.DEFERRED)
        self.mStatus = theStatus

    def clone(self, regionNo):
        clonedEvent = Event(self.mId + str(regionNo))
        clonedEvent.mType = self.mType
        # runtime info does not need to be cloned
        #clonedEvent.mStatus = self.mStatus
        return clonedEvent
    