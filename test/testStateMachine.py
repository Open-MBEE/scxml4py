'''
    testStateMachine module part of scxml4py unit tests.
    
    @authors: landolfa
'''

import unittest
from scxml4py.stateMachine import StateMachine
from scxml4py.state import StateCompound, StateAtomic, StateParallel

    
class TestStateMachine(unittest.TestCase):

    def testSMId(self):
        sm = StateMachine("MyStateMachine")
        assert(sm.getId()=="MyStateMachine")
        sm.setId("Pippo")
        assert(sm.getId()=="Pippo")

    def testSMSubstates(self):
        sm = StateMachine("MyStateMachine")
        s1 = StateCompound("S1")
        s11 = StateAtomic("S11")
        s12 = StateAtomic("S12")
        s1.addSubstate(s11)
        s1.addSubstate(s12)
        sm.addSubstate(s1)
        print(str(sm))

    def testSMInitialTrans(self):
        sm = StateMachine("MyStateMachine")
        s1 = StateCompound("S1")
        sm.addSubstate(s1)
        sm.setInitialState(s1)
        print(str(sm))
        
    def testSMClone1(self):
        sm = StateMachine("MyStateMachine")
        p = StateParallel("P")
        a = StateCompound("A")
        b = StateAtomic("B")
        c = StateAtomic("C")
        a.addSubstate(b)
        a.addSubstate(c)
        p.addSubstate(a)
        p.resolveAbsoluteId()
        a.resolveAbsoluteId()
        b.resolveAbsoluteId()
        c.resolveAbsoluteId()
        sm.addParallel(p)
        sm.updateStatesMap(p.getAbsoluteId(), p)
        sm.updateStatesMap(a.getAbsoluteId(), a)
        sm.updateStatesMap(b.getAbsoluteId(), b)
        sm.updateStatesMap(c.getAbsoluteId(), c)
        print(str(sm))
        print(sm.mStatesMap)
        sm.setId("ClonedStateMachine")
        sm.cloneParallel(2, "P", {}, {})
        assert(len(sm.mStatesMap) == 10)
        assert("P" in sm.mStatesMap.keys())
        assert("P.A" in sm.mStatesMap.keys())
        assert("P.A.B" in sm.mStatesMap.keys())
        assert("P.A.C" in sm.mStatesMap.keys())
        assert("P.A1" in sm.mStatesMap.keys())
        assert("P.A1.B1" in sm.mStatesMap.keys())
        assert("P.A1.C1" in sm.mStatesMap.keys())
        assert("P.A2" in sm.mStatesMap.keys())
        assert("P.A2.B2" in sm.mStatesMap.keys())
        assert("P.A2.C2" in sm.mStatesMap.keys())
        print(str(sm))
        print(sm.mStatesMap)

    def testSMClone2(self):
        sm = StateMachine("MyStateMachine2")
        a = StateCompound("A")
        p = StateParallel("P")
        b = StateAtomic("B")
        a.addSubstate(p)
        p.addSubstate(b)        
        p.resolveAbsoluteId()
        a.resolveAbsoluteId()
        b.resolveAbsoluteId()
        sm.addSubstate(a)
        sm.updateStatesMap(p.getAbsoluteId(), p)
        sm.updateStatesMap(a.getAbsoluteId(), a)
        sm.updateStatesMap(b.getAbsoluteId(), b)
        print(str(sm))
        print(sm.updateStatesMap)
        sm.setId("ClonedStateMachine2")
        sm.cloneParallel(3, "A.P", {}, {})
        assert(len(sm.mStatesMap) == 6)
        assert("A" in sm.mStatesMap.keys())
        assert("A.P" in sm.mStatesMap.keys())
        assert("A.P.B" in sm.mStatesMap.keys())
        assert("A.P.B1" in sm.mStatesMap.keys())
        assert("A.P.B2" in sm.mStatesMap.keys())
        assert("A.P.B3" in sm.mStatesMap.keys())
        print(str(sm))
        print(sm.mStatesMap)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

