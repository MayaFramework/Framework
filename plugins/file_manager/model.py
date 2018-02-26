import os

from Framework.lib.gui_loader import gui_loader
from PySide2 import QtCore, QtGui, QtWidgets

from filetypes.mayaFile import Maya
from filetypeChooser import FileTypeChooser
from filetypes.folder import Folder
from gui.pathButton import PathButton

from Framework import get_icon_path

ICON_PATH = get_icon_path()
PROJECT_ROOT = "bm2"

form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "gui", "main.ui"))


class FileManager(form, base):

    def __init__(self):
        super(FileManager, self).__init__()
        self.setupUi(self)

        self._currentFolder = None
        self._selectedItem = None
        self.history = list()
        self.pathBar = list()

        self.initUI()
        self.connectSignals()

    @property
    def selectedItem(self):
        return self._selectedItem

    @selectedItem.setter
    def selectedItem(self, value):
        self._selectedItem = value

    @property
    def currentFolder(self):
        return self._currentFolder

    @currentFolder.setter
    def currentFolder(self, value):
        self._currentFolder = value

    def initUI(self):
        self._setIcons()
        initialFolder = Folder(PROJECT_ROOT)
        self.currentFolder = initialFolder
        self.populateMainContainer(initialFolder)

    def _setIcons(self):
        previousArrow = os.path.join(ICON_PATH, "left-arrow.png")
        forwardArrow = os.path.join(ICON_PATH, "right-arrow.png")
        open = os.path.join(ICON_PATH, "open_icon.png")
        download = os.path.join(ICON_PATH, "download_icon.png")
        save = os.path.join(ICON_PATH, "save_icon_2.png")
        self.beforeBT.setIcon(QtGui.QIcon(previousArrow))
        self.afterBT.setIcon(QtGui.QIcon(forwardArrow))
        self.openBT.setIcon(QtGui.QIcon(open))
        self.downloadBT.setIcon(QtGui.QIcon(download))
        self.saveBT.setIcon(QtGui.QIcon(save))

    def connectSignals(self):
        self.beforeBT.clicked.connect(self._handleBackButton)
        self.mainContainer.itemDoubleClicked.connect(self._itemDoubleClicked)
        self.mainContainer.itemClicked.connect(self._itemClicked)
        self.openBT.clicked.connect(self.openFile)
        self.saveBT.clicked.connect(self.saveFile)
        self.downloadBT.clicked.connect(self.downloadFile)

    def _itemDoubleClicked(self, item):
        folderObj = item.data(QtCore.Qt.UserRole)
        self.populateMainContainer(folderObj=folderObj)

    def _itemClicked(self, item):
        itemObj = item.data(QtCore.Qt.UserRole)
        if isinstance(itemObj, Maya):
            self.showMetadataInfo(itemObj=itemObj)
        self.openBT.setEnabled(itemObj.couldBeOpened)
        self.saveBT.setEnabled(itemObj.couldBeSaved)
        self.downloadBT.setEnabled(itemObj.couldBeDownloaded)
        self.selectedItem = itemObj

    def _handleBackButton(self):
        self.history.pop(-1)
        previousFolder = self.history[-1]
        self.populateMainContainer(previousFolder, addHistory=False)

    def _pathButtonClicked(self):
        pathButton = self.sender()
        self._refreshPathBar(pathButton)
        self.populateMainContainer(folderObj=pathButton.folderObj, addHistory=False)

    def openFile(self):
        self.selectedItem.open()

    def saveFile(self):
        self.selectedItem.save()

    def downloadFile(self):
        self.selectedItem.download()

    def populateMainContainer(self, folderObj, addHistory=True):
        self.currentFolder = folderObj
        self.mainContainer.clear()
        self.mainContainer.setIconSize(QtCore.QSize(200,200))
        for childFile in folderObj.remote_children:
            listItem = QtWidgets.QListWidgetItem()
            fileObj, fileWidget = FileTypeChooser.getClass(childFile, includeWidget=True)
            newFile = fileObj(childFile)
            newFileWidget = fileWidget(newFile)
            self.setItemData(item=listItem,
                             data=newFile,
                             parentTree=self.mainContainer,
                             widget=newFileWidget)
        if addHistory:
            self.addFolder2History(folderObj)

    def showMetadataInfo(self, itemObj):
        if not hasattr(itemObj, "metadata"):
            self.thumbnailLB.setPixmap(QtGui.QPixmap())
            self.thumbnailLB.setText("No Thumbnail")
            self.userLB.setText("No metadata")
            self.nameLB.setText("No metadata")
            self.dateLB.setText("No metadata")
            self.versionLB.setText("No metadata")
        else:
            ba = QtCore.QByteArray.fromBase64(str(itemObj.metadata.image))
            img = QtGui.QPixmap()
            img.loadFromData(ba)
            self.thumbnailLB.setPixmap(QtGui.QPixmap(img))
            self.userLB.setText(itemObj.metadata.author)
            self.nameLB.setText(os.path.basename(itemObj.metadata.scene_path))
            self.dateLB.setText(itemObj.metadata.modified)
            self.versionLB.setText(itemObj.metadata.scene_version)

    def addFolder2History(self, folder):
        self.history.append(folder)
        pathButton = PathButton(folder)
        pathButton.clicked.connect(self._pathButtonClicked)
        self.pathLayout.addWidget(pathButton)
        self.pathBar.append(pathButton)

    def setItemData(self, item, data, parentTree, widget=None):
        item.setData(QtCore.Qt.UserRole, data)
        parentTree.addItem(item)
        if widget:
            parentTree.setItemWidget(item, widget)
            item.setSizeHint(widget.sizeHint())

    def _refreshPathBar(self, pathButton):
        found = False
        for button in self.pathBar:
            if button == pathButton:
                found = True
                continue
            if found:
                button.setParent(None)
                index = self.pathLayout.indexOf(button)
                self.pathLayout.takeAt(index)
