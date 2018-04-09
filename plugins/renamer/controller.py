import os

class Renamer(object):
    def __init__(self, sceneFolder):

        self.sceneFolder = sceneFolder
        self.validSceneName = self.generateFileName()
        if self.validSceneName:
            fields = self.validSceneName.split(".")[0].split("_")
            self.show = fields[0]
            self.departmentTask = fields[1]
            self.department = fields[2]
            self.asset= fields[3]
            self.task = fields[4]
            self.details = fields[5]
            self.main = fields[6]
            self.comment1 = fields[7]
            self.comment2 = fields[8]
            self.folder = fields[9]

    def generateFileName(self):
        try:
            root, show, department, asset, task, details, main, folder = self.sceneFolder.split("/")
            folderPath = "{show}_{department}{task}_{department}_{asset}_{task}_{details}_{main}_default_none_{folder}.ma".format(
                **locals()).lower()
            return folderPath
        except:
            return None

    def compare(self, mayaScene):
        if not self.validSceneName:
            return False
        correctMayaSceneName = os.path.basename(mayaScene).split(".")[0]
        sceneFields = correctMayaSceneName.split("_")
        print sceneFields
        show = sceneFields[0]
        departmentTask = sceneFields[1]
        department = sceneFields[2]
        asset= sceneFields[3]
        task = sceneFields[4]
        details = sceneFields[5]
        main = sceneFields[6]
        folder = sceneFields[9]
        for k, v in locals().iteritems():
            if not hasattr(self, k):
                continue
            if v.lower() != getattr(self, k).lower():
                return False
        return True


