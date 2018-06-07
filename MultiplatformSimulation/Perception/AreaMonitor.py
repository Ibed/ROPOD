from Perception import Event as e
class AreaMonitor(object):
    def __init__(self, worldModel):
        self.type = 'area'
        self.worldModel = worldModel
        self.worldModel.listOfMonitors.append(self)

    def monitorTargetAreas(self,areasToBeMonitored):
        """check platform WM target areas and put event on the event stack if it has changed"""
        for areaLabel in areasToBeMonitored:
            area = self.worldModel.returnArea(areaLabel)
            if area.isAvailable:
                area.currentState = (area.label,'available')
            else:
                area.currentState = (area.label,'unavailable')
            if not area.previousState == area.currentState:
                if (area.isAvailable == False):
                    for event in self.worldModel.eventStack:
                        if event.eventType == 'area' and event.eventSubject == area.label and event.eventMessage == 'available':
                            self.worldModel.eventStack.remove(event)
                    currentEvent = e.Event('area',area.label,'unavailable')
                    self.worldModel.eventStack.append(currentEvent)
                    print(self.worldModel.label,' - event: area ',area.label,'unavailable')
                if (area.isAvailable == True):
                    for event in self.worldModel.eventStack:
                        if event.eventType == 'area' and event.eventSubject == area.label and event.eventMessage == 'unavailable':
                            self.worldModel.eventStack.remove(event)
                    currentEvent = e.Event('area', area.label, 'available')
                    self.worldModel.eventStack.append(currentEvent)
                    print(self.worldModel.label, ' - event: area ', area.label, 'available')
            area.previousState = area.currentState
