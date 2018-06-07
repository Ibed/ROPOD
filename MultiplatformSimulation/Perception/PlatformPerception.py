
class PlatformPerception(object):

    def __init__(self, world, worldModel):
        """This details the outward perceptions to other units/platforms or objects. The own location of the platform
        is decided by perceiving the own unit locations"""
        self.world = world
        self.worldModel = worldModel

    def checkPlatformState(self):
        """if all units are in an area, switch world model current state"""
        units = iter(self.worldModel.listOfUnits)
        try:
            first = next(units)
        except StopIteration:
            print('platform has no units')
            return
        unitsAreInSameArea = all(first.WM.currentArea == rest.WM.currentArea for rest in units)
        if unitsAreInSameArea:
            self.worldModel.currentArea = first.WM.currentArea

    def checkQueriedAreas(self,areasToPerceive):
        """check for objects in queried areas and update in WM"""
        """locate area origin (center) in world frame"""
        for areaLabel in areasToPerceive:
            area = self.worldModel.returnArea(areaLabel)
            area.isAvailable = True
            """check units inside area"""
            leftAreaBoundary = area.posRelToTopNode[0] - area.xDim / 2
            rightAreaBoundary = area.posRelToTopNode[0] + area.xDim / 2
            bottomAreaBoundary = area.posRelToTopNode[1] - area.yDim / 2
            topAreaBoundary = area.posRelToTopNode[1] + area.yDim / 2
            for unit in self.world.listOfUnits:
                ownUnit = self.worldModel.isPartOfPlatform(unit)
                if not ownUnit:
                    if (unit.actualPosition[0]-unit.radius > leftAreaBoundary
                        and unit.actualPosition[0]+unit.radius < rightAreaBoundary
                        and unit.actualPosition[1]-unit.radius > bottomAreaBoundary
                        and unit.actualPosition[1]+unit.radius < topAreaBoundary):
                        area.isAvailable = False
            """check obstacles"""
            for object in self.world.listOfObjects:
                if (object.actualPosition[0]-object.radius > leftAreaBoundary
                    and object.actualPosition[0]+object.radius < rightAreaBoundary
                    and object.actualPosition[1]-object.radius > bottomAreaBoundary
                    and object.actualPosition[1]+object.radius < topAreaBoundary):
                    area.isAvailable = False

