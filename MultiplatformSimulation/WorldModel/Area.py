
class Area(object):

    def __init__(self,xDim, yDim, level, label):
        self.xDim = xDim
        self.yDim = yDim
        self.level = level
        self.label = label
        self.motherNode = []
        self.daughterNodes = []
        self.posRelToMother = [0,0]
        self.posRelToTopNode = [0,0]
        self.isAvailable = True
        self.currentState = None
        self.previousState = None

    def updateDaughterNodes(self):
        if len(self.daughterNodes) == 0:
            return
        else:
            for area in self.daughterNodes:
                area.posRelToTopNode[0] += self.posRelToMother[0]
                area.posRelToTopNode[1] += self.posRelToMother[1]
                area.updateDaughterNodes()
