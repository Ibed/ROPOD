import math
from Platform import UnitTask as ut
class UnitWM (object):

    def __init__(self,platformLabel, label,mass,radius,posRelToStartingArea,startingArea,areaList):
        self.label = label
        self.platformLabel = platformLabel
        self.currentArea = startingArea
        self.targetArea = startingArea
        self.taskAreas = [self.currentArea, self.targetArea]
        self.areaList = areaList
        self.eventStack = []
        self.platformEvents = []
        self.listOfMonitors = []
        self.task = ut.UnitTask()
        self.staticConstraints = [] #list of points
        self.dynamicConstraints = []  # list of points
        self.predictedConstraints = []
        self.constraintViolationPredicted = False

        """Physical parameters"""
        """these are in the local frame of the area"""
        self.mass = mass
        self.radius = radius
        self.measuredPositionRelToCurrentArea = posRelToStartingArea
        self.measuredSpeed = [0,0]
        self.measuredAcceleration = [0,0]
        self.measuredForceOnUnit = [0,0] #external forces
        self.nominalSpeedMagnitude = 1.4
        self.maxOutputForceMagnitude = 10
        self.maxAccelerationMagnitude = self.maxOutputForceMagnitude/self.mass
        self.forceGain = 1
        self.desiredMotionDirection = 0

        self.risk = []

    def getDirection(self,vector):
        return math.atan2(vector[1],vector[0])

    def getMagnitude(self,vector):
        return math.sqrt(math.pow(vector[0],2)+ math.pow(vector[1],2))

    def getVector(self,direction,magnitude):
        vector = [0,0]
        vector[0] = math.cos(direction)*magnitude
        vector[1] = math.sin(direction)*magnitude
        return vector

    def areaFramePointToUnitFrame(self, point, angle):
        output = [0,0]
        unitPosRelToStartingArea = [0,0]
        unitPosRelToStartingArea[0] = self.measuredPositionRelToCurrentArea[0]+self.currentArea.posRelToTopNode[0]\
                                      -self.taskAreas[0].posRelToTopNode[0]
        unitPosRelToStartingArea[1] = self.measuredPositionRelToCurrentArea[1] + self.currentArea.posRelToTopNode[1] \
                                      - self.taskAreas[0].posRelToTopNode[1]
        point[0] = point[0] - unitPosRelToStartingArea[0]
        point[1] = point[1] - unitPosRelToStartingArea[1]
        output[0] = point[0] * math.cos(angle) + point[1] * math.sin(angle)
        output[1] = -point[0] * math.sin(angle) + point[1] * math.cos(angle)
        return output

    def unitFrameVectorToAreaFrame(self,vector,angle):
        output = [0, 0]
        output[0] = vector[0] * math.cos(angle) - vector[1] * math.sin(angle)
        output[1] = vector[0] * math.sin(angle) + vector[1] * math.cos(angle)
        return output