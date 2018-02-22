from remoteObject import RemoteObject
import os
from Framework import get_icon_path

ICON_PATH = get_icon_path()

class AlembicFile(RemoteObject):

    def __init__(self, alembicPath):
        super(AlembicFile, self).__init__(path=alembicPath)

        self.icon = os.path.join(ICON_PATH, "extension_abc.png")
        self.associatedExtensions = [".abc"]

