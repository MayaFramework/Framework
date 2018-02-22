from alembic import AlembicFile
from image import ImageFile
from scene import Scene
from remoteObject import RemoteObject
from generic import GenericObject
import os

import json

class TypeChooser(object):

    @staticmethod
    def getObjectType(path):
        extension = RemoteObject.getExtension(path)
        classObj = TypeChooser.getCorrectClass(extension)
        instancedClassObj = classObj(path)
        return instancedClassObj

    @staticmethod
    def getCorrectClass(extension):
        path_to_current_file = os.path.realpath(__file__)
        current_directory = os.path.dirname(path_to_current_file)
        path_to_file = os.path.join(current_directory, "extensions.json")
        with open(path_to_file) as extensionsConfig:
            data = json.load(extensionsConfig)
        for k,v in data.iteritems():
            if extension in v.get("extensions"):
                return eval(v.get("class"))
        else:
            return GenericObject




