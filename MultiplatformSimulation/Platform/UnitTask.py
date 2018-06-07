class UnitTask(object):

    def __init__(self,endConditions = None,configuration = None,preConditions=None):
        """for now, no preconditions are needed, and the endconditions are an areaLabel"""
        self.preConditions = preConditions
        self.endConditions = endConditions
        self.configuration = configuration

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__