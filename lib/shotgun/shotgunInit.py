import shotgun_api3 as sapi
from Framework.lib.shotgun.user import ShotgunUser, User
from Framework.lib.shotgun.sequence import Sequence


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

    def getUserV2(self, loginName):
        user = self.shotgun.find_one("HumanUser", filters=[["login", "is", loginName]], fields=["login", "name"])
        if user:
            return User(user.get("id"), **user)
        return None

    def getSeqs(self, names=False, fields=["code"]):
        seqs = self.shotgun.find("Sequence", [["project", "is", {"type":"Project", "id":86}]], fields)
        if seqs:
            if names:
                return sorted([seq.get("code") for seq in seqs])
            return [Sequence(seq.get("id"), **seq) for seq in seqs]
        return None

    def getSeq(self, sequence, fields=["code"]):
        seq = self.shotgun.find_one("Sequence", [["code", "is", sequence]], fields)
        if seq:
            _id = seq.get("id")
            return Sequence(_id, **seq)
        return None

# s = ShotgunInit()
# # seq = s.getSeq("WTF")
# # print seq
# # shot = seq.getShot("020")
# # print shot.getTask("Light")

# user = s.getUserV2("asierra")
# print user.getTasks()[0]
# # print s.getUserV2("asierra").getTasks()
# # sType = "HumanUser"
# # filters = [["name", "is", "Dalia Gutierrez"]]
# # user = s.shotgun.find_one(sType, filters)
# # # print user
# # print s.shotgun.find_one("Task",  , ["content", "entity", "sg_status_list"])