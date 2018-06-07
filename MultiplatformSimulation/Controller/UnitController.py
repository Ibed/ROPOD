import math
import copy
from Controller import Trigger as t

class UnitController(object):

    def __init__(self,worldModel,world, plan):
        """life cycle state machine with 2 states"""
        self.controllerGraph = {'CS1': ['CT1'], 'CT1': ['CS2'],
                                'CS2': ['CT2'], 'CT2': ['CS1'],}
        """CS are the control states, CT are the control triggers"""
        self.stateDescriptions = {'CS1': 'coasting',
                                  'CS2': 'running motion controller'}
        self.currentState = 'CS1'
        """current events are read of the platform/unit monitor stack"""
        self.currentEvents = []

        self.world = world
        self.worldModel = worldModel
        self.plan = plan
        self.ceCounter = 0

        self.triggerList = []
        self.triggerList.append(t.Trigger('start trigger', 'start', 'CS2'))
        self.triggerList.append(t.Trigger('CT1', 'CS1', 'CS2'))
        self.triggerList.append(t.Trigger('CT2', 'CS2', 'CS1'))


    def changeTriggerConditions(self,triggerLabel,triggerConditions):
        for trigger in self.triggerList:
            if trigger.label == triggerLabel:
                trigger.triggerConditions = triggerConditions

    def updatePlanState(self):
        """check the current plan state, if events on the event stack should trigger a state change, change state"""
        """put all events from platform and units together"""
        worldModelEvents = copy.deepcopy(self.worldModel.eventStack)
        platformEvents = copy.deepcopy(self.worldModel.platformEvents)
        worldModelEvents.extend(platformEvents)
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
        """put all events from platform and unit together"""
        worldModelEvents = copy.deepcopy(self.worldModel.eventStack)
        platformEvents = copy.deepcopy(self.worldModel.platformEvents)
        worldModelEvents.extend(platformEvents)
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
        if self.stateDescriptions[self.currentState] == 'coasting':
            self.pauseMotion()
        if self.stateDescriptions[self.currentState] == 'running motion controller':
            self.runMotionController()

    def determineTargetAreaDirection1(self):
        targetNodePosition = self.worldModel.targetArea.posRelToTopNode
        currentNodePosition = self.worldModel.currentArea.posRelToTopNode
        currentRelPosition = self.worldModel.measuredPositionRelToCurrentArea
        currentPosition = [0,0]
        currentPosition[0] = currentRelPosition[0] + currentNodePosition[0]
        currentPosition[1] = currentRelPosition[1] + currentNodePosition[1]
        relativeTargetPosition = [0,0]
        relativeTargetPosition[0] = targetNodePosition[0] - currentPosition[0]
        relativeTargetPosition[1] = targetNodePosition[1] - currentPosition[1]
        targetAreaDirection = math.atan2(relativeTargetPosition[1],relativeTargetPosition[0])
        return targetAreaDirection

    def determineTargetAreaDirection2(self):
        targetNodePosition = self.worldModel.taskAreas[1].posRelToTopNode
        currentNodePosition = self.worldModel.taskAreas[0].posRelToTopNode
        currentRelPosition = self.worldModel.measuredPositionRelToCurrentArea
        currentPosition = [0,0]
        currentPosition[0] = currentRelPosition[0] + currentNodePosition[0]
        currentPosition[1] = currentRelPosition[1] + currentNodePosition[1]
        relativeTargetPosition = [0,0]
        relativeTargetPosition[0] = targetNodePosition[0] - currentPosition[0]
        relativeTargetPosition[1] = targetNodePosition[1] - currentPosition[1]
        tolerance = self.worldModel.radius
        if (relativeTargetPosition[0] > 0
            and relativeTargetPosition[1] > - self.worldModel.taskAreas[1].yDim/2 + tolerance
            and relativeTargetPosition[1] < + self.worldModel.taskAreas[1].yDim/2 - tolerance):
            targetAreaDirection = 0
        elif (relativeTargetPosition[0] < 0
            and relativeTargetPosition[1] > - self.worldModel.taskAreas[1].yDim/2 + tolerance
            and relativeTargetPosition[1] < + self.worldModel.taskAreas[1].yDim/2 - tolerance):
            targetAreaDirection = math.pi
        elif (relativeTargetPosition[1] > 0
            and relativeTargetPosition[0] > - self.worldModel.taskAreas[1].xDim/2 + tolerance
            and relativeTargetPosition[0] < + self.worldModel.taskAreas[1].xDim/2 - tolerance):
            targetAreaDirection = math.pi/2
        elif (relativeTargetPosition[1] < 0
            and relativeTargetPosition[0] > - self.worldModel.taskAreas[1].xDim/2 + tolerance
            and relativeTargetPosition[0] < + self.worldModel.taskAreas[1].xDim/2 - tolerance):
            targetAreaDirection = 3*math.pi/2
        else:
            print("target area direction undetermined")
            targetAreaDirection = 0
        return targetAreaDirection

    def runMotionController(self):
        """motion controller algorithm, also limits force vector when max velocity is reached"""
        predictedConstraints = self.worldModel.predictedConstraints

        """1.1 if any violating predicted constraints, try to avoid or brake until halt"""
        if predictedConstraints:
            self.ceCounter +=1
            #print(self.ceCounter)
            rightConstraint = False
            leftConstraint = False
            middleConstraint = False
            for constraint in predictedConstraints:
                if constraint[0]>self.worldModel.radius/4:
                    rightConstraint = True
                if constraint[0]<-self.worldModel.radius/4:
                    leftConstraint = True
                if constraint[0]>-self.worldModel.radius/4 and constraint[0]<self.worldModel.radius/4:
                    middleConstraint = True
            if rightConstraint:
                desiredMotionDirection = self.worldModel.getDirection(self.worldModel.measuredSpeed) + math.pi / 2
            if leftConstraint:
                desiredMotionDirection = self.worldModel.getDirection(self.worldModel.measuredSpeed) - math.pi / 2
            if (leftConstraint and rightConstraint) or middleConstraint:
                desiredMotionDirection = self.worldModel.getDirection(self.worldModel.measuredSpeed)+math.pi

        """1.2 if there are no violating constraints, go to target area"""
        if not predictedConstraints:
            desiredMotionDirection = self.determineTargetAreaDirection2()
        desiredForceMagnitude = self.worldModel.maxOutputForceMagnitude
        forceVector = self.worldModel.getVector(desiredMotionDirection, desiredForceMagnitude)

        """2. limit driving force"""
        speedMagnitude = math.sqrt(math.pow(self.worldModel.measuredSpeed[0], 2)+
                                   math.pow(self.worldModel.measuredSpeed[1], 2))
        if speedMagnitude >= self.worldModel.nominalSpeedMagnitude:
            alpha = self.worldModel.getDirection(self.worldModel.measuredSpeed)
            beta = math.pi/2-(alpha-desiredMotionDirection)
            forceMag = desiredForceMagnitude*math.cos(beta)
            if forceMag < 0:
                forceVector = self.worldModel.getVector(alpha+math.pi/2,math.fabs(forceMag))
            elif forceMag > 0:
                forceVector = self.worldModel.getVector(alpha - math.pi / 2, math.fabs(forceMag))
            else:
                forceVector = [0,0]


        """3. Update unit driving force"""
        for unit in self.world.listOfUnits:
            if unit.label == self.worldModel.label and unit.platformLabel == self.worldModel.platformLabel:
                unit.drivingForce = forceVector

    def forceVectorLimiter(self):
        """limits force when velocity exceeds maximum"""

    def pauseMotion(self):
        for unit in self.world.listOfUnits:
            if unit.label == self.worldModel.label and unit.platformLabel == self.worldModel.platformLabel:
                    unit.drivingForce = [0,0]


