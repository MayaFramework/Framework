from generic import GenericWidget
import os
from Framework import get_icon_path

from Framework.lib.gui_loader import gui_loader


form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "ui", "folder.ui"))

ICON_PATH = get_icon_path()


class FolderWidget(form, GenericWidget):

    ICON = os.path.join(ICON_PATH, "folder.png")

    def __init__(self, folderObj, icon=ICON, parent=None, initialize=False):
        super(FolderWidget, self).__init__(folderObj, icon=icon, parent=parent, initialize=initialize)
        self.setupUi(self)

        self.initUI()
        self.connectSignals()

    def connectSignals(self):
        self.favouriteBT.favourited.connect(self.markAsFavourite)

    def markAsFavourite(self):
        print self.parent()
        print self.parent().parent()
        print self.fileObj







