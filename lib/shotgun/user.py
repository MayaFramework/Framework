import shotgun_api3
from shotgunObject import ShotgunObject
from shotgunExceptions import NotRegisteredUser
from task import Task


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
        return True if self.shotgunObj.authenticate_human_user(user_login=self.login, user_password=password) else False

    def getField(self, fieldName):
        field = self.shotgunObj.find_one(
                        self.entityType, filters=[["name", "is", self.name]], fields=[fieldName])
        if not field.get(fieldName):
            raise ValueError("Can't find {} in the type entity {}".format(fieldName, self.entityType))
        return field.get(fieldName)

    def getFields(self, fieldsNames):
        fieldsDict = dict()
        for field in fieldsNames:
            fieldValue = self.getField(field)
            fieldsDict.update({field:fieldValue})
        return fieldsDict

    def getUserImage(self):
        return self.getField("image")


class User(ShotgunObject):

    TYPE = "HumanUser"
    NAMINGATTR = "name"

    def __init__(self, userID, **userInfo):
        super(User, self).__init__(userID, **userInfo)

    def getTasks(self):
        if not hasattr(self, "userName"):
            user = self.shotgun.find_one("HumanUser", filters=[["id", "is", self.id]], fields=["login", "name"])
            if not user:
                raise NotRegisteredUser("Can't find user with id {}".format(self.id))
            userName = user.get("name")
            setattr(self, "userName", userName)

        filters = [
            ["project", "is", {"type":"Project", "id":86}], 
            ["task_assignees", "name_contains", self.userName]
            ]

        fields = [
            "content",
            "entity", 
            "sg_status_list"
            ]

        tasks = self.shotgun.find("Task", filters, fields)
        if tasks:
            return [Task(task.get("id"), **task) for task in tasks]

        return None

