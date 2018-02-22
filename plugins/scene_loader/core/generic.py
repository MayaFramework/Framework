from remoteObject import RemoteObject

class GenericObject(RemoteObject):

    def __init__(self, path):
        super(GenericObject, self).__init__(path=path)
