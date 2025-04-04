'''
    testApplication module part of scxml4py unit tests.
    
    @authors: landolfa
'''

import unittest
import logging
import threading
import time
from pathlib import Path
from queue import Queue

import scxml4py.helper
from scxml4py.listeners import StatusListener
from scxml4py.reader import Reader
from scxml4py.action import Action
from scxml4py.activity import ThreadedActivity
from scxml4py.context import Context
from scxml4py.event import Event
from scxml4py.executor import Executor
from scxml4py.exceptions import ScxmlError, ScxmlSyntaxError


class ActionStatus(Action, StatusListener):
    # implemented by the developer, stub can be generated
    def __init__(self):
        Action.__init__(self, "STATUS.Execute", None, None)
        self.mStatus = None
    
    def notify(self, status):
        self.mStatus = status
    
    def execute(self, theCtx):
        logging.getLogger("scxml4py").info("Status: <" + scxml4py.helper.formatStatus(self.mStatus) + ">")


class ActivityInitializing(ThreadedActivity):
    def __init__(self, theEventQueue, theData):
        ThreadedActivity.__init__(self, "Initializing", theEventQueue, theData)

    def run(self):
        while self.isRunning() == True:
            logging.getLogger("scxml4py").info("Activity <" + self.getId() + "> is running...")
            # @TODO init code here
            self.sendInternalEvent(Event("INITCLOSED"))
            self.setRunning(False)
            break

class ActivityDisabling(ThreadedActivity):
    def __init__(self, theEventQueue, theData):
        ThreadedActivity.__init__(self, "Disabling", theEventQueue, theData)

    def run(self):
        while self.isRunning() == True:
            logging.getLogger("scxml4py").info("Activity <" + self.getId() + "> is running...")
            # @TODO disable code here
            self.sendInternalEvent(Event("DISABLECLOSED"))
            self.setRunning(False)
            break

class ActivityOpening(ThreadedActivity):
    def __init__(self, theEventQueue, theData):
        ThreadedActivity.__init__(self, "Opening", theEventQueue, theData)

    def run(self):
        while self.isRunning() == True:
            logging.getLogger("scxml4py").info("Activity <" + self.getId() + "> is running...")
            # @TODO open shutter code here
            self.sendInternalEvent(Event("ISOPEN"))
            self.setRunning(False)
            break

class ActivityClosing(ThreadedActivity):
    def __init__(self, theEventQueue, theData):
        ThreadedActivity.__init__(self, "Closing", theEventQueue, theData)

    def run(self):
        while self.isRunning() == True:
            logging.getLogger("scxml4py").info("Activity <" + self.getId() + "> is running...")
            # @TODO closing shutter code here
            self.sendInternalEvent(Event("ISCLOSED"))
            self.setRunning(False)
            break
            
class Data(object):
    # implemented by the developer
    # data shared between actions and activities
    def __init__(self):
        self.mSharedInfo = None
    
    def getSharedInfo(self):
        # requires mutex
        return sharedInfo
    
    def setSharedInfo(self, sharedInfo):
        # requires mutex
        self.mSharedInfo = sharedInfo


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
    
    def createActions(self, theEventQueue, theData):
        self.mActionList = [ActionStatus(), 
                            Action("STOP.Execute"), 
                            Action("INIT.Execute"), 
                            Action("INIT.Complete"), 
                            Action("INIT.Abort"), 
                            Action("RESET.Execute"), 
                            Action("ENABLE.Complete"), 
                            Action("DISABLE.Execute"),
                            Action("OPEN.Execute"), 
                            Action("CLOSE.Execute"),
                            Action("UNEXP.Execute"), 
                            Action("ERR.Execute")]
    
    def createActivities(self, theEventQueue, theData):
        self.mActivityList = [ActivityInitializing(theEventQueue, theData), 
                              ActivityOpening(theEventQueue, theData), 
                              ActivityClosing(theEventQueue, theData), 
                              ActivityDisabling(theEventQueue, theData)]
    
    
