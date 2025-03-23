import logging
import threading
from queue import Queue

import scxml4py.helper
from scxml4py.reader import Reader
from scxml4py.context import Context
from scxml4py.event import Event
from scxml4py.executor import Executor

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


class Application(threading.Thread):   
    def __init__(self, scxml_doc_str:str, data, theEventQueue, actions, activities):
        threading.Thread.__init__(self)
        self.mRunning = False
        self.mEventQueue = theEventQueue
        self.mData = data
        
        self.mActionMgr = ActionMgr()
        self.mActionMgr.createActions(theData=self.mData, action_classes=actions)
        self.mActionMgr.createActivities(theEventQueue=self.mEventQueue, theData=self.mData, activity_classes=activities)
        
        self.mContext = Context()
        logging.getLogger("scxml4py").info("Loading SCXML model") 
        self.mModel = Reader().readString("modelName", scxml_doc_str, self.mActionMgr.getActions(), self.mActionMgr.getActivities())
        logging.getLogger("scxml4py").debug("Loaded SCXML model: " + scxml4py.helper.formatModel(self.mModel))
        self.mExecutor = Executor(self.mModel, self.mContext)
        self.mExecutor.addStatusListener(self.mActionMgr.getAction("ActionStatus"))
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
            logging.getLogger("scxml4py").debug("Application received event = <" + theEvent.__str__() + ">")
            self.mExecutor.processEvent(theEvent)
            if theEvent.getId() == "_EXIT":
                logging.getLogger("scxml4py").debug("Application exiting...")
                self.mRunning = False
        logging.getLogger("scxml4py").info("Stopping execution of <" + self.mModel.getId() + ">")
        self.mExecutor.stop()
        logging.getLogger("scxml4py").info("Status: <" + scxml4py.helper.formatStatus(self.mExecutor.getStatus()) + ">")

class SCXML_Engine:
    def __init__(self, scxml_doc: str, actions, activities, data):
        self.doc = scxml_doc
        self.event_queue = Queue()
        self.data = data

        self.application = Application(self.doc, self.data, self.event_queue, actions, activities)

    def start(self):
        self.application.start()

    def terminate(self):
        self.event_queue.put(Event("_EXIT"), True, 2)
        self.application.join()

    def get_current_status(self):
        return scxml4py.helper.formatStatus(self.application.mExecutor.getStatus())

    def send_signal(self, signal_name:str, rtc_block:bool=True):
        self.event_queue.put(Event(signal_name), rtc_block, 2)
