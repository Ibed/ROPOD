from matplotlib import pyplot as plt
from matplotlib import patches
import math
import numpy as np

class World (object):

    def __init__(self,xDim,yDim,env):
        """origin lies at the center of the world, coincident with the top level mother node of the platform WM"""
        self.xDim = xDim
        self.yDim = yDim
        self.listOfStructures = [] #list of vectors containing [xDim,yDim,position]
        self.listOfUnits = []  #list of vectors containing [unit object]
        self.listOfObjects = []
        self.areaList = []   #areaList of one of the platforms

        self.timestep = 0.01
        self.env = env
        self.action = env.process(self.run())

    def run(self):
        """function gets called when initialized"""
        end = 250
        """initialize figure for showing world elements"""
        xLim = [0, 0]
        yLim = [0, 0]
        fig = plt.figure()
        for area in self.areaList:
            if area.level == 0:
                margin = 0.5
                xLim[0] = -area.xDim/2 - margin
                xLim[1] = area.xDim / 2 + margin
                yLim[0] = -area.yDim / 2 - margin
                yLim[1] = area.yDim / 2 + margin
                break

        ax = plt.axes(xlim=(xLim[0], xLim[1]), ylim=(yLim[0], yLim[1]))
        plt.gca().set_aspect('equal', adjustable='box')

        """draw areas"""
        for area in self.areaList:
            if area.level == 0:
                ax.add_patch(patches.Rectangle((-area.xDim/2,-area.yDim/2) ,area.xDim,area.yDim, fill=False, linestyle='dotted'))
                plt.text(-area.xDim/2,-area.yDim/2,area.label)
            if area.level > 0:
                ax.add_patch(patches.Rectangle((area.posRelToTopNode[0]-area.xDim / 2, area.posRelToTopNode[1]-area.yDim / 2)
                                               , area.xDim, area.yDim, fill=False, linestyle='dotted'))
                plt.text(area.posRelToTopNode[0]-area.xDim / 2, area.posRelToTopNode[1]-area.yDim / 2, area.label)

        """draw structures"""
        for structure in self.listOfStructures:
            ax.add_patch(patches.Rectangle((structure.position[0]-structure.xDim / 2, structure.position[1]-structure.yDim / 2),
                                           structure.xDim, structure.yDim, fill=False))

        """draw objects"""
        for object in self.listOfObjects:
            circle = plt.Circle((object.actualPosition), object.radius, fill=False)
            ax.add_patch(circle)

        """draw units"""
        #ax.annotate('unit going from one area to another', xy=(-2, 2.1))

        for unit in self.listOfUnits:
            circle = plt.Circle((unit.actualPosition), unit.radius, fill=False)
            #label = ('1')
            #ax.annotate(label, xy=unit.actualPosition)
            ax.add_patch(circle)

        plt.ion()
        plt.show()

        while True:
            """update world elements"""
            for unit in self.listOfUnits:

                speed = unit.WM.getMagnitude(unit.actualSpeed)
                if not speed < 0.001 and speed > -0.001:
                    dragDirection = unit.WM.getDirection(unit.actualSpeed) + math.pi
                    dragVector = unit.WM.getVector(dragDirection,unit.dragMagnitude)
                else:
                    dragVector = [0,0]
                    unit.actualSpeed = [0,0]

                unit.totalForceOnUnit[0] = unit.externalForceOnUnit[0] + unit.drivingForce[0] + dragVector[0]
                unit.totalForceOnUnit[1] = unit.externalForceOnUnit[1] + unit.drivingForce[1] + dragVector[1]

                unit.actualAcceleration[0] = unit.totalForceOnUnit[0] / unit.mass
                unit.actualAcceleration[1] = unit.totalForceOnUnit[1] / unit.mass

                unit.actualSpeed[0] += unit.actualAcceleration[0] * self.timestep
                unit.actualSpeed[1] += unit.actualAcceleration[1] * self.timestep

                unit.previousPosition = [unit.actualPosition[0],unit.actualPosition[1]]

                unit.actualPosition[0] += unit.actualSpeed[0] * self.timestep
                unit.actualPosition[1] += unit.actualSpeed[1] * self.timestep

                if self.env.now<end:
                    plt.plot([unit.previousPosition[0],unit.actualPosition[0]],[unit.previousPosition[1],unit.actualPosition[1]],'b')

                    """print('time passed:', self.env.now * self.timestep, 'seconds')
                    unit.distanceTravelled += math.sqrt(math.pow(unit.actualPosition[0] - unit.previousPosition[0], 2) + math.pow(
                        unit.actualPosition[1] - unit.previousPosition[1], 2))
                    print(unit.label, 'distance traveled:', unit.distanceTravelled, 'metres')"""
                if False:
                    plt.figure()
                    t = np.linspace(0, end/ (1/self.timestep), len(self.listOfUnits[0].WM.risk))
                    plt.plot(t,self.listOfUnits[0].WM.risk)
                    plt.title('unit risk for low granularity world model')
                    plt.xlabel('time [s]')
                    plt.ylabel('absolute risk')
                    print('average risk:',sum(self.listOfUnits[0].WM.risk)/len(self.listOfUnits[0].WM.risk))

                    """plt.figure()
                    t = np.linspace(0, end / (1/self.timestep), len(self.listOfUnits[1].WM.risk))
                    plt.plot(t, self.listOfUnits[1].WM.risk)
                    plt.title('platform 2 unit risk')
                    plt.xlabel('time [s]')
                    plt.ylabel('absolute risk')
                    print('average risk:', sum(self.listOfUnits[1].WM.risk) / len(self.listOfUnits[1].WM.risk))"""


            plt.draw()
            if False:
                for unit in self.listOfUnits:
                    if unit.WM.staticConstraints:
                        for constraint in unit.WM.staticConstraints:
                            point = plt.Circle((constraint[0]+unit.WM.taskAreas[0].posRelToTopNode[0],
                                                constraint[1]+unit.WM.taskAreas[0].posRelToTopNode[1]),0.01)
                            ax.add_patch(point)
                    if unit.WM.dynamicConstraints:
                        for constraint in unit.WM.dynamicConstraints:
                            point = plt.Circle((constraint), 0.01)
                            ax.add_patch(point)

            fig.canvas.flush_events()
            yield self.env.timeout(1)


    def setAreaList(self,areaList):
        self.areaList = areaList

    def addStructure(self,xDim, yDim, position):
        self.listOfStructures.append(Structure(xDim,yDim,position))

    def addObject(self,radius,actualPosition):
        self.listOfObjects.append(Object(radius,actualPosition))

    def addUnit(self,unit):
        """position is required in world frame, not local area frame"""
        self.listOfUnits.append(unit)
        print('unit added to world')


class Object(object):

    def __init__(self,radius,actualPosition):
        self.radius = radius
        self.actualPosition = actualPosition

class Structure(object):

    def __init__(self,xDim,yDim,position):
        self.xDim = xDim
        self.yDim = yDim
        self.position = position