'''
    testAction module part of scxml4py unit tests.
    
    @authors: landolfa
'''

import logging
import unittest
from scxml4py.action import Action
from scxml4py.context import Context

class CustomAction1(Action):
    def __init__(self, theId):
        Action.__init__(self, theId)
        
    def evaluate(self, theContext):
        return False    

    def execute(self, theContext):
        # do something useful
        logging.getLogger('scxml4py').info(self.getId())    


class CustomAction2(Action):
    def __init__(self):
        Action.__init__(self, "CustomAction2")
        
    def evaluate(self, theContext):
        return True

    def execute(self, theContext):
        # do something useful
        logging.getLogger('scxml4py').info(self.getId())    
        
class TestAction(unittest.TestCase):


    def testActionId(self):
        a1 = CustomAction1("CustomAction1")
        assert(a1.getId()=="CustomAction1")
        a1.setId("Pippo")
        assert(a1.getId()=="Pippo")
        a2 = CustomAction2()
        assert(a2.getId()=="CustomAction2")
        
    def testActionEvaluate(self):
        ctx = Context()
        a1 = CustomAction1("CustomAction1")
        assert(a1.evaluate(ctx) == False)
        a2 = CustomAction2()
        assert(a2.evaluate(ctx) == True)
        
    def testActionCompare(self):
        a11 = Action("a11")
        a111 = Action("a111")
        assert(a11 == a11)
        assert(a11 != a111)
        assert(a11 < a111)
        assert(a111 > a11)
        assert(None < a11)
        assert(a11 != None)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    