'''
    listeners module part of scxml4py.
    
    @authors: landolfa
'''

class EventListener(object):
    
    def notify(self, event):
        pass


class StatusListener(object):
    
    def notify(self, status):
        pass
