
from Framework.lib.gui_loader import gui_loader
import os
from ..core import scene
from PySide2 import QtCore, QtGui, QtWidgets
from Framework.plugins.dependency_loader.dependency_loader_window import DependencyLoaderWidget
import maya.cmds as cmds


form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "scene_widget.ui"))


class FileWidget(form, base):

    OPENICON = QtGui.QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "icons/open_icon.png"))
    DOWNLOAD = QtGui.QIcon(os.path.join(os.path.dirname(os.path.realpath(__file__)), "icons/download_icon.png"))

    def __init__(self, fileInstance, mainUi):
        super(FileWidget, self).__init__()
        self.setupUi(self)

        self.__isMayaScene = True if isinstance(fileInstance, scene.Scene) else False
        self.fileInstance = fileInstance
        self.mainUi = mainUi

        self.__default_state_window()
        self.__connect_default_signals()

    @property
    def metadata(self):
        if self.__isMayaScene:
            return self.fileInstance.metadata
        else:
            return None

    def __default_state_window(self):
        self.openBT.setIcon(self.OPENICON)
        self.downloadBT.setIcon(self.DOWNLOAD)
        if hasattr(self.fileInstance, "icon") and getattr(self.fileInstance, "icon"):
            self.extensionImageLB.setPixmap(QtGui.QPixmap(self.fileInstance.icon))
        else:
            self.extensionImageLB.setText(self.fileInstance.extension.upper())
        if self.metadata:
            self.__set_image()
        if not self.__isMayaScene:
            self.openBT.setEnabled(False)
            self.sceneLB.setText(self.fileInstance.name)
        else:
            self.openBT.setEnabled(True)
            self.sceneLB.setText(self.fileInstance.scene_name)

    def __connect_default_signals(self):
        self.openBT.clicked.connect(self.open_scene)
        self.downloadBT.clicked.connect(self.download_scene)

    def __set_image(self):
        ba = QtCore.QByteArray.fromBase64(str(self.metadata.image))
        img = QtGui.QPixmap()
        img.loadFromData(ba)
        self.iconLB.setPixmap(img)

    def open_scene(self):
        self.download_scene()
        cmds.file(self.fileInstance.local_path, o=True, f=True)

    def download_scene(self):
        tool = DependencyLoaderWidget(self.fileInstance.local_path)
        self.obj = gui_loader.get_default_container(tool, "Update All")
        self.obj.show()
        tool.execute_update_process()