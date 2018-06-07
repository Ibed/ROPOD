from Controller import Trigger as t
from Platform import UnitTask as ut
import copy

class PlatformController(object):

    def __init__(self,worldModel,plan):
        """life cycle state machine with 3 states and a starting state"""
        self.controllerGraph = {'start':['start trigger'],'start trigger':['CS2'],
                                'CS1':['CT1','CT3'], 'CT1':['CS2'], 'CT3':['CS3'],
                                'CS2':['CT2','CT5'], 'CT2':['CS1'], 'CT5':['CS3'],
                                'CS3':['CT4','CT6'], 'CT4':['CS1'], 'CT6':['CS2']}
        """CS are the control states, CT are the control triggers"""
        self.stateDescriptions = {'CS1':'changing unit task',
                                  'CS2':'pausing',
                                  'CS3':'sending/updating unit tasks'}
        self.currentState = 'start'
        """current events are read of the platform/unit event stack in the world model"""
        self.worldModel = worldModel
        self.plan = plan

        self.triggerList = []
        self.triggerList.append(t.Trigger('start trigger', 'start', 'CS2'))
        self.triggerList.append(t.Trigger('CT1','CS1','CS2'))
        self.triggerList.append(t.Trigger('CT2','CS2','CS1'))
        self.triggerList.append(t.Trigger('CT3','CS1','CS3'))
        self.triggerList.append(t.Trigger('CT4','CS3','CS1'))
        self.triggerList.append(t.Trigger('CT5','CS2','CS3'))
        self.triggerList.append(t.Trigger('CT6','CS3','CS2'))

    def changeTriggerConditions(self,triggerLabel,triggerConditions):
        for trigger in self.triggerList:
            if trigger.label == triggerLabel:
                trigger.triggerConditions = triggerConditions

    def updatePlanState(self):
        """check the current plan state, if events on the event stack should trigger a state change, change state"""
        """put all events from platform and units together"""
        worldModelEvents = copy.deepcopy(self.worldModel.eventStack)
        for unit in self.worldModel.listOfUnits:
            unitEvents = copy.deepcopy(unit.WM.eventStack)
            worldModelEvents.extend(unitEvents)
        allEvents = worldModelEvents
        """look at current state, iterate corresponding triggers"""
        listOfStateTriggerLabels = self.plan.planGraph[self.plan.currentStateLabel]
        for possibleTriggerLabel in listOfStateTriggerLabels:
            for trigger in self.plan.triggerList:
                if trigger.label == possibleTriggerLabel:
                    """if trigger is triggered, change state"""
                    if trigger.isTriggered(allEvents):
                        self.plan.currentStateLabel = trigger.endNodeLabel
                        state = self.plan.returnState(self.plan.currentStateLabel)
                        print(self.worldModel.label,' - plan state: ',state.stateType,state.stateSubject)
                        return


    def updateControlState(self):
        """check the current plan state, if events on the event stack should trigger a state change, change state"""
        """put all events from platform and units together"""
        worldModelEvents = copy.deepcopy(self.worldModel.eventStack)
        for unit in self.worldModel.listOfUnits:
            unitEvents = copy.deepcopy(unit.WM.eventStack)
            worldModelEvents.extend(unitEvents)
        allEvents = worldModelEvents
        """look at current state, iterate corresponding triggers"""
        listOfStateTriggerLabels = self.controllerGraph[self.currentState]
        for possibleTriggerLabel in listOfStateTriggerLabels:
            for trigger in self.triggerList:
                if trigger.label == possibleTriggerLabel:
                    """if trigger is triggered, change state"""
                    if trigger.isTriggered(allEvents):
                        self.currentState = trigger.endNodeLabel
                        print(self.worldModel.label,' - control state: ',self.stateDescriptions[self.currentState])
                        return


    def executeControlState(self):
        """at the moment, only one task type exists"""
        if self.stateDescriptions[self.currentState] == 'pausing':
            return
        if self.stateDescriptions[self.currentState] == 'sending/updating unit tasks':
            for unit in self.worldModel.listOfUnits:
                targetArea = self.worldModel.targetArea
                task = ut.UnitTask(targetArea,self.worldModel.currentConfiguration)
                self.sendTask(unit, task)

    def sendTask(self,unit,task):
        unit.WM.task = task
