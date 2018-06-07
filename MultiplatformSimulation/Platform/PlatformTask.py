class PlatformTask(object):

    def __init__(self,endConditions,preConditions=None):
        """for now, no preconditions are needed, and the endconditions are an areaLabel"""
        self.preConditions = preConditions
        self.endConditions = endConditions