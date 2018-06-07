class Trigger(object):

    def __init__(self,label,startNodeLabel,endNodeLabel,triggerConditions = [[]]):
        self.startNodeLabel = startNodeLabel
        self.endNodeLabel = endNodeLabel
        self.label = label

        self.triggerConditions = triggerConditions  #presented as a nested list e.g: [[event1] and [event2 or event3] and...]

    def isTriggered(self,eventList):
        passesCondition = False
        for conditionList in self.triggerConditions:
            for condition in conditionList:
                for event in eventList:
                    if event == condition and condition.isNegated == False:
                        passesCondition = True
                        break
                    if event != condition and condition.isNegated:
                        passesCondition = True
                if passesCondition:
                    break
            if not passesCondition:
                return False
            passesCondition = False
        return True