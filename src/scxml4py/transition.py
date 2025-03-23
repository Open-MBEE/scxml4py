'''
    transition module part of scxml4py.
    
    @authors: landolfa
'''

from scxml4py.executableContent import ExecutableContent


class Transition(object):
    def __init__(self):
        self.mEvent = None
        self.mConditions = ExecutableContent()
        self.mActions = ExecutableContent()
        self.mSource = None
        self.mTargets = list()

    def __str__(self):
        tmp = "FromState <"
        if self.mSource != None:
            tmp += self.mSource.getId()
        tmp += ">"
        tmp += " ToState <"
        isFirst = True
        for s in self.mTargets:
            if isFirst == True:
                isFirst = False
            else:
                tmp += " "
            tmp += s.getId()
        tmp += "> "    
        tmp += " Guards <" + self.mConditions.__str__() + ">"
        if self.mEvent != None:
            tmp += " Event <" + self.mEvent.__str__() + ">"        
        else:    
            tmp += " Event <>" 
        tmp += " Actions <" + self.mActions.__str__() + ">"
        return tmp
    
    def __lt__(self, other):
        if other == None:
            return False
        return self.__str__() < other.__str__()
    
    def __eq__(self, other):
        if other == None:
            return False
        return self.__str__() == other.__str__()
        """
        # compare source state       
        if self.mSource == None and other.mSource != None:
            return False
        if self.mSource != None and other.mSource == None:
            return False        
        if self.mSource != None and other.mSource != None:
            if self.mSource.getAbsoluteId() != other.mSource.getAbsoluteId():
                return False
        # compare destination
        if self.mTargets.__len__() != other.mTargets.__len__():
            return False
        if self.mTargets.__len__() > 0:
            if self.mTargets[0].getAbsoluteId() != other.mTargets[0].getAbsoluteId():
                return False
        # compare triggering events
        if self.mEvent != other.mEvent:
            return False    
        # compare guards
        if self.mConditions != other.mConditions:
            return False
        # compare actions
        return self.mActions == other.mActions
        """
        
    def getSource(self):
        return self.mSource
    
    def getEvent(self):
        return self.mEvent
    
    def getTargets(self):
        return self.mTargets

    def getActions(self):
        return self.mActions
    
    def getConditions(self):
        return self.mConditions
    
    
    def addTarget(self, theState):
        if theState != None:
            self.mTargets.append(theState)

    def addAction(self, theAction):
        if theAction != None:
            self.mActions.addAction(theAction)

    def addCondition(self, theCondition):
        if theCondition != None:
            self.mConditions.addAction(theCondition)

    def isEnabled(self, theContext, theEvent = None):
        # there is no input Event 
        if theEvent == None:
            return (self.getEvent() == None and self.mConditions.evaluate(theContext) == True)
        # there is an input event but no event on the transition
        elif self.getEvent() == None:
            return False;
        # there are both input event and event on the transition
        else:
            return (self.getEvent().getId() == theEvent.getId() and self.mConditions.evaluate(theContext) == True)
        
    def setSource(self, theState):
        self.mSource = theState
        
    def setTargets(self, theTargets):
        self.mTargets = theTargets
        
    def setEvent(self, theEvent):
        self.mEvent = theEvent
        
    def clone(self, regionNo, sourceState, actionMap):
        clonedTrans = Transition()
        clonedTrans.mSource = sourceState
        if self.mEvent != None:
            clonedTrans.mEvent = self.mEvent.clone(regionNo)
        for a in self.mActions.getActions():
            newId = a.getId() + str(regionNo)
            if newId in actionMap:
                clonedTrans.addAction(actionMap[newId])
            else:
                clonedTrans.addAction(a)
        for c in self.mConditions.getActions():
            newId = c.getId() + str(regionNo)
            if newId in actionMap:
                clonedTrans.addCondition(actionMap[newId])
            else:
                clonedTrans.addCondition(c)
        # copy targets states as they are, they will be updated in a second step
        # usign helper.updateClonedTransitionTargets
        for s in self.mTargets:
            clonedTrans.mTargets.append(s)
        return clonedTrans
    