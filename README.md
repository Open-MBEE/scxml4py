# scxml4py

`scxml4py` is a Python implementation of an SCXML (State Chart XML) interpreter with a programmatic API.  
It allows you to execute SCXML documents, interact with the state machine during runtime, and hook into state transitions and events — making it useful for animations, simulations, or embedded reactive systems.

---

## ✨ Features

- ✅ Execute SCXML state machines in Python
- ✅ Control the state machine via a simple API
- ✅ Register custom actions and activities
- ✅ Hook into state changes and events with listeners (great for visualizations or UI feedback)
- ✅ Clean architecture for integration into your systems

---

## 🚀 Quick Start

```python
import logging
import time

import scxml4py.helper
from scxml4py.engine import SCXML_Engine
from scxml4py.action import Action
from scxml4py.activity import ThreadedActivity
from scxml4py.event import Event

class ActivityOnline(ThreadedActivity):
    # implemented by the developer, stub can be generated
    def __init__(self, theEventQueue, theData):
        ThreadedActivity.__init__(self, "ActivityOnline", theEventQueue, theData)

    def run(self):
        counter = 0
        while self.isRunning() == True:
            logging.getLogger("scxml4py").info("Activity <" + self.getId() + "> is running...")
            time.sleep(1)
            counter += 1
            if counter == 5:
                self.sendInternalEvent(Event("GoOffline"))
                self.setRunning(False)
                break
            
class Data(object):
    # implemented by the developer
    # data shared between actions and activities
    def __init__(self):
        self.mSharedInfo = None
    
    def getSharedInfo(self):
        # requires mutex
        return self.mSharedInfo
    
    def setSharedInfo(self, sharedInfo):
        # requires mutex
        self.mSharedInfo = sharedInfo

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

# SCXML source and data setup
simple_sm_data = Data()
simple_sm = SCXML_Engine(
    simpleSM_string, 
    actions=[ActionStatus], 
    activities=[ActivityOnline], 
    data=simple_sm_data
)

# Start the state machine
simple_sm.start()

# Interact with it
simple_sm.send_signal("GoOnline", True)
status = simple_sm.get_current_status()

simple_sm.send_signal("GoOffline", True)
status = simple_sm.get_current_status()

print(">>>>>>", status)

# Clean termination
simple_sm.terminate()
```

---

## 🔌 Extensibility

You can define your own `Action` and `Activity` classes to extend behavior. These can interact with the SCXML runtime and external systems.

### Example: Custom Action

```python
class ActionStatus(Action):
    def __init__(self, data):
        self.data = data

    def execute(self):
        print("Status Action Executed")
```

---

## 🎯 Use Cases

- Simulation engines with event-driven state models
- GUI applications with animated state transitions
- Lightweight embedded state machines in Python systems
- Robotics or IoT orchestration using reactive logic

---

## 🔍 Listeners

You can register listeners on:

- **State configuration changes**
- **Events triggered during execution**

This makes it ideal for visualizing execution or syncing with front-end UIs.

---

## 📦 Installation

Clone and install in editable mode:

```bash
git clone https://github.com/openmbee/scxml4py.git
cd scxml4py
pip install -e .
```

---

## 🧩 Requirements

- Python 3.10+
- No external dependencies beyond the standard library

---

## References
Visual SCXML Editor for VsCode: https://marketplace.visualstudio.com/items?itemName=Phrogz.visual-scxml-editor

---

## 📄 License

APACHE 2.0 License © 2024 Luigi Andolfato, Robert Karban


## 📚 SCXML_Engine API

The `SCXML_Engine` class provides a high-level API to load, execute, and interact with SCXML state machines.

---

### 🔹 `SCXML_Engine(scxml_doc: str, actions, activities, data)`

#### **Constructor**
Initializes the SCXML engine with a state machine definition and supporting elements.

| Parameter     | Type      | Description |
|---------------|-----------|-------------|
| `scxml_doc`   | `str`     | The SCXML document as a string. |
| `actions`     | `list`    | List of `Action` classes to be instantiated and injected. |
| `activities`  | `list`    | List of `Activity` classes to be instantiated and injected. |
| `data`        | `Data`    | Shared data object passed to actions and activities. |

#### **Example**
```python
engine = SCXML_Engine(
    scxml_doc=some_scxml_string,
    actions=[ActionStatus],
    activities=[ActivityOnline],
    data=my_data
)
```

---

### 🔹 `start()`

Starts the SCXML interpreter in a background thread.

```python
engine.start()
```

---

### 🔹 `terminate()`

Gracefully terminates the interpreter by sending an `_EXIT` signal and waiting for the interpreter to shut down.

```python
engine.terminate()
```

---

### 🔹 `send_signal(signal_name: str, rtc_block: bool = True)`

Sends an external event (signal) into the state machine.

| Parameter       | Type    | Description |
|-----------------|---------|-------------|
| `signal_name`   | `str`   | The name of the event to trigger. |
| `rtc_block`     | `bool`  | Whether to block the call for RTC (default: `True`). |

```python
engine.send_signal("GoOnline")
```

---

### 🔹 `get_current_status() → str`

Returns a human-readable summary of the current active states.

```python
status = engine.get_current_status()
print(status)
```
---

## ⚙️ Extending Behavior with Actions & Activities

To inject custom behavior into your state machine, subclass the `Action` or `Activity` base classes and register them during engine initialization.

---

### 🔹 `class Action`

Base class for actions executed during SCXML transitions or states.

#### 🔧 Subclass Responsibilities
You must implement the `execute()` method.

#### 🔹 `def execute(self)`

Called when the SCXML interpreter executes this action (e.g., during a `<onentry>` or `<transition>`).

#### ✅ Example:

```python
from scxml4py import Action

class ActionStatus(Action):
    def __init__(self, data):
        self.data = data

    def execute(self):
        print("Executing status check")
```

Pass it to the engine:

```python
engine = SCXML_Engine(scxml_doc, actions=[ActionStatus], activities=[], data=my_data)
```

---

### 🔹 `class Activity`

Base class for activities that run concurrently during active states (like `<invoke>` in SCXML). Activities run in their own threads.

#### 🔧 Subclass Responsibilities
You must implement the `run()` method.

#### 🔹 `def run(self)`

This method is executed in a separate thread when the activity is started by the SCXML interpreter. Use it to perform asynchronous or ongoing work.

#### ✅ Example:

```python
from scxml4py import Activity

class ActivityOnline(ThreadedActivity):
    def __init__(self, event_queue, data):
        self.event_queue = event_queue
        self.data = data

    def run(self):
        print("Activity started")
        # Optionally send events to the state machine
        self.event_queue.put(Event("SomeInternalEvent"))
```

Register the activity:

```python
engine = SCXML_Engine(scxml_doc, actions=[], activities=[ActivityOnline], data=my_data)
```

---

### 💡 Use Case Summary

| Interface | Runs When               | Use Case                                |
|-----------|-------------------------|------------------------------------------|
| `Action`  | On state transitions    | Trigger logic during events             |
| `Activity`| While state is active   | Run background tasks, pollers, workers  |


```


