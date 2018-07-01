import shotgun_api3 as sapi


class Sequence(object):

    def __init__(self, code=None, seqID=None, **sequenceInfo):

        self.shotgun = sapi.Shotgun("https://esdip.shotgunstudio.com",
                                    script_name="shotgunAPI", api_key="f8da64a710923a25352e3d0e06bd31c56395cb5943e03bfaf9a90a73794e1ac1")

        self.id = seqID
        self.code = code

        [setattr(self, k,v) for k,v in sequenceInfo.iteritems()]
        
        if not self.id and not self.code:
            raise RuntimeError("At least code or id must be provided")

        elif self.id and not self.code:
            seq = self.shotgun.find_one("Sequence", [["id", "is", self.id]], ["code"])
            self.code = seq.get("code")

        elif not self.id and self.code:
            seq = self.shotgun.find_one("Sequence", [["code", "is", self.code]])
            self.id = seq.get("id")

    def getShots(self, names=False, fields=["code"]):
        shots = self.shotgun.find("Shot", [["sg_sequence", "is", {"type":"Sequence", "id":self.id}]], fields)
        if shots:
            if names:
                return sorted([shot.get("code") for shot in shots])
            return shots
        return None

