import simpy
import World as w
from Perception import Event as e
from Platform import Platform as plat, PlatformTask as platTask

"""create simulation objects"""
env = simpy.Environment()
simpleWorld = w.World(4,4,env)
simpleTask = platTask.PlatformTask('A13')
platform1 = plat.Platform('platform 1',env,simpleWorld)

"""1.create world model(s)"""
platform1.WM.createArea(4, 4, 0, 'A')
platform1.WM.createArea(1, 1, 1, 'A1')
platform1.WM.createArea(1, 1, 1, 'A2')
platform1.WM.createArea(2, 1, 1, 'A3')
platform1.WM.createArea(1, 1, 1, 'A4')
platform1.WM.createArea(1, 1, 1, 'A5')
platform1.WM.createArea(2, 1, 1, 'A6')
platform1.WM.createArea(1, 1, 1, 'A7')
platform1.WM.createArea(2, 1, 1, 'A8')
platform1.WM.createArea(1, 1, 1, 'A9')
platform1.WM.createArea(1, 1, 1, 'A10')
platform1.WM.createArea(1, 1, 2, 'A31')
platform1.WM.createArea(1, 1, 2, 'A32')
platform1.WM.createArea(1, 1, 2, 'A61')
platform1.WM.createArea(1, 1, 2, 'A62')
platform1.WM.createArea(1, 1, 2, 'A81')
platform1.WM.createArea(1, 1, 2, 'A82')

platform1.WM.containArea('A', 'A1', [-1.5, 1.5])
platform1.WM.containArea('A', 'A2', [1.5, 1.5])
platform1.WM.containArea('A', 'A3', [-1, 0.5])
platform1.WM.containArea('A', 'A4', [0.5, 0.5])
platform1.WM.containArea('A', 'A5', [1.5, 0.5])
platform1.WM.containArea('A', 'A6', [-1, -0.5])
platform1.WM.containArea('A', 'A7', [1.5, -0.5])
platform1.WM.containArea('A', 'A8', [-1, -1.5])
platform1.WM.containArea('A', 'A9', [0.5, -1.5])
platform1.WM.containArea('A', 'A10', [1.5, -1.5])
platform1.WM.containArea('A3', 'A31', [-0.5, 0])
platform1.WM.containArea('A3', 'A32', [0.5, 0])
platform1.WM.containArea('A6', 'A61', [-0.5, 0])
platform1.WM.containArea('A6', 'A62', [0.5, 0])
platform1.WM.containArea('A8', 'A81', [-0.5, 0])
platform1.WM.containArea('A8', 'A82', [0.5, 0])

platform1.WM.linkAreas('A2', 'A5')

platform1.WM.setStartingArea('A10')
simpleWorld.setAreaList(platform1.WM.areaList)

"""2. give tasks"""
platform1.giveTask(simpleTask)

"""3. generate paths"""

"""4. generate plans"""
platform1.plan.addState('start',None,None)
platform1.plan.addState('PS1','waiting in', 'A10')
platform1.plan.addState('PS2', 'going to', 'A7')
platform1.plan.addState('PS3', 'waiting in','A7')
platform1.plan.addState('PS4', 'going to', 'A5')
platform1.plan.addState('PS5', 'waiting in','A5')
platform1.plan.currentStateLabel = 'start'

platform1.plan.addTrigger('start trigger','start','PS1',[[e.Event('location',platform1.WM.currentArea.label,platform1.label)]])
platform1.plan.addTrigger('PT1','PS1','PS2',[[e.Event('area','A7','available')]])
platform1.plan.addTrigger('PT2', 'PS2', 'PS1', [[e.Event('area', 'A7', 'unavailable')],[e.Event('location','A10',platform1.label)]])
platform1.plan.addTrigger('PT3', 'PS2', 'PS3',[[e.Event('location', 'A7', platform1.label)]])

platform1.plan.addTrigger('PT4','PS3','PS4',[[e.Event('area','A5','available')]])
platform1.plan.addTrigger('PT5', 'PS4', 'PS3', [[e.Event('area', 'A5', 'unavailable')],[e.Event('location','A7',platform1.label)]])
platform1.plan.addTrigger('PT6', 'PS4', 'PS5',[[e.Event('location', 'A7', platform1.label)]])

"""5.create platform units"""
platform1.createUnit('platform 1 body unit',5,0.15,[0.21,0])
platform1.createUnit('platform 1 left arm unit',5,0.15,[-0.21,0])

"""6. add objects and structures"""
simpleWorld.addObject(0.1,[1.2,-0.6])
simpleWorld.addStructure(4,4,[0,0])
simpleWorld.addStructure(1,1,[0.5,-0.5])
simpleWorld.addStructure(2,1,[0,1.5])


"""run simulation. one time unit is 0.05 seconds"""
env.run(1000)