class State(object):

    def __init__(self,label,stateType,stateSubject):
        self.label = label
        self.stateType = stateType
        self.stateSubject = stateSubject
        self.listOfTriggers = []