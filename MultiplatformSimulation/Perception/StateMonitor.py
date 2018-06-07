from Perception import Event as e
class StateMonitor(object):
    def __init__(self, worldModel, plan):
        self.type = 'state'
        self.worldModel = worldModel
        self.plan = plan
        self.previousState = None
        self.currentState = None
        self.worldModel.listOfMonitors.append(self)

    def monitorPlanState(self):
        """check current plan state, announce type if changed"""
        state = self.plan.returnState(self.plan.currentStateLabel)
        self.currentState = state.stateType
        if not self.previousState == self.currentState:
            for event in self.worldModel.eventStack:
                if event.eventType == 'plan state type':
                    self.worldModel.eventStack.remove(event)
            event = e.Event('plan state type',self.worldModel.label,state.stateType)
            self.worldModel.eventStack.append(event)
            print(self.worldModel.label,' - event:',event.eventSubject,'state type has changed to *',state.stateType,'*')
        self.previousState = self.currentState