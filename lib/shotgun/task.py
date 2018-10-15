from shotgunObject import ShotgunObject


class Task(ShotgunObject):

    TYPE = "Task"
    NAMINGATTR = "content"

    def __init__(self, taskID, **taskInfo):
        super(Task, self).__init__(taskID, **taskInfo)