import logging
import threading
from queue import Queue

import scxml4py.helper
from scxml4py.reader import Reader
from scxml4py.context import Context
from scxml4py.event import Event
from scxml4py.executor import Executor
from scxml4py.listeners import EventListener
from scxml4py.action import Action
from scxml4py.listeners import StatusListener

from scxmlApp.actionmgr import ActionMgr

# Installed as status listener, engine looks for "ActionStatus" action
class _ActionStatus(Action, StatusListener):
    # implemented by the developer, stub can be generated
    def __init__(self, theData, theActionMgr):
        Action.__init__(self, "ActionStatus", None, theData)
        self.mStatus = None
        self.mActionMgr = theActionMgr
    
    def notify(self, status):
        self.mStatus = status
        userActionStatus = self.mActionMgr.getAction("ActionStatusListener")
        if userActionStatus is not None:
            logging.getLogger("scxmlApp").debug (">>>>>>>>>>>>>>>>>>>>>>>>>>>userActionStatus found")    
            userActionStatus.execute(status)
        logging.getLogger("scxmlApp").info(">>>>_ActionStatus::notify Status: <" + scxml4py.helper.formatStatus(self.mStatus) + ">")
    
    # why do I need this?
    def execute(self, theCtx):
        logging.getLogger("scxmlApp").info(">>>>_ActionStatus::execute Status: <" + scxml4py.helper.formatStatus(self.mStatus) + ">")


class _EventListener(EventListener):
    def __init__(self, theData, callback, theActionMgr):
        self.mEvent = None
        self.callback = callback
        self.theData = theData
        self.mActionMgr = theActionMgr
    
    def notify(self, event):
        self.mEvent = event
        self.callback()
        userActionEvent = self.mActionMgr.getAction("ActionEventListener")
        if userActionEvent is not None:
            logging.getLogger("scxmlApp").debug (">>>>>>>>>>>>>>>>>>>>>>>>>>>userActionEvent found")    
            userActionEvent.execute(event)
        logging.getLogger("scxmlApp").info(">>>>_EventListener::notify EventListener: <" + ">")
        logging.getLogger("scxmlApp").debug(event.getStatus())


class _Application(threading.Thread):   
    def __init__(self, theScxmlDoc:str, data, theEventQueue, actions, activities):
        threading.Thread.__init__(self)
        self.mRunning = False
        self.mEventQueue = theEventQueue
        self.mData = data
        self._event = threading.Event()
        
        self.mActionMgr = ActionMgr()
        self.mActionMgr.createActions(theData=self.mData, action_classes=actions)
        self.mActionMgr.createActivities(theEventQueue=self.mEventQueue, theData=self.mData, activity_classes=activities)
        
        self.mContext = Context()
        logging.getLogger("scxmlApp").info("_Application::Loading SCXML model") 
        self.mModel = Reader().readString("modelName", theScxmlDoc, self.mActionMgr.getActions(), self.mActionMgr.getActivities())
        logging.getLogger("scxmlApp").debug("_Application::Loaded SCXML model: " + scxml4py.helper.formatModel(self.mModel))
        self.mExecutor = Executor(self.mModel, self.mContext)
        self.mActionStatus = _ActionStatus(theData=self.mData, theActionMgr = self.mActionMgr)
        self.mEventListener = _EventListener(theData=self.mData, callback=self.event_callback, theActionMgr = self.mActionMgr)
        self.mExecutor.addStatusListener(self.mActionStatus)
        self.mExecutor.addEventListener(self.mEventListener)
        logging.getLogger("scxmlApp").info("_Application::Status: <" + scxml4py.helper.formatStatus(self.mExecutor.getStatus()) + ">")
        
    def run(self):
        logging.getLogger("scxmlApp").info("_Application::Starting execution of <" + self.mModel.getId() + ">")
        self.mRunning = True
        self.mExecutor.start()
        logging.getLogger("scxmlApp").info("_Application::Status: <" + scxml4py.helper.formatStatus(self.mExecutor.getStatus()) + ">")
        while self.mRunning == True:
            theEvent = self.mEventQueue.get(True, None)
            #Queue().get(block, timeout)
            # loop on the event queue send the event to the SM engine
            logging.getLogger("scxmlApp").debug("_Application::Application received event = <" + theEvent.__str__() + ">")
            self.mExecutor.processEvent(theEvent)
            if theEvent.getId() == "_EXIT":
                logging.getLogger("scxmlApp").debug("_Application::Application exiting...")
                self.mRunning = False
        logging.getLogger("scxmlApp").info("_Application::Stopping execution of <" + self.mModel.getId() + ">")
        self.mExecutor.stop()
        logging.getLogger("scxmlApp").info("_Application::Status: <" + scxml4py.helper.formatStatus(self.mExecutor.getStatus()) + ">")

    def event_callback(self):
        self._event.set()  # unblock the waiting method

    def wait_for_event(self):
        self._event.wait()  # this blocks until .set() is called

class Application:
    def __init__(self, scxmlDoc: str, actions, activities, data):
        self.doc = scxmlDoc
        self.event_queue = Queue()
        self.data = data

        self.application = _Application(self.doc, self.data, self.event_queue, actions, activities)

    def start(self):
        self.application.start()

    def terminate(self):
        self.event_queue.put(Event("_EXIT"), True, 2)
        self.application.wait_for_event()
        self.application.join()

    def get_current_status(self):
        return scxml4py.helper.formatStatus(self.application.mExecutor.getStatus())

    def send_signal(self, signal_name:str, sync:bool=True, rtc_block:bool=True):
        self.event_queue.put(Event(signal_name), sync, 2)
        if rtc_block:
            self.application.wait_for_event()

