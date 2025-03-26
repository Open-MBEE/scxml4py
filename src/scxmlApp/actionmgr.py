class ActionMgr(object):
    # generated class    
    def __init__(self):
        self.mActionList = list()
        self.mActivityList = list()

    def getAction(self, theActionId):
        for a in self.mActionList:
            if a.getId() == theActionId:
                return a
        return None

    def getActions(self):
        return self.mActionList
    
    def getActivity(self, theActivityId):
        for a in self.mActivityList:
            if a.getId() == theActivityId:
                return a
        return None
    
    def getActivities(self):
        return self.mActivityList
    
    def createActions(self, theData, action_classes):
        self.mActionList = [cls(theData) for cls in action_classes]

    def createActivities(self, theEventQueue, theData, activity_classes):
        self.mActivityList = [cls(theEventQueue, theData) for cls in activity_classes]
