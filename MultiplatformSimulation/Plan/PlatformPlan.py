from Controller import Trigger as t
from Plan import State as s

class PlatformPlan(object):

    def __init__(self):
        self.planGraph = {}
        self.currentStateLabel = None
        self.triggerList = []
        self.stateList = []

    def addState(self, stateLabel, stateType, stateSubject):
        self.planGraph[stateLabel] = []
        state = s.State(stateLabel,stateType,stateSubject)
        self.stateList.append(state)

    def addTrigger(self,label,startNode,endNode,triggerConditions = [[]]):
        trigger = t.Trigger(label,startNode,endNode,triggerConditions)
        self.triggerList.append(trigger)
        self.planGraph[startNode].append(label)
        self.planGraph[label]=[endNode]
        state = self.returnState(startNode)
        state.listOfTriggers.append(trigger)

    def returnState(self,stateLabel):
        for state in self.stateList:
            if state.label == stateLabel:
                return state

    def determineAreasToBeMonitored(self):
        currentState = self.returnState(self.currentStateLabel)
        areasToBeMonitored = []
        if not currentState.stateSubject == None:
            areasToBeMonitored.append(currentState.stateSubject)
            for trigger in currentState.listOfTriggers:
                neighborState = self.returnState(trigger.endNodeLabel)
                if not neighborState.stateSubject == currentState.stateSubject:
                    areasToBeMonitored.append(neighborState.stateSubject)
        return areasToBeMonitored

    def updateTargetArea(self,worldModel):
        currentState = self.returnState(self.currentStateLabel)
        if currentState.stateType == 'going to':
            targetArea = worldModel.returnArea(currentState.stateSubject)
            worldModel.targetArea = targetArea