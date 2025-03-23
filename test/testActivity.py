'''
    testActivity module part of scxml4py unit tests.
    
    @authors: landolfa
'''
import asyncio
import unittest
import time
from scxml4py.activity import AbstractActivity
from scxml4py.activity import ThreadedActivity, CoroActivity

class CustomActivity(AbstractActivity): 
    def run(self):
        while self.isRunning():
            self.sleep(1)

class CustomCoroActivity(CoroActivity):
    def __init__(self):
        super(CustomCoroActivity, self).__init__("ID")
        self.sig = False

    async def run(self):
        self.sig = True


class TestThreadedActivity(unittest.TestCase):

    def testActivityId(self):
        a1 = CustomActivity("CustomActivity")

        self.assertEqual("CustomActivity", a1.getId())
        a1.setId("Pippo")

        self.assertEqual("Pippo", a1.getId())

    def testActivityStartAndStop(self):
        a1 = ThreadedActivity("CustomActivity")
        self.assertFalse(a1.isRunning())
        for i in range(10):
            #print(i);
            a1.start()
            self.assertTrue(a1.isRunning())
            a1.stop()
            self.assertFalse(a1.mThread.isAlive())

            
class TestCoroActivity(unittest.TestCase):
        
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def tearDown(self):
        self.loop.close()

    def test_activity_should_start_and_stop(self):
        activity = CustomCoroActivity()

        self.assertFalse(activity.isRunning())
        # schedule activity to run
        activity.start()
        self.assertTrue(activity.isRunning())

        # "run" the task manually since we don't actually have an eventloop
        # running.
        self.loop.run_until_complete(asyncio.wait_for(activity.mTask, 0.5))
        
        # Stop coroutine
        activity.stop() 
        self.assertFalse(activity.isRunning())

        # Assert that the activity has been running
        self.assertTrue(activity.sig)
 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
