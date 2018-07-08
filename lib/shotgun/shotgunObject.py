import shotgun_api3 as sapi


class ShotgunObject(object):

    TYPE = None

    def __init__(self, code=None, objectId=None, **extraInfo):

        self.shotgun = sapi.Shotgun("https://esdip.shotgunstudio.com",
                                    script_name="shotgunAPI", api_key="f8da64a710923a25352e3d0e06bd31c56395cb5943e03bfaf9a90a73794e1ac1")

        self.id = objectId if objectId else extraInfo.pop("id", None)
        self.code = code if code else extraInfo.pop("code", None)

        if not self.id and not self.code:
            raise RuntimeError("At least code or id must be provided")

        elif self.id and not self.code:
            seq = self.shotgun.find_one(self.TYPE, [["id", "is", self.id]], ["code"])
            self.code = seq.get("code")

        elif not self.id and self.code:
            seq = self.shotgun.find_one(self.TYPE, [["code", "is", self.code]])
            self.id = seq.get("id")

        # for k,v in extraInfo.iteritems():
            # print k,v
        [setattr(self, k,v) for k,v in extraInfo.iteritems()]

    def getField(self, field):
        if not isinstance(field, str):
            raise TypeError("fields must be a str, not {}".format(type(field)))

        return self.shotgun.find_one(self.TYPE, [["id", "is", self.id]], [field]).get(field)

    def getFields(self, fields):
        if not isinstance(fields, list):
            raise TypeError("fields must be a list, not {}".format(type(fields)))
            
        return self.shotgun.find_one(self.TYPE, [["id", "is", self.id]], fields)