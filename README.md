scxml4py
========

`scxml4py` is a Python implementation of an SCXML (State Chart XML) interpreter with a programmatic API.  
It allows execution of SCXML documents and interaction with the interpreter at runtime through a clean, flexible API. The framework is designed for applications such as simulations, reactive systems, robotics, and UI-driven state animations.

---

Features
--------

- ✅ Execute SCXML state machines in Python
- ✅ Control the interpreter at runtime through a Python API
- ✅ Register custom `Action` and `Activity` classes
- ✅ Listen to state configuration changes and event dispatches
- ✅ Shared Python `Data` object for interaction between actions and activities
- ✅ Simple threading model for concurrent behaviors

---

Example
-------

```python
import logging
import time

import scxml4py.helper
from scxmlApp.application import Application
from scxml4py.action import Action
from scxml4py.activity import ThreadedActivity
from scxml4py.event import Event

class ActionStatusListener(Action):
    def __init__(self, theData):
        super().__init__("ActionStatusListener", None, theData)

    def execute(self, status):
        # This method is executed when the SCXML engine executes the Status action.
        # Its exact invocation depends on your SCXML model.
        # For example, it can be bound to a <transition>, <onentry>, or <onexit> element.
        # In your model, this action is triggered by an internal transition on the "Status" event.
        logging.getLogger("scxml4py").info(
            ">>>>ActionStatusListener::nb Status: <" + scxml4py.helper.formatStatus(status) + ">"
        )

class ActionEventListener(Action):
    def __init__(self, theData):
        super().__init__("ActionEventListener", None, theData)

    def execute(self, event):
        logging.getLogger("scxml4py").info(">>>>ActionEventListener::nb Event received")
        print(event.getStatus())

class ActivityOnline(ThreadedActivity):
    def __init__(self, theEventQueue, theData):
        super().__init__("ActivityOnline", theEventQueue, theData)

    def run(self):
        counter = 0
        while self.isRunning():
            logging.getLogger("scxml4py").info("Activity <" + self.getId() + "> is running...")
            time.sleep(1)
            counter += 1
            if counter == 5:
                self.sendInternalEvent(Event("GoOffline"))
                self.setRunning(False)

class Data:
    def __init__(self):
        self.mSharedInfo = None

    def getSharedInfo(self):
        return self.mSharedInfo

    def setSharedInfo(self, sharedInfo):
        self.mSharedInfo = sharedInfo

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(threadName)s - %(module)s - %(funcName)s - %(message)s',
    level=logging.DEBUG
)

simpleSM_string = '''<?xml version="1.0" ?>
<scxml xmlns="http://www.w3.org/2005/07/scxml" version="1.0" datamodel="ecmascript" initial="OFF">
  <state id="OFF">
    <transition event="GoOnline" target="ONLINE"/>
  </state>
  <state id="ONLINE">
    <transition event="GoOffline" target="OFF"/>
    <invoke id="ActivityOnline"/>  	
  </state>
</scxml>'''

simple_sm_data = Data()
simple_sm = Application(
    scxmlDoc=simpleSM_string,
    actions=[ActionStatusListener, ActionEventListener],
    activities=[ActivityOnline],
    data=simple_sm_data
)

simple_sm.start()
simple_sm.send_signal("GoOnline", rtc_block=True)
print(">>>>>>", simple_sm.get_current_status())
time.sleep(10)
simple_sm.send_signal("GoOffline", rtc_block=True)
print(">>>>>>", simple_sm.get_current_status())
simple_sm.terminate()
```

---

Listener Interfaces
-------------------

To respond to state changes and events during execution, implement listener interfaces:

- `StatusListener`: receives current state configuration updates.
- `EventListener`: receives dispatched events.

These can be combined with actions. For example:

```python
class ActionStatus(Action, StatusListener, EventListener):
    def notify(self, update):
        print("Received update:", update)
```

---

Note on Data Model
------------------

The SCXML `<data>` model is **not implemented**. Instead, a custom Python `Data` class is used to store and share state among `Action` and `Activity` instances.

---

Application API
---------------

### `Application(scxmlDoc: str, actions, activities, data)`

| Parameter    | Type      | Description |
|--------------|-----------|-------------|
| `scxmlDoc`   | `str`     | The SCXML document as a string |
| `actions`    | `list`    | List of `Action` classes to instantiate |
| `activities` | `list`    | List of `Activity` classes to instantiate |
| `data`       | `object`  | Shared Python data object |

### `start()`
Starts the interpreter in a background thread.

### `terminate()`
Stops the interpreter by sending an `_EXIT` event and waiting for all threads to finish.

### `send_signal(signal_name: str, sync: bool = True, rtc_block: bool = True)`
Sends an external event (signal) to the state machine.

- `sync`: if `True`, the event is synchronized.
- `rtc_block`: if `True`, waits until the SCXML engine finishes processing the event.

### `get_current_status() -> str`
Returns a human-readable string showing the currently active state(s).

---

Writing Actions & Activities
----------------------------

### `class Action`

Subclass and implement:

```python
def execute(self):
    pass
```

The `execute()` method is called when your action is triggered by SCXML elements:
- `<transition>` → when the event occurs
- `<onentry>` / `<onexit>` → when entering/exiting a state
- Internal transitions (e.g., the `Status` event in your model)

### `class ThreadedActivity`

Subclass and implement:

```python
def run(self):
    while self.isRunning():
        ...
```

Send events from within the activity:

```python
self.sendInternalEvent(Event("EventName"))
```

---

Installation
------------

```bash
git clone https://github.com/openmbee/scxml4py.git
cd scxml4py
pip install -e .
```

---

Requirements
------------

- Python 3.10+
- No third-party dependencies

---

Related Tools
-------------

- [Visual SCXML Editor for VSCode](https://marketplace.visualstudio.com/items?itemName=Phrogz.visual-scxml-editor)

---

License
-------

Apache 2.0 License © 2024 Luigi Andolfato, Robert Karban

