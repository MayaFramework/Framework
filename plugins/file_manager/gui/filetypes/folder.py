from generic import GenericWidget
import os
from Framework import get_icon_path


ICON_PATH = get_icon_path()


class FolderWidget(GenericWidget):

    ICON = os.path.join(ICON_PATH, "folder.png")

    def __init__(self, folderObj, icon=ICON, parent=None):
        super(FolderWidget, self).__init__(folderObj, icon=icon, parent=parent)





