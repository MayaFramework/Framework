import shotgun_api3 as sapi
from shotgunObject import ShotgunObject
from shot import Shot


class Sequence(ShotgunObject):

    TYPE = "Sequence"
    NAMINGATTR = "code"

    @classmethod
    def createByCode(cls, seqCode):
        shotgun = sapi.Shotgun("https://esdip.shotgunstudio.com",
                                    script_name="shotgunAPI", api_key="f8da64a710923a25352e3d0e06bd31c56395cb5943e03bfaf9a90a73794e1ac1")
        seq = shotgun.find_one(cls.TYPE, [["code", "is", seqCode]], ["code"])
        _id = seq.get("id")
        return cls(seqID=_id, **seq)

    def __init__(self, seqID, **sequenceInfo):
        super(Sequence, self).__init__(seqID, **sequenceInfo)

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
            ["code", "is", "{}.{}".format(self.entityName.lower(), shot)]
            ]
        shot = self.shotgun.find_one("Shot",filters , fields)
        if shot:
            return Shot(**shot)
        return None        

s = Sequence.createByCode("WTF")
print s.id
# print s.image
# print s.getShot("020").entityName
# print s.getShot("020").image