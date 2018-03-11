import shotgun_api3 as sapi
from user import ShotgunUser

class ShotgunInit(object):
    def __init__(self):
        
        # TODO Change my credentials with the admin ones
        self.shotgun = sapi.Shotgun("https://esdip.shotgunstudio.com",
                                    script_name="shotgunAPI", api_key="f8da64a710923a25352e3d0e06bd31c56395cb5943e03bfaf9a90a73794e1ac1")

    def getUser(self, userName):
        user = self.shotgun.find_one("HumanUser", filters=[["name", "is", userName]], fields=["login", "name"])
        if user:
            return ShotgunUser(self.shotgun, **user)
        return None

        