class Application(threading.Thread):   
    def __init__(self, theModelPath, theEventQueue):
        threading.Thread.__init__(self)
        self.mRunning = False
        self.mModelPath = theModelPath
        self.mEventQueue = theEventQueue
        self.mData = Data()
        
        self.mActionMgr = ActionMgr()
        self.mActionMgr.createActions(self.mEventQueue, self.mData)
        self.mActionMgr.createActivities(self.mEventQueue, self.mData)
        
        self.mContext = Context()
        logging.getLogger("scxml4py").info("Loading SCXML model: <" + theModelPath.__str__() + ">") 
        self.mModel = Reader().read(theModelPath.__str__(), self.mActionMgr.getActions(), self.mActionMgr.getActivities())
        logging.getLogger("scxml4py").debug("Loaded SCXML model: " + scxml4py.helper.formatModel(self.mModel))
        self.mExecutor = Executor(self.mModel, self.mContext)
        self.mExecutor.addStatusListener(self.mActionMgr.getAction("STATUS.Execute"))
        logging.getLogger("scxml4py").info("Status: <" + scxml4py.helper.formatStatus(self.mExecutor.getStatus()) + ">")
        
    def run(self):
        logging.getLogger("scxml4py").info("Starting execution of <" + self.mModel.getId() + ">")
        self.mRunning = True
        self.mExecutor.start()
        logging.getLogger("scxml4py").info("Status: <" + scxml4py.helper.formatStatus(self.mExecutor.getStatus()) + ">")
        while self.mRunning == True:
            theEvent = self.mEventQueue.get(True, None)
            #Queue().get(block, timeout)
            # loop on the event queue send the event to the SM engine
            logging.getLogger("scxml4py").info("Application received event = <" + theEvent.__str__() + ">")
            self.mExecutor.processEvent(theEvent)
            if theEvent.getId() == "OFF":
                logging.getLogger("scxml4py").debug("Application exiting...")
                self.mRunning = False
        logging.getLogger("scxml4py").info("Stopping execution of <" + self.mModel.getId() + ">")
        self.mExecutor.stop()
        logging.getLogger("scxml4py").info("Status: <" + scxml4py.helper.formatStatus(self.mExecutor.getStatus()) + ">")
            
            
            
class TestShutter(unittest.TestCase):

    def setUp(self):        
        unittest.TestCase.setUp(self)
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(threadName)s - %(module)s - %(funcName)s - %(message)s', level=logging.INFO)
        # setup the path to the directory containing the SCXML models
        self.mModelsPath = Path(".")
        for x in self.mModelsPath.iterdir():
            if x.is_dir() and x.__str__() == "models":
                self.mModelsPath = self.mModelsPath / "models"
                #print("found models dir")
                break
            elif x.is_dir() and x.__str__() == "test":
                self.mModelsPath = self.mModelsPath / "test" / "models"
                #print("found test dir")
                break
        #self.mCurrentPath.resolve()
        #print("===> " + self.mCurrentPath.__str__())  
          
    def testShutter(self):
        myEventQueue = Queue()
        filePath = self.mModelsPath / 'scxmlShutter.xml'
        filePath.resolve()
        myApp = Application(filePath, myEventQueue)
        myApp.start()
        myEventQueue.put(Event("STATUS"), True, 2)
        myEventQueue.put(Event("INIT"), True, 2)
        time.sleep(2) # @TODO wait until it is initialized
        myEventQueue.put(Event("STATUS"), True, 2)
        myEventQueue.put(Event("ENABLE"), True, 2)
        myEventQueue.put(Event("STATUS"), True, 2)
        myEventQueue.put(Event("OPEN"), True, 2)
        time.sleep(2) # @TODO wait until it is open
        myEventQueue.put(Event("STATUS"), True, 2)
        myEventQueue.put(Event("CLOSE"), True, 2)
        time.sleep(2) # @TODO wait until it is closed
        myEventQueue.put(Event("STATUS"), True, 2)
        myEventQueue.put(Event("DISABLE"), True, 2)
        time.sleep(2) # @TODO wait until it is disabled
        myEventQueue.put(Event("STATUS"), True, 2)
        myEventQueue.put(Event("RESET"), True, 2)
        myEventQueue.put(Event("STATUS"), True, 2)
        myEventQueue.put(Event("OFF"), True, 2)
        myApp.join()
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

