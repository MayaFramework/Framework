import shotgun_api3 as sapi
from Framework.lib.shotgun.user import ShotgunUser


class ShotgunInit(object):
    
    def __init__(self):
        
        # TODO Change my credentials with the admin ones
        self.shotgun = sapi.Shotgun("https://esdip.shotgunstudio.com",
                                    script_name="shotgunAPI", api_key="f8da64a710923a25352e3d0e06bd31c56395cb5943e03bfaf9a90a73794e1ac1")

    def getUser(self, loginName):
        user = self.shotgun.find_one("HumanUser", filters=[["login", "is", loginName]], fields=["login", "name"])
        if user:
            return ShotgunUser(self.shotgun, **user)
        return None

    def getSeqs(self, names=False, fields=["code"]):
        seqs = self.shotgun.find("Sequence", [["project", "is", {"type":"Project", "id":86}]], fields)
        if names:
            return sorted([seq.get("code") for seq in seqs])
        return seqs

    def getSeq(self, sequence, fields=["code"]):
        return self.shotgun.find_one("Sequence", [["code", "is", sequence]], fields)

    def getShots(self, sequence, names=False, fields=["code"]):
        sequenceObj = self.getSeq(sequence)
        if sequenceObj:
            shots = self.shotgun.find("Shot", [["sg_sequence", "is", {"type":"Sequence", "id":sequenceObj.get("id")}]], fields)
            if names:
                return sorted([shot.get("code") for shot in shots])
            return shots
        return None


        
