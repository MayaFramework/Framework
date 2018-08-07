import shotgun_api3 as sapi

class NotRegisteredUser(sapi.ShotgunError):
    pass


class NotValidField(sapi.ShotgunError):
    pass
        