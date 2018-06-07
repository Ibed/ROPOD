from WorldModel import UnitWM as w
from Controller import UnitController as c
from Plan import UnitPlan as p
from Perception import UnitPerception as pe
from Perception import LocationMonitor as lm
from Perception import StateMonitor as sm
from Perception import TargetReachedMonitor as trm
from Perception import UnitTaskMonitor as utm
from Perception import ConstraintMonitor as cm
from Perception import Event as e

class Unit(object):

    def __init__(self, platformLabel, label, mass, radius,posRelToStartingArea, startingArea, areaList,env, world):
        self.label = label
        self.platformLabel = platformLabel
        self.WM = w.UnitWM(platformLabel, label,mass,radius,posRelToStartingArea,startingArea,areaList)
        self.perception = pe.UnitPerception(world, self.WM)
        self.plan = p.UnitPlan()
        self.controller = c.UnitController(self.WM, world, self.plan)

        """these physical parameters are in reference to the world frame, not the local area frame of the WM.
        They are used by the world class as opposed to the variables in the WM's"""
        self.actualSpeed = [0,0]
        self.actualAcceleration = [0,0]
        self.externalForceOnUnit = [0,0]
        self.drivingForce = [0,0]
        self.totalForceOnUnit = [0,0]
        self.actualPosition = [0,0]
        self.actualPosition[0] = startingArea.posRelToTopNode[0] + posRelToStartingArea[0]
        self.actualPosition[1] = startingArea.posRelToTopNode[1] + posRelToStartingArea[1]
        self.distanceTravelled = 0
        self.mass = mass
        self.radius = radius
        self.dragMagnitude = 2

        self.world = world
        self.env = env
        self.action = env.process(self.run())

    def run(self):
        """gets called when initialised"""
        """1. create monitors"""
        locationMonitor = lm.LocationMonitor(self.WM)
        stateMonitor = sm.StateMonitor(self.WM,self.plan)
        targetReachedMonitor = trm.TargetReachedMonitor(self.WM)
        unitTaskMonitor = utm.UnitTaskMonitor(self.WM)
        constraintMonitor = cm.ConstraintMonitor(self.WM)

        """2. create plan based on task type (atm only one type of task exists)"""
        self.plan.addState('start', None, None)
        self.plan.addState('PS1','waiting in','current area')
        self.plan.addState('PS2', 'going to', 'target area')
        self.plan.currentStateLabel = 'start'

        self.plan.addTrigger('start trigger', 'start', 'PS1', [[e.Event('location', self.WM.currentArea.label, self.label)]])
        self.plan.addTrigger('PT1','PS1','PS2',[[e.Event('task','new',True)]])
        self.plan.addTrigger('PT2', 'PS2', 'PS1', [[e.Event('target reached', self.label, True)]])

        """3. decide controller state triggers"""
        self.controller.changeTriggerConditions('CT1', [[e.Event('plan state type', self.label, 'going to'),e.Event('constraint',self.WM.label,True)]])
        self.controller.changeTriggerConditions('CT2', [[e.Event('plan state type', self.label, 'waiting in')],[e.Event('constraint',self.WM.label,False)]])
        self.controller.changeTriggerConditions('start trigger',[[e.Event('location', self.WM.currentArea.label, self.label)]])
        while True:
            """0. interpret task"""
            for event in self.WM.eventStack:
                if event.eventType == 'task':
                    self.WM.targetArea = self.WM.task.endConditions
                    self.WM.taskAreas[0] = self.WM.currentArea
                    self.WM.taskAreas[1] = self.WM.targetArea


            """1.measure unit position, speed, acceleration and current area. Check for static constraints when receiving
            new task, check for dynamic constraints every timestep. Calculate risk"""
            self.perception.updateWMPosition()
            self.perception.updateWMSpeed()
            self.perception.updateWMAcceleration()
            self.perception.checkUnitArea()
            for event in self.WM.eventStack:
                if event.eventType == 'task':
                    self.perception.checkStaticConstraints()
            self.perception.checkDynamicConstraints()
            self.perception.checkPredictedConstraintCollision()
            #self.perception.calculateRisk(self)

            """2.monitors put events on the event stack"""
            constraintMonitor.monitorConstraints()
            unitTaskMonitor.isTaskNew()
            stateMonitor.monitorPlanState()
            locationMonitor.monitorLocation()
            targetReachedMonitor.isTargetReached()

            """3. controller reads events and changes unit plan state and control state"""
            self.controller.updatePlanState()
            self.controller.updateControlState()

            """4. execute control state"""
            self.controller.executeControlState()

            yield self.env.timeout(1)
