import simpy
import World as w
from Perception import Event as e
from Platform import Platform as plat, PlatformTask as platTask
from matplotlib import pyplot as plt

"""create simulation objects"""
env = simpy.Environment()
simpleWorld = w.World(3,3,env)
simpleTask = platTask.PlatformTask('A3')
platform1 = plat.Platform('platform 1',env,simpleWorld)

"""1.create world model(s)"""
platform1.WM.createArea(3, 3, 0, 'A')
platform1.WM.createArea(1.5, 1.5, 1, 'A1')
platform1.WM.createArea(1.5, 1.5, 1, 'A2')
platform1.WM.createArea(1.5, 1.5, 1, 'A3')

platform1.WM.containArea('A', 'A1', [-0.75, -0.75])
platform1.WM.containArea('A', 'A2', [-0.75, 0.75])
platform1.WM.containArea('A', 'A3', [0.75, 0.75])

platform1.WM.linkAreas('A1', 'A2')
platform1.WM.linkAreas('A2', 'A3')

platform1.WM.setStartingArea('A1')
simpleWorld.setAreaList(platform1.WM.areaList)

"""2. give tasks"""
platform1.giveTask(simpleTask)

"""3. generate paths"""

"""4. generate plans"""
platform1.plan.addState('start',None,None)
platform1.plan.addState('PS1','waiting in', 'A1')
platform1.plan.addState('PS2', 'going to', 'A2')
platform1.plan.addState('PS3', 'waiting in','A2')
platform1.plan.addState('PS4', 'going to', 'A3')
platform1.plan.addState('PS5', 'waiting in','A3')
platform1.plan.currentStateLabel = 'start'

platform1.plan.addTrigger('start trigger','start','PS1',[[e.Event('location',platform1.WM.currentArea.label,platform1.label)]])
platform1.plan.addTrigger('PT1','PS1','PS2',[[e.Event('area','A2','available')]])
platform1.plan.addTrigger('PT2', 'PS2', 'PS1', [[e.Event('area', 'A2', 'unavailable')],[e.Event('location','A1',platform1.label)]])
platform1.plan.addTrigger('PT3', 'PS2', 'PS3',[[e.Event('location', 'A2', platform1.label)]])
platform1.plan.addTrigger('PT4','PS3','PS4',[[e.Event('area','A3','available')]])
platform1.plan.addTrigger('PT5', 'PS4', 'PS3', [[e.Event('area', 'A3', 'unavailable')],[e.Event('location','A2',platform1.label)]])
platform1.plan.addTrigger('PT6', 'PS4', 'PS5',[[e.Event('location', 'A3', platform1.label)]])

"""5.create platform units"""
platform1.createUnit('platform 1 unit 1',6,0.2,[0.375,0])

"""6. add objects and structures"""
simpleWorld.addStructure(0.2,3.3,[-1.65,0.1])
simpleWorld.addStructure(3.2,0.2,[0.05,1.65])
simpleWorld.addStructure(1.5,1.5,[0.8,-0.8])


"""run simulation. one time unit is 0.01 seconds"""
env.run(1000)
while True:
    1

