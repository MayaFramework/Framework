from Framework.lib.ext_lib import shotgun_api3 as sapi

class NotRegisteredUser(sapi.ShotgunError):
    pass


class NotValidField(sapi.ShotgunError):
    pass
        