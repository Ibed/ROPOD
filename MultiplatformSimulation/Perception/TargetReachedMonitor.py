from Perception import Event as e
class TargetReachedMonitor(object):

    def __init__(self,worldModel):
        self.type = 'target reached'
        self.worldModel = worldModel
        self.previousState = None
        self.currentState = None
        self.worldModel.listOfMonitors.append(self)

    def isTargetReached(self):
        if not self.worldModel.targetArea == None:
            targetReached = (self.worldModel.currentArea.label == self.worldModel.targetArea.label)
            self.currentState = targetReached
            if not self.currentState == self.previousState:
                if targetReached:
                    for event in self.worldModel.eventStack:
                        if event.eventType == 'target reached' and event.eventSubject == self.worldModel.label:
                            self.worldModel.eventStack.remove(event)
                    event = e.Event('target reached',self.worldModel.label,targetReached)
                    self.worldModel.eventStack.append(event)
                    print(self.worldModel.label, ' - event: target area',self.worldModel.targetArea.label, 'reached')
                if not targetReached:
                    for event in self.worldModel.eventStack:
                        if event.eventType == 'target reached' and event.eventSubject == self.worldModel.label:
                            self.worldModel.eventStack.remove(event)
                    event = e.Event('target reached',self.worldModel.label,targetReached)
                    self.worldModel.eventStack.append(event)
                    print(self.worldModel.label, ' - event: target area',self.worldModel.targetArea.label, 'not yet reached')
        self.previousState = self.currentState