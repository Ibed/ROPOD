from WorldModel import PlatformWM as w
from Plan import PlatformPlan as p
from Controller import PlatformController as c
from Perception import PlatformPerception as pe
from Platform import Unit as u
from Perception import Event as e
from Perception import LocationMonitor as lm
from Perception import StateMonitor as sm
from Perception import AreaMonitor as am
import copy

class Platform(object):

    def __init__(self, platformLabel, env,world):
        self.label = platformLabel
        self.WM = w.PlatformWM(platformLabel)
        self.plan = p.PlatformPlan()
        self.controller = c.PlatformController(self.WM,self.plan)
        self.perception = pe.PlatformPerception(world, self.WM)
        self.task = None
        self.world = world

        self.env = env
        self.action = env.process(self.run())

    def createUnit(self, unitLabel, mass, radius, posRelToStartingArea):
        currentArea = self.WM.currentArea
        areaList = self.WM.areaList
        unit = u.Unit(self.label,unitLabel,mass,radius, posRelToStartingArea,currentArea,areaList, self.env,self.world)
        self.WM.listOfUnits.append(unit)
        self.world.addUnit(unit)

    def giveTask(self,task):
        self.task = task

    def run(self):
        """called when initializing platform"""
        yield self.env.timeout(10)

        """1. create control FSM, the trigger conditions are dependant on the plan, but are static for now"""
        self.controller.changeTriggerConditions('CT1',[[e.Event('','','')]])
        self.controller.changeTriggerConditions('CT2', [[e.Event('', '', '')]])
        self.controller.changeTriggerConditions('CT3', [[e.Event('', '', '')]])
        self.controller.changeTriggerConditions('CT4', [[e.Event('', '', '')]])
        self.controller.changeTriggerConditions('CT5', [[e.Event('plan state type',self.label,'going to')]])
        self.controller.changeTriggerConditions('CT6', [[e.Event('plan state type',self.label,'waiting in')]])
        self.controller.changeTriggerConditions('start trigger', [[e.Event('location',self.WM.currentArea.label,self.label)]])


        """2.create monitors"""
        locationMonitor = lm.LocationMonitor(self.WM)
        areaMonitor = am.AreaMonitor(self.WM)
        stateMonitor = sm.StateMonitor(self.WM,self.plan)


        while True:
            yield self.env.timeout(1)
            """0. update target area"""
            self.plan.updateTargetArea(self.WM)

            """1. Update areas to be monitored"""
            areaLabelList = self.plan.determineAreasToBeMonitored()
            self.WM.updateAreasToBeMonitored(areaLabelList)

            """2. use perception to check own location and areas decided by the plan for objects or other units"""
            self.perception.checkQueriedAreas(areaLabelList)
            self.perception.checkPlatformState()

            """3. monitors check the plan (info stored in WM, but decided by plan) to decide what has to be monitored 
            and put events on event stacks"""
            stateMonitor.monitorPlanState()
            locationMonitor.monitorLocation()
            areaMonitor.monitorTargetAreas(self.WM.areasLabelsToBeMonitored)
            for unit in self.WM.listOfUnits:
                unit.WM.platformEvents = copy.deepcopy(self.WM.eventStack)

            """4. controller reads events, checks state triggers, switches plan (plan changes path and areas to be monitored)
            , control"""
            self.controller.updatePlanState()
            self.controller.updateControlState()

            """5. controller state is executed."""
            self.controller.executeControlState()
