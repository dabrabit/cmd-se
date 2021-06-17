class ExpertSystem(object):
    """docstring for ExpertSystem."""

    def __init__(self, objects={}):
        super(ExpertSystem, self).__init__()

        # Properties
        self.objects = objects
        self.askedAttributes = {}

    def setAskedAttribute(self, attr, value):
        self.askedAttributes[attr] = value
        return None

    def getObjectAttributes(self, object):
        return self.objects[object]['attrs']

    def wasAttributeAskedFor(self, attr):
        return attr in self.askedAttributes

    def hasCertainTypeOfAttributes(self, object, type):
        for attr in self.askedAttributes:
            if self.askedAttributes[attr] != type:
                continue

            if type:
                if attr not in self.objects[object]['attrs']:
                    return False
            else:
                if attr in self.objects[object]['attrs']:
                    return True

        return type

    def wasAttributeRejected(self, object):
        for attr in self.objects[object]['attrs']:
            if not self.askedAttributes[attr]:
                return True

        return False
