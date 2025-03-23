'''
    testContext module part of scxml4py unit tests.
    
    @authors: landolfa
'''

import unittest
from scxml4py.context import Context
from scxml4py.event import Event
        
class TestContext(unittest.TestCase):

    def testContextName(self):
        ctx = Context()
        ctx.setName("myContext")
        assert(ctx.getName() == "myContext")

    def testContextSessionId(self):
        ctx = Context()
        ctx.setSessionId("mySessionId")
        assert(ctx.getSessionId() == "mySessionId")

    def testContextLastEvent(self):
        e1 = Event("event1")
        ctx = Context()
        ctx.setLastEvent(e1);
        assert(ctx.getLastEvent() == e1)
        assert(ctx.getLastEvent().getId() == "event1")
        
    def testContextAddElement(self):
        ctx = Context()
        ctx.addElement("element1", "testElement1")
        assert ctx.getElement("element1") == "testElement1"
        ctx.addElement("element2", "testElement2")
        assert ctx.getElement("element2") == "testElement2"

    def testContextDelElement(self):
        ctx = Context()
        ctx.addElement("element1", "testElement1")
        ctx.addElement("element2", "testElement2")
        ctx.delElement("element1")
        assert ctx.getElement("element1") == None
        assert ctx.getElement("element2") == "testElement2"

    def testContextGetNonExistigElement(self):
        ctx = Context()
        element = ctx.getElement("element3")
        assert(element == None)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
