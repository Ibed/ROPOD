import math
import copy
import numpy as np
from shapely.geometry import LineString

class UnitPerception(object):

    def __init__(self,world, worldModel):
        """this class 'measures' unit physical parameters"""
        self.world = world
        self.worldModel = worldModel

    def checkUnitArea(self):
        """update current area based on position"""
        position = self.worldModel.measuredPositionRelToCurrentArea
        if not(position[0] > -self.worldModel.currentArea.xDim /2 and
            position[0] < self.worldModel.currentArea.xDim / 2 and
            position[1] > -self.worldModel.currentArea.yDim / 2 and
            position[1] < self.worldModel.currentArea.yDim / 2):
            for area in self.worldModel.areaList:
                if not area.daughterNodes:
                    for unit in self.world.listOfUnits:
                        if unit.label == self.worldModel.label:
                            leftAreaBoundary = area.posRelToTopNode[0] - area.xDim / 2
                            rightAreaBoundary = area.posRelToTopNode[0] + area.xDim / 2
                            bottomAreaBoundary = area.posRelToTopNode[1] - area.yDim / 2
                            topAreaBoundary = area.posRelToTopNode[1] + area.yDim / 2
                            if (unit.actualPosition[0] - unit.radius > leftAreaBoundary
                                and unit.actualPosition[0] + unit.radius < rightAreaBoundary
                                and unit.actualPosition[1] - unit.radius > bottomAreaBoundary
                                and unit.actualPosition[1] + unit.radius < topAreaBoundary):
                                self.worldModel.currentArea = area

    def updateWMPosition(self):
        """check relative position of unit in area, then update WM"""
        measuredRelPosition = [0,0]
        for unit in self.world.listOfUnits:
            if unit.platformLabel == self.worldModel.platformLabel and unit.label == self.worldModel.label:
                measuredRelPosition[0] = unit.actualPosition[0] - self.worldModel.currentArea.posRelToTopNode[0]
                measuredRelPosition[1] = unit.actualPosition[1] - self.worldModel.currentArea.posRelToTopNode[1]
                self.worldModel.measuredPositionRelToCurrentArea = measuredRelPosition

    def updateWMSpeed(self):
        """check speed of unit in world, then update WM"""
        for unit in self.world.listOfUnits:
            if unit.platformLabel == self.worldModel.platformLabel and unit.label == self.worldModel.label:
                self.worldModel.measuredSpeed = unit.actualSpeed

    def updateWMAcceleration(self):
        """check speed of unit in world, then update WM"""
        for unit in self.world.listOfUnits:
            if unit.platformLabel == self.worldModel.platformLabel and unit.label == self.worldModel.label:
                self.worldModel.measuredAcceleration = unit.actualAcceleration

    def checkStaticConstraints(self):
        """check static constraints for the unit of the current and target area. a constraint collision monitor will check
        the evolution of these constraints relative to each other"""
        constraintList = []
        stepsize = 0.01
        tolerance = 0
        """discretise area constraints into points relative to starting area origin"""
        if self.worldModel.currentArea.posRelToTopNode[0] < self.worldModel.targetArea.posRelToTopNode[0]:
            x = -self.worldModel.currentArea.xDim / 2 +tolerance
            y = -self.worldModel.currentArea.yDim / 2 +tolerance
            while y <= self.worldModel.currentArea.yDim/2-tolerance:
                point = [-self.worldModel.currentArea.xDim/2+tolerance, y]
                constraintList.append(point)
                y += stepsize
            while x <= self.worldModel.currentArea.xDim/2+self.worldModel.targetArea.xDim-tolerance:
                point = [x, self.worldModel.currentArea.yDim/2-tolerance]
                constraintList.append(point)
                x += stepsize
            while y >= -self.worldModel.currentArea.yDim/2+tolerance:
                point = [self.worldModel.currentArea.xDim/2+self.worldModel.targetArea.xDim-tolerance, y]
                constraintList.append(point)
                y -= stepsize
            while x >= -self.worldModel.currentArea.xDim/2+tolerance:
                point = [x, -self.worldModel.currentArea.yDim/2+tolerance]
                constraintList.append(point)
                x -= stepsize
        if self.worldModel.currentArea.posRelToTopNode[0] > self.worldModel.targetArea.posRelToTopNode[0]:
            x = self.worldModel.currentArea.xDim / 2 - tolerance
            y = -self.worldModel.currentArea.yDim / 2 +tolerance
            while y <= self.worldModel.currentArea.yDim/2-tolerance:
                point = [self.worldModel.currentArea.xDim/2-tolerance, y]
                constraintList.append(point)
                y += stepsize
            while x >= -self.worldModel.currentArea.xDim/2-self.worldModel.targetArea.xDim+tolerance:
                point = [x, self.worldModel.currentArea.yDim/2-tolerance]
                constraintList.append(point)
                x -= stepsize
            while y >= -self.worldModel.currentArea.yDim/2+tolerance:
                point = [-self.worldModel.currentArea.xDim/2-self.worldModel.targetArea.xDim+tolerance, y]
                constraintList.append(point)
                y -= stepsize
            while x <= self.worldModel.currentArea.xDim/2-tolerance:
                point = [x, -self.worldModel.currentArea.yDim/2+tolerance]
                constraintList.append(point)
                x += stepsize
        if self.worldModel.currentArea.posRelToTopNode[1] < self.worldModel.targetArea.posRelToTopNode[1]:
            x = -self.worldModel.currentArea.xDim / 2 +tolerance
            y = -self.worldModel.currentArea.yDim / 2 +tolerance
            while y <= self.worldModel.currentArea.yDim/2+self.worldModel.targetArea.yDim-tolerance:
                point = [-self.worldModel.currentArea.xDim/2+tolerance, y]
                constraintList.append(point)
                y += stepsize
            while x <= self.worldModel.currentArea.xDim/2-tolerance:
                point = [x, self.worldModel.currentArea.yDim/2+self.worldModel.targetArea.yDim-tolerance]
                constraintList.append(point)
                x += stepsize
            while y >= -self.worldModel.currentArea.yDim/2+tolerance:
                point = [self.worldModel.currentArea.xDim/2-tolerance, y]
                constraintList.append(point)
                y -= stepsize
            while x >= -self.worldModel.currentArea.xDim/2+tolerance:
                point = [x, -self.worldModel.currentArea.yDim/2+tolerance]
                constraintList.append(point)
                x -= stepsize
        if self.worldModel.currentArea.posRelToTopNode[1] > self.worldModel.targetArea.posRelToTopNode[1]:
            x = -self.worldModel.currentArea.xDim / 2 +tolerance
            y = self.worldModel.currentArea.yDim / 2 -tolerance
            while y >= -self.worldModel.currentArea.yDim/2-self.worldModel.targetArea.yDim+tolerance:
                point = [-self.worldModel.currentArea.xDim/2+tolerance, y]
                constraintList.append(point)
                y -= stepsize
            while x <= self.worldModel.currentArea.xDim/2-tolerance:
                point = [x, -self.worldModel.currentArea.yDim/2-self.worldModel.targetArea.yDim+tolerance]
                constraintList.append(point)
                x += stepsize
            while y <= self.worldModel.currentArea.yDim/2-tolerance:
                point = [self.worldModel.currentArea.xDim/2-tolerance, y]
                constraintList.append(point)
                y += stepsize
            while x <= -self.worldModel.currentArea.xDim/2+tolerance:
                point = [x, self.worldModel.currentArea.yDim/2-tolerance]
                constraintList.append(point)
                x += stepsize

        for area in self.worldModel.taskAreas:
            for object in self.world.listOfObjects:
                leftAreaBoundary = area.posRelToTopNode[0] - area.xDim / 2
                rightAreaBoundary = area.posRelToTopNode[0] + area.xDim / 2
                bottomAreaBoundary = area.posRelToTopNode[1] - area.yDim / 2
                topAreaBoundary = area.posRelToTopNode[1] + area.yDim / 2
                if (object.actualPosition[0] >= leftAreaBoundary
                    and object.actualPosition[0] <= rightAreaBoundary
                    and object.actualPosition[1] >= bottomAreaBoundary
                    and object.actualPosition[1] <= topAreaBoundary):
                    angleIncrement = stepsize/object.radius
                    objectOrigin = [0,0]
                    objectOrigin[0] = object.actualPosition[0] - self.worldModel.taskAreas[0].posRelToTopNode[0]
                    objectOrigin[1] = object.actualPosition[1] - self.worldModel.taskAreas[0].posRelToTopNode[1]
                    angle = 0
                    while angle < 2*math.pi:
                        point = [objectOrigin[0]+(object.radius+tolerance)*math.cos(angle), objectOrigin[1]+(object.radius+tolerance)
                                 *math.sin(angle)]
                        constraintList.append(point)
                        angle += angleIncrement

        self.worldModel.staticConstraints = constraintList

    def checkDynamicConstraints(self):
        """check static constraints for the unit of the current and target area. a constraint collision monitor will check
                the evolution of these constraints relative to each other"""
        """discretise units into points relative to starting area origin"""
        constraintList = []
        stepsize = 0.01 #arc length
        tolerance = 0.05
        for area in self.worldModel.taskAreas:
            for unit in self.world.listOfUnits:
                if unit.label != self.worldModel.label:
                    leftAreaBoundary = area.posRelToTopNode[0] - area.xDim / 2
                    rightAreaBoundary = area.posRelToTopNode[0] + area.xDim / 2
                    bottomAreaBoundary = area.posRelToTopNode[1] - area.yDim / 2
                    topAreaBoundary = area.posRelToTopNode[1] + area.yDim / 2
                    if (unit.actualPosition[0] > leftAreaBoundary
                        and unit.actualPosition[0] < rightAreaBoundary
                        and unit.actualPosition[1] > bottomAreaBoundary
                        and unit.actualPosition[1] < topAreaBoundary):
                        angleIncrement = stepsize/unit.radius
                        unitOrigin = [0,0]
                        unitOrigin[0] = unit.actualPosition[0] - self.worldModel.taskAreas[0].posRelToTopNode[0]
                        unitOrigin[1] = unit.actualPosition[1] - self.worldModel.taskAreas[0].posRelToTopNode[1]
                        angle = 0
                        while angle < 2*math.pi:
                            point = [unitOrigin[0]+(unit.radius+tolerance)*math.cos(angle), unitOrigin[1]+(unit.radius+tolerance)
                                     *math.sin(angle)]
                            constraintList.append(point)
                            angle += angleIncrement
        self.worldModel.dynamicConstraints = constraintList

    def checkPredictedConstraintCollision(self):
        """check predicted constraint collisions according to braking vector"""
        """1.calculate braking distance vector"""
        brakingVector = self.calculateBrakingVector()
        """2.check for constraints"""
        violatingConstraints = []
        staticConstraints = copy.deepcopy(self.worldModel.staticConstraints)
        allConstraints = copy.deepcopy(self.worldModel.dynamicConstraints)
        allConstraints.extend(staticConstraints)
        for constraint in allConstraints:
            point = self.worldModel.areaFramePointToUnitFrame(constraint,
                                                              self.worldModel.getDirection(brakingVector) - math.pi / 2)
            if (point[0] < self.worldModel.radius and point[0] > -self.worldModel.radius
                and point[1] > -self.worldModel.radius and point[1] < self.worldModel.getMagnitude(brakingVector)):
                violatingConstraints.append(point)
        self.worldModel.predictedConstraints = violatingConstraints
        if violatingConstraints:
            self.worldModel.constraintViolationPredicted = True
        else:
            self.worldModel.constraintViolationPredicted = False

    def calculateBrakingVector(self):
        timestep = 0.01
        predictedVelocity = self.worldModel.measuredSpeed
        predictedVelocityMag = self.worldModel.getMagnitude(predictedVelocity)
        predictedVelocityDir = self.worldModel.getDirection(predictedVelocity)
        predictedDistance = [0, 0]
        while predictedVelocityMag > 0.01:
            predictedDistance[0] = predictedDistance[0] + predictedVelocity[0] * timestep
            predictedDistance[1] = predictedDistance[1] + predictedVelocity[1] * timestep

            predictedVelocityMag = predictedVelocityMag - (1/self.worldModel.mass)*self.worldModel.maxOutputForceMagnitude*timestep
            predictedVelocity = self.worldModel.getVector(predictedVelocityDir, predictedVelocityMag)

        brakingVector = predictedDistance
        brakingVectorMag = self.worldModel.getMagnitude(brakingVector)*1.5    #tolerance factor
        brakingVectorMag += self.worldModel.radius
        brakingVectorDirection = self.worldModel.getDirection(brakingVector)
        brakingVector = self.worldModel.getVector(brakingVectorDirection,brakingVectorMag)
        return brakingVector

    def updateWMForce(self):
        """check external force on the unit in list of units of world, then update WM"""

    def calculateRisk(self,unit):
        environmentLines = []
        for structure in self.world.listOfStructures:
            line1 = [structure.position[0] - structure.xDim / 2 - unit.actualPosition[0],
                     structure.position[1] - structure.yDim / 2 - unit.actualPosition[1],
                     structure.position[0] - structure.xDim / 2 - unit.actualPosition[0],
                     structure.position[1] + structure.yDim / 2 - unit.actualPosition[1],
                     [0,0]]
            line2 = [structure.position[0] - structure.xDim / 2 - unit.actualPosition[0],
                     structure.position[1] + structure.yDim / 2 - unit.actualPosition[1],
                     structure.position[0] + structure.xDim / 2 - unit.actualPosition[0],
                     structure.position[1] + structure.yDim / 2 - unit.actualPosition[1],
                     [0,0]]
            line3 = [structure.position[0] + structure.xDim / 2 - unit.actualPosition[0],
                     structure.position[1] + structure.yDim / 2 - unit.actualPosition[1],
                     structure.position[0] + structure.xDim / 2 - unit.actualPosition[0],
                     structure.position[1] - structure.yDim / 2 - unit.actualPosition[1],
                     [0,0]]
            line4 = [structure.position[0] + structure.xDim / 2 - unit.actualPosition[0],
                     structure.position[1] - structure.yDim / 2 - unit.actualPosition[1],
                     structure.position[0] - structure.xDim / 2 - unit.actualPosition[0],
                     structure.position[1] - structure.yDim / 2 - unit.actualPosition[1],
                     [0,0]]
            environmentLines.append(line1)
            environmentLines.append(line2)
            environmentLines.append(line3)
            environmentLines.append(line4)
        for otherUnit in self.world.listOfUnits:
            if otherUnit.WM.label != self.worldModel.label:
                line1 = [otherUnit.actualPosition[0] - otherUnit.radius - unit.actualPosition[0],
                         otherUnit.actualPosition[1] - otherUnit.radius - unit.actualPosition[1],
                         otherUnit.actualPosition[0] - otherUnit.radius - unit.actualPosition[0],
                         otherUnit.actualPosition[1] + otherUnit.radius - unit.actualPosition[1],
                         otherUnit.actualSpeed]
                line2 = [otherUnit.actualPosition[0] - otherUnit.radius - unit.actualPosition[0],
                         otherUnit.actualPosition[1] + otherUnit.radius - unit.actualPosition[1],
                         otherUnit.actualPosition[0] + otherUnit.radius - unit.actualPosition[0],
                         otherUnit.actualPosition[1] + otherUnit.radius - unit.actualPosition[1],
                         otherUnit.actualSpeed]
                line3 = [otherUnit.actualPosition[0] + otherUnit.radius - unit.actualPosition[0],
                         otherUnit.actualPosition[1] + otherUnit.radius - unit.actualPosition[1],
                         otherUnit.actualPosition[0] + otherUnit.radius - unit.actualPosition[0],
                         otherUnit.actualPosition[1] - otherUnit.radius - unit.actualPosition[1],
                         otherUnit.actualSpeed]
                line4 = [otherUnit.actualPosition[0] + otherUnit.radius - unit.actualPosition[0],
                         otherUnit.actualPosition[1] - otherUnit.radius - unit.actualPosition[1],
                         otherUnit.actualPosition[0] - otherUnit.radius - unit.actualPosition[0],
                         otherUnit.actualPosition[1] - otherUnit.radius - unit.actualPosition[1],
                         otherUnit.actualSpeed]
                environmentLines.append(line1)
                environmentLines.append(line2)
                environmentLines.append(line3)
                environmentLines.append(line4)
        theta = 0
        deltaTheta = 2*math.pi/360
        Np = 2*math.pi/deltaTheta
        Np = round(Np)
        unitPerceptionRange = 5
        risk = 0
        for x in range(0,Np):
            unitLine = [0,0,math.cos(theta)*unitPerceptionRange, math.sin(theta)*unitPerceptionRange]
            theta += deltaTheta
            sections = []
            for line in environmentLines:

                line1 = LineString([(line[0], line[1]), (line[2], line[3])])
                line2 = LineString([(unitLine[0], unitLine[1]), (unitLine[2], unitLine[3])])
                section = line1.intersection(line2)

                if (section.bounds):
                    point = [section.bounds[0],section.bounds[1],line[4]]
                    sections.append(point)

            for s in sections:
                magnitudes = []
                mag = math.sqrt(math.pow(s[0],2)+math.pow(s[1],2))
                magnitudes.append(mag)

            if len(sections)!=0:
                relPos = copy.deepcopy(sections[magnitudes.index(min(magnitudes))])
                ownSpeed = self.worldModel.measuredSpeed
                speed = [ownSpeed[0]-relPos[2][0],ownSpeed[1]-relPos[2][1]]
                if math.sqrt(math.pow(speed[0],2)+math.pow(speed[1],2)) > 0.01:
                    epsilon = ((relPos[0]/math.sqrt(math.pow(relPos[0],2)+math.pow(relPos[1],2))*
                              speed[0]/math.sqrt(math.pow(speed[0],2)+math.pow(speed[1],2))+
                              relPos[1]/math.sqrt(math.pow(relPos[0],2)+math.pow(relPos[1],2))*
                              speed[1]/math.sqrt(math.pow(speed[0],2)+math.pow(speed[1],2))+1)*0.5)
                    risk += (math.sqrt(math.pow(speed[0],2)+math.pow(speed[1],2))/
                            (math.sqrt(math.pow(relPos[0],2)+math.pow(relPos[1],2))-self.worldModel.radius)*math.pow(epsilon,2))
        risk = 1/Np*risk
        self.worldModel.risk.append(risk)