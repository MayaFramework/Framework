import shotgun_api3

class ShotgunUser(object):
    
    def __init__(self, shotgunObj, **userEntity):

        self.shotgunObj = shotgunObj
        self.userEntity = userEntity
        self._name = userEntity.get("name", None)
        self._login = userEntity.get("login", None)
        self._id = userEntity.get("id", None)
        self._entityType = userEntity.get("type", "HumanUser")

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        self._login = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def entityType(self):
        return self._entityType

    @entityType.setter
    def entityType(self, value):
        self._entityType = value

    def authenticate(self, password):
        return self.shotgunObj.authenticate_human_user(user_login=self.login, user_password=password)

    def getField(self, fieldName):
        field = self.shotgunObj.find_one(
                        self.entityType, filters=[["name", "is", self.name]], fields=[fieldName])
        if not field.get(fieldName):
            raise ValueError("Can't find {} in the type entity {}".format(fieldName, self.entityType))
        return {fieldName:field.get(fieldName)}

    def getFields(self, fieldsNames):
        fieldsDict = dict()
        for field in fieldsNames:
            fieldDict = self.getField(field)
            fieldsDict.update(fieldDict)
        return fieldsDict

    def getUserImage(self):
        return self.getField("image")
