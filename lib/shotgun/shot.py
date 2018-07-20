import shotgun_api3 as sapi
from shotgunObject import ShotgunObject


class Shot(ShotgunObject):

    TYPE = "Shot"
    NAMINGATTR = "code"

    def __init__(self, shotID=None, **shotInfo):
        super(Shot, self).__init__(shotID, **shotInfo)

        self._image = shotInfo.pop("image", None)
        self._status = shotInfo.pop("status", None)
        # self._name = shotInfo.pop("code", None)

    @property
    def image(self):
        if not self._image:
            image = self.getField("image")
            if image:
                self._image = image
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def status(self):
        if not self._status:
            status = self.getField("status")
            if status:
                self._status = status
        return self._status    

    @status.setter
    def status(self, value):
        self._status = value

    def getTasks(self, names=False, **fields):
        fields = fields if fields else ['content','start_date','due_date']
        tasks = self.shotgun.find("Task", [["entity", "is", {"type":"Shot", "id":self.id}]], fields)
        if tasks:
            if names:
                return sorted([task.get("content") for task in tasks])
            return tasks
        return None

    def getTask(self, taskName, **fields):
        fields = fields if fields else ['content','start_date','due_date', "task_assignees"]
        filters =   [
                        ["entity", "is", {"type":"Shot", "id":self.id}], 
                        ["content", "is", taskName]
                    ]
        task = self.shotgun.find_one("Task", filters, fields)
        return task if task else None


# s = Shot(code="tst.180")
# print s.getField("open_notes")
# print s.image
# print s.getTask("FX")

# fields = [
#     'content',
#     'start_date',
#     'due_date'
#     ]

# print s.shotgun.find_one("Task", [["entity", "is", {"type":"Shot", "id":s.id}], ["content", "is", "Layout"]], fields)
