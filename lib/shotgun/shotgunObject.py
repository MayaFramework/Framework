import shotgun_api3 as sapi
from shotgunExceptions import NotValidField
from abc import ABCMeta
import logging

logging.basicConfig()
logger = logging.getLogger("shotgunObject")

class ShotgunObject(object):

    TYPE = None
    NAMINGATTR = None

    __metaclass__ = ABCMeta

    def __init__(self, objectId, **extraInfo):

        self.shotgun = sapi.Shotgun("https://esdip.shotgunstudio.com",
                                    script_name="shotgunAPI", api_key="f8da64a710923a25352e3d0e06bd31c56395cb5943e03bfaf9a90a73794e1ac1")

        self.id = objectId
        self._extraInfo = extraInfo

        [setattr(self, k,v) for k,v in extraInfo.iteritems()]        

    def __str__(self):
        return "({type} {name}: [{extraInfo}])".format(type=self.TYPE, name=self.entityName, extraInfo=self._extraInfo)

    def __getattr__(self, attr):
        if not attr in self.__dict__:
            logger.warning("Getting attr '{}' from Shotgun for {}".format(attr, self.__class__.__name__))
            _attr = self.getField(attr)
            if not _attr:
                raise NotValidField("{} is not a valid field for {}".format(attr, self.TYPE))
            setattr(self, attr, _attr)
            return _attr
        else:
            return self.__dict__.get(attr)

    @property
    def entityName(self):
        if not hasattr(self, self.NAMINGATTR):
            __nameAttr = self.getField(self.NAMINGATTR)
            if not __nameAttr:
                return None

            setattr(self, self.NAMINGATTR, __nameAttr)
            return __nameAttr
        else:
            return getattr(self, self.NAMINGATTR)

    @entityName.setter
    def entityName(self, value):
        if not hasattr(self, self.NAMINGATTR):
            setattr(self, self.NAMINGATTR, value)

    @property
    def entityType(self):
        return self.TYPE

    def getField(self, field):
        if not isinstance(field, str):
            raise TypeError("fields must be a str, not {}".format(type(field)))

        return self.shotgun.find_one(self.TYPE, [["id", "is", self.id]], [field]).get(field)

    def getFields(self, fields):
        if not isinstance(fields, list):
            raise TypeError("fields must be a list, not {}".format(type(fields)))
            
        return self.shotgun.find_one(self.TYPE, [["id", "is", self.id]], fields) 