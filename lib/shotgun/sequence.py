import shotgun_api3 as sapi
from shotgunObject import ShotgunObject
from shot import Shot


class Sequence(ShotgunObject):

    TYPE = "Sequence"

    def __init__(self, code=None, seqID=None, **sequenceInfo):
        super(Sequence, self).__init__(code=code, objectID=seqID, **sequenceInfo)

    def getShots(self, names=False, **fields):
        fields = fields if fields else ["code", "assets", "description", "sg_status_list", "image"]
        shots = self.shotgun.find("Shot", [["sg_sequence", "is", {"type":"Sequence", "id":self.id}]], fields)
        if shots:
            if names:
                return sorted([shot.get("code") for shot in shots])
            return [Shot(**shots) for shot in shots]
        return None

    def getShot(self, shot, **fields):
        fields = fields if fields else ["code", "assets", "description", "sg_status_list", "image"]
        filters = [
            ["sg_sequence", "is", {"type":"Sequence", "id":self.id}], 
            ["code", "is", "{}.{}".format(self.code.lower(), shot)]
            ]
        shot = self.shotgun.find_one("Shot",filters , fields)
        if shot:
            return Shot(**shot)
        return None        

# s = Sequence(code="WTF")
# print s.getShot("020").image