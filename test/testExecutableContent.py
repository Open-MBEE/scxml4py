'''
    testExecutableContent module part of scxml4py unit tests.
    
    @authors: landolfa
'''
 
import logging
import unittest
from scxml4py.action import Action
from scxml4py.context import Context
from scxml4py.executableContent import ExecutableContent
 
class CustomAction1(Action):
    def __init__(self, theId):
        Action.__init__(self, theId)        
    def evaluate(self, theContext):
        return True
    def execute(self, theContext):
        # do something useful
        logging.getLogger('scxml4py').info("Execute action: " + self.getId())    


class CustomAction2(Action):
    def __init__(self):
        Action.__init__(self, "CustomAction2")
    def evaluate(self, theContext):
        return False
    def execute(self, theContext):
        # do something useful
        logging.getLogger('scxml4py').info("Execute action: " + self.getId())    

class TestExecutableContent(unittest.TestCase):

    def testEvaluateTwoAction(self):
        ctx = Context()
        a1 = CustomAction1("CustomAction1")
        a2 = CustomAction2()
        execContent = ExecutableContent()
        execContent.addAction(a1)
        execContent.addAction(a2)
        assert(execContent.evaluate(ctx) == False)

    def testExecuteTwoAction(self):
        ctx = Context()
        a1 = CustomAction1("CustomAction1")
        a2 = CustomAction2()
        execContent = ExecutableContent()
        execContent.addAction(a1)
        execContent.addAction(a2)
        execContent.execute(ctx);
        
    def testCompare(self):
        a1 = Action("a1")
        a2 = Action("a2")
        execContent1 = ExecutableContent()
        execContent1.addAction(a1)
        execContent2 = ExecutableContent()
        execContent2.addAction(a1)        
        execContent2.addAction(a2)
        assert(execContent1 == execContent1)
        assert(execContent1 != execContent2)
        assert(execContent1 != None)
        assert(None != execContent1)
        assert(execContent1 < execContent2)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()