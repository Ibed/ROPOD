from Perception import Event as e
class ConstraintMonitor(object):

    def __init__(self,worldModel):
        self.type = 'constraint'
        self.worldModel = worldModel
        self.previousState = False
        self.currentState = False
        self.worldModel.listOfMonitors.append(self)

    def monitorConstraints(self):
        """monitor unit constraints. If constraint is about to be violated, throw event"""
        self.currentState = self.worldModel.constraintViolationPredicted
        if not self.previousState == self.currentState:
            for event in self.worldModel.eventStack:
                if event.eventType == 'constraint':
                    self.worldModel.eventStack.remove(event)
            if self.currentState:
                currentEvent = e.Event('constraint', self.worldModel.label, True)
                self.worldModel.eventStack.append(currentEvent)
                print(self.worldModel.label, ' - event: constraint violation predicted ')
            if not self.currentState:
                currentEvent = e.Event('constraint', self.worldModel.label, False)
                self.worldModel.eventStack.append(currentEvent)
        self.previousState = self.currentState



