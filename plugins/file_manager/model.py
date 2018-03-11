import os
from functools import partial
import urllib
import threading
from Framework.lib.gui_loader import gui_loader
from PySide2 import QtCore, QtGui, QtWidgets
from Framework.lib.shotgun.shotgunInit import ShotgunInit
from Framework.plugins.dependency_uploader.uploader_background_widget import UploaderBackgroundWidget


from filetypes.mayaFile import Maya
from filetypeChooser import FileTypeChooser
from filetypes.folder import Folder
from gui.pathButton import PathButton
from gui import newfileDialog; reload(newfileDialog)
from gui.siginDialog import SignInDialog

from Framework import get_icon_path

ICON_PATH = get_icon_path()

NOTHUMBNAIL = os.path.join(ICON_PATH, "no-image.png")
PROJECT_ROOT = "bm2"

form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "gui", "main.ui"))


class FileManager(form, base):

    def __init__(self):
        super(FileManager, self).__init__()
        self.setupUi(self)

        self._currentFolder = None
        self._selectedItem = None
        self._userAuthenticated = False
        self._userInfo = None
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

    @property
    def userAuthethicated(self):
        return self._userAuthenticated

    @userAuthethicated.setter
    def userAuthethicated(self, value):
        self._userAuthenticated = value

    @property
    def userInfo(self):
        return self._userInfo

    @userInfo.setter
    def userInfo(self, value):
        if not isinstance(value, tuple):
            raise TypeError("userInfo must be a tuple, not {}".format(type(value)))
        self._userInfo = value

    def initUI(self):
        self.mainContainer.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._setIcons()
        self.thumbnailLB.setPixmap(QtGui.QPixmap(NOTHUMBNAIL))
        initialFolder = Folder(PROJECT_ROOT)
        self.currentFolder = initialFolder
        self.populateMainContainer(initialFolder)

    def _setIcons(self):
        previousArrow = os.path.join(ICON_PATH, "left-arrow.png")
        forwardArrow = os.path.join(ICON_PATH, "right-arrow.png")
        # open = os.path.join(ICON_PATH, "open_icon.png")
        open = os.path.join(ICON_PATH, "essential", "folder-10.png")
        # download = os.path.join(ICON_PATH, "download_icon.png")
        download = os.path.join(ICON_PATH, "essential", "download.png")
        # save = os.path.join(ICON_PATH, "save_icon_2.png")
        save = os.path.join(ICON_PATH, "essential", "save.png")
        # addFile = os.path.join(ICON_PATH, "add_cloud_green.png")
        addFile = os.path.join(ICON_PATH, "essential", "cloud-computing-2.png")
        self.beforeBT.setIcon(QtGui.QIcon(previousArrow))
        self.afterBT.setIcon(QtGui.QIcon(forwardArrow))
        self.openBT.setIcon(QtGui.QIcon(open))
        self.downloadBT.setIcon(QtGui.QIcon(download))
        self.saveBT.setIcon(QtGui.QIcon(save))
        self.addFileBT.setIcon(QtGui.QIcon(addFile))

    def connectSignals(self):
        self.beforeBT.clicked.connect(self._handleBackButton)
        self.mainContainer.itemDoubleClicked.connect(self._itemDoubleClicked)
        self.mainContainer.itemClicked.connect(self._itemClicked)
        self.openBT.clicked.connect(self.openFile)
        self.saveBT.clicked.connect(self.saveFile)
        self.downloadBT.clicked.connect(self.downloadFile)
        self.mainContainer.customContextMenuRequested.connect(self._mainContainerContextMenu)
        self.mainContainer.dropped.connect(self._fileDropped)
        self.actionSignIn.triggered.connect(self._signinDialog)
        self.addFileBT.clicked.connect(self._selectedFileToAdd)

    def _itemDoubleClicked(self, item):
        folderObj = item.data(QtCore.Qt.UserRole)
        self.populateMainContainer(fileObj=folderObj)

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
        self.populateMainContainer(fileObj=pathButton.folderObj, addHistory=False)

    def _mainContainerContextMenu(self, pos):

        def fixPos(pos):
            newPos = self.mainContainer.mapToGlobal(pos)
            x = newPos.x() + 13
            y = newPos.y() + 13
            return QtCore.QPoint(x, y)

        item = self.mainContainer.itemAt(pos)
        itemData = None
        if item:
            itemData = item.data(QtCore.Qt.UserRole)
        menu = self.generateContextMenu(itemData=itemData)
        menu.move(fixPos(pos))
        menu.show()

    def _fileDropped(self, files):
        # TODO This method will add all the files to Dropbox
        self.addFiles(files)

    def _signinDialog(self):
        dialog = SignInDialog(self)
        accepted = dialog.exec_()
        if accepted:
            self.userAuthethicated = True
            self.userInfo = (dialog.userName, str(dialog.password).encode('base64','strict'))
            self.authorizeUser(enableUI=True)

    def _selectedFileToAdd(self):
        files = QtWidgets.QFileDialog.getOpenFileNames(self, "Select files", "P://BM2")
        if len(files[0]) == 0:
            return
        self.addFiles(files[0])


    def addFiles(self, files):
        """
        TODO Hay que ver si queremos anadir los files a la carpeta en la que estamos, o recrear el path del file
        :param file:
        :return:
        """
        dialog = UploaderBackgroundWidget(files, max_threads=5)
        dialog.show()
        dialog.execute_upload_process()

    def authorizeUser(self, enableUI=False):
        sg = ShotgunInit()
        user = sg.getUser(self.userInfo[0])
        imageURL = user.getField("image")
        data = urllib.urlopen(imageURL).read()
        image = QtGui.QImage()
        image.loadFromData(data)
        self.userImageLB.setPixmap(QtGui.QPixmap(image))
        self.userNameLB.setText(self.userInfo[0])
        if enableUI:
            self._enableUI()

    def _enableUI(self):
        self.centralwidget.setEnabled(True)

    def generateContextMenu(self, itemData):
        print self.currentFolder.local_path
        menu = QtWidgets.QMenu(self)
        newFileAction = self.createNewAction("Create new File", self.showNewFileDialog, menu)
        if len(os.path.normpath(self.currentFolder.local_path).replace("\\", '/').split("/")) != 8:
            newFileAction.setDisabled(True)
        if itemData:
            menu.addAction("Copy path", partial(self.copyPath, itemData))
        return menu

    def createNewAction(self, actionName, connectTo, menu):
        newAction = QtWidgets.QAction(actionName, menu)
        newAction.triggered.connect(connectTo)
        menu.addAction(newAction)
        return newAction

    def copyPath(self, itemData):
        clipboard = QtGui.QClipboard()
        clipboard.setText(os.path.normpath(itemData.local_path))

    def showNewFileDialog(self):
        dialog = newfileDialog.NewFileDialog(parent=self)
        response = dialog.exec_()
        if response:
            dialog.newFile.save(force=True, create_snapshot=True, checkPaths=False, isNewfile=True, author=self.userInfo[0])

    def openFile(self):
        self.selectedItem.open()

    def saveFile(self):
        self.selectedItem.save(author=self.userInfo[0])

    def downloadFile(self):
        self.selectedItem.download()

    def populateMainContainer(self, fileObj, addHistory=True):
        if isinstance(fileObj, Folder):
            self.currentFolder = fileObj
            self.mainContainer.clear()
            self.mainContainer.setIconSize(QtCore.QSize(200,200))
            for childFile in fileObj.remote_children:
                listItem = QtWidgets.QListWidgetItem()
                fileInstance, fileWidget = FileTypeChooser.getClass(childFile, includeWidget=True)
                newFile = fileInstance(childFile)
                newFileWidget = fileWidget(newFile)
                self.setItemData(item=listItem,
                                 data=newFile,
                                 parentTree=self.mainContainer,
                                 widget=newFileWidget)
            if addHistory:
                self.addFolder2History(fileObj)

    def showMetadataInfo(self, itemObj):
        if not hasattr(itemObj, "metadata"):
            self.thumbnailLB.setPixmap(QtGui.QPixmap(NOTHUMBNAIL))
            # self.thumbnailLB.setText("No Thumbnail")
            self.userLB.setText("No metadata")
            self.dateLB.setText("No metadata")
            self.versionLB.setText("No metadata")
        else:
            ba = QtCore.QByteArray.fromBase64(str(itemObj.metadata.image))
            img = QtGui.QPixmap()
            img.loadFromData(ba)
            self.thumbnailLB.setPixmap(QtGui.QPixmap(img))
            self.userLB.setText(itemObj.metadata.author)
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
