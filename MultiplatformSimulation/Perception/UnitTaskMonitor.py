from Perception import Event as e
from Platform import UnitTask as t

class UnitTaskMonitor(object):

    def __init__(self,worldModel):
        self.type = 'unit task'
        self.worldModel = worldModel
        self.previousState = t.UnitTask()
        self.currentState = t.UnitTask()
        self.worldModel.listOfMonitors.append(self)

    def isTaskNew(self):
        self.currentState = self.worldModel.task
        if not self.currentState == self.previousState:
            self.worldModel.eventStack.append(e.Event('task','new',True))
            print(self.worldModel.label,'- event: new task received')
        else:
            for event in self.worldModel.eventStack:
                if event.eventType == 'task':
                    self.worldModel.eventStack.remove(event)
        self.previousState = self.currentState