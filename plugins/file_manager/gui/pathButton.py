from PySide2 import QtWidgets

class PathButton(QtWidgets.QPushButton):

    def __init__(self, folderObj, parent=None):
        super(PathButton, self).__init__(parent)

        self.folderObj = folderObj

        self.setText(folderObj.name)