from Perception import Event as e
class LocationMonitor(object):

    def __init__(self,worldModel):
        self.type = 'location'
        self.worldModel = worldModel
        self.previousState = None
        self.currentState = None
        self.worldModel.listOfMonitors.append(self)

    def monitorLocation(self):
        """monitor platform current location in world model and throw event if it has changed"""
        self.currentState = self.worldModel.currentArea.label
        if not self.previousState == self.currentState:
            for event in self.worldModel.eventStack:
                if event.eventType == 'location':
                    self.worldModel.eventStack.remove(event)
            currentEvent = e.Event('location',self.worldModel.currentArea.label,self.worldModel.label)
            self.worldModel.eventStack.append(currentEvent)
            print(self.worldModel.label, ' - event: i am in area ', self.worldModel.currentArea.label)
        self.previousState = self.currentState



