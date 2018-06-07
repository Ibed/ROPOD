class Event(object):

    def __init__(self,eventType,eventSubject,eventMessage,isNegated = False):
        self.eventType = eventType       #what kind of event?
        self.eventSubject = eventSubject #about what object/variable?
        self.eventMessage = eventMessage #what's the state of the object?

        self.isNegated = isNegated       #when this is true, it gets interpreted as the opposite by the controller

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
