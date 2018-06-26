import os
from functools import partial
import urllib
import maya.cmds as cmds
import datetime
import threading
from Framework.lib.gui_loader import gui_loader
from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
from Framework.lib.shotgun.shotgunInit import ShotgunInit
# from Framework.plugins.dependency_uploader.uploader_background_widget import UploaderBackgroundWidget
from Framework.lib.logger import logger


from settings import CustomSettings
from filetypes.mayaFile import Maya
from filetypeChooser import FileTypeChooser
from filetypes.folder import Folder
from gui.pathButton import PathButton
from gui import newfileDialog
from gui.siginDialog import SignInDialog
import Framework.plugins.renamer.controller as renamer


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
        self.settings = CustomSettings("BM2", "FileManager")

        self.initUI()
        self.connectSignals()
        self.setSettings()

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
        # self.mainContainer.headerItem().setSizeHint(0, QtCore.QSize(400, 20))
        self.mainContainer.setColumnWidth(0, 400)
        # self.mainContainer.setColumnWidth(1, 200)
        # self.mainContainer.setColumnWidth(2, 100)
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
        # save = os.path.join(ICON_PATH, "essential", "save.png")
        # addFile = os.path.join(ICON_PATH, "add_cloud_green.png")
        addFile = os.path.join(ICON_PATH, "essential", "cloud-computing-2.png")
        self.beforeBT.setIcon(QtGui.QIcon(previousArrow))
        self.afterBT.setIcon(QtGui.QIcon(forwardArrow))
        self.openBT.setIcon(QtGui.QIcon(open))
        self.downloadBT.setIcon(QtGui.QIcon(download))
        # self.saveBT.setIcon(QtGui.QIcon(save))
        self.addFileBT.setIcon(QtGui.QIcon(addFile))

    def setSettings(self):
        if len(self.settings.items()) != 0:
            username = self.settings["userName"]
            login = self.settings["login"]
            password = self.settings["password"]
            if username and password:
                self.userInfo = (username, login, password)
                self.authorizeUser(True)

    def connectSignals(self):
        self.beforeBT.clicked.connect(self._handleBackButton)
        self.mainContainer.itemDoubleClicked.connect(self._itemDoubleClicked)
        self.mainContainer.itemClicked.connect(self._itemClicked)
        self.mainContainer.customContextMenuRequested.connect(self._mainContainerContextMenu)
        self.mainContainer.dropped.connect(self._fileDropped)
        self.actionSignIn.triggered.connect(self._signinDialog)
        self.addFileBT.clicked.connect(self._selectedFileToAdd)
        self.toLocalPathBT.clicked.connect(self.goToLocalPath)

    def _itemDoubleClicked(self, item):
        folderObj = item.data(0, QtCore.Qt.UserRole)
        self.populateMainContainer(fileObj=folderObj)

    def _itemClicked(self, item):
        itemObj = item.data(0, QtCore.Qt.UserRole)
        if isinstance(itemObj, Maya):
            self.showMetadataInfo(itemObj=itemObj)
        self.openBT.setEnabled(itemObj.couldBeOpened)
        self.chkSaveBT.setEnabled(itemObj.couldBeSaved)
        self.outSaveBT.setEnabled(itemObj.couldBeSaved)
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
            # itemData = item.data(0, QtCore.Qt.UserRole)
            itemData = item
        menu = self.generateContextMenu(itemData=itemData)
        menu.move(fixPos(pos ))
        menu.show()

    def _fileDropped(self, files):
        isCorrectDir = self.compareFilesPath(files[0])
        if not isCorrectDir:
            msg = "You are trying to upload a file from<br><br><b>{}</b><br>to<br><b>{}</b><br><br>".format(
                                                            os.path.normpath(self.currentFolder.local_path),
                                                            os.path.normpath(os.path.dirname(files[0]))
                                                        )
            msg += "Please, move the file to the current folder that you have open in the File Explorer\n"
            msg += "or navigate to the file path within the File Explorer"
            QtWidgets.QMessageBox.critical(self, "Check your file/folder!", msg)
        else:
            self.addFiles(files)

    def _signinDialog(self):
        dialog = SignInDialog(self)
        accepted = dialog.exec_()
        if accepted:
            self.userAuthethicated = True
            self.userInfo = (dialog.userName, str(dialog.login), str(dialog.password).encode('base64','strict'))
            self.authorizeUser(enableUI=True)

    def _selectedFileToAdd(self):
        files = QtWidgets.QFileDialog.getOpenFileNames(self, "Select files", "P://BM2")[0]
        if len(files) == 0:
            return
        self._fileDropped(files)

    def closeEvent(self, event):
        self.settings["userName"] = str(self.userInfo[0])
        self.settings["login"] = str(self.userInfo[1])
        self.settings["password"] = str(self.userInfo[2].decode('base64','strict'))
        super(FileManager, self).closeEvent(event)

    def addFiles(self, files):
        dialog = UploaderBackgroundWidget(files, max_threads=5)
        dialog.show()
        dialog.execute_upload_process()

    def authorizeUser(self, enableUI=False):
        sg = ShotgunInit()
        user = sg.getUser(self.userInfo[1])
        try:
            imageURL = user.getField("image")
            data = urllib.urlopen(imageURL).read()
            image = QtGui.QImage()
            image.loadFromData(data)
        except ValueError:
            image = QtGui.QImage()
        self.userImageLB.setPixmap(QtGui.QPixmap(image))
        self.userNameLB.setText(self.userInfo[0])
        if enableUI:
            self._enableUI()
        self.actionSignIn.setText("Change user")

    def _enableUI(self):
        self.centralwidget.setEnabled(True)

    def generateContextMenu(self, itemData):
        menu = QtWidgets.QMenu(self)
        newFileAction = self.createNewAction("Create new File", self.showNewFileDialog, menu)
        menu.addSeparator()
        downloadFile = self.createNewAction("Download", self.downloadFile, menu)
        downloadFileOnly = self.createNewAction("Download File only", self.downloadFile, menu)
        downloadDependencies = self.createNewAction("Download Dependencies only", self.downloadFile, menu)
        menu.addSeparator()
        self.createNewAction("Open", self.openFile, menu)
        if not isinstance(itemData, Maya):
            newFileAction.setDisabled(True)
            downloadFileOnly.setDisabled(True)
            downloadDependencies.setDisabled(True)
        if itemData:
            menu.addAction("Copy path", partial(self.copyPath, itemData))
        return menu

    def createNewAction(self, actionName, connectTo, menu):
        newAction = QtWidgets.QAction(actionName, menu)
        newAction.triggered.connect(connectTo)
        menu.addAction(newAction)
        return newAction

    def copyPath(self, itemData):
        itemData = itemData.data(0, QtCore.Qt.UserRole)
        clipboard = QtGui.QClipboard()
        clipboard.setText(os.path.normpath(itemData.local_path))

    def showNewFileDialog(self):
        dialog = newfileDialog.NewFileDialog(parent=self)
        response = dialog.exec_()
        if response:
            dialog.newFile.save(force=True, create_snapshot=False, checkPaths=False, isNewfile=True, author=self.userInfo[0])

    def compareFilesPath(self, file):
        currentFolderDir = os.path.normpath(self.currentFolder.local_path).lower()
        fileFolderDir = os.path.normpath(os.path.dirname(file)).lower()
        return True if str(currentFolderDir) == str(fileFolderDir) else False

    def goToLocalPath(self):
        currentScene = os.path.dirname(cmds.file(q=True, sn=True))
        currentScene = os.path.normpath(currentScene)
        try:
            self.toFolderPath(currentScene)
        except:
            pass

    def verifyScenePath(self):
        if not isinstance(self.selectedItem, Folder):
            path = os.path.normpath(self.selectedItem.local_path).replace("\\", "/")
            print path
            sceneName = os.path.basename(path)
            rename = renamer.Renamer()
            fields = rename.get_fields_from_file_path(path)
            fileName = rename.generate_file_name(fields)
            if sceneName.split(".")[0] == fileName.split(".")[0]:
                return True
            else:
                fixedPath = rename.generate_complete_file_path(fields)
                msg = "You are trying to upload a file with the wrong naming convention.\n"
                msg += "Please, rename the scene with the following name\n\n"
                msg += "{}".format(fixedPath)
                logger.error(msg)
                return False

    def openFile(self):
        if os.path.isfile(self.selectedItem.local_path):
            msg = "It looks like the path <br><b>{}</b><br>exists in local.<br>".format(self.selectedItem.local_path)
            msg +="Do you want to download the scene anyway?"
            response = QtWidgets.QMessageBox.warning(self,
                                                     "Local scene found!",
                                                     msg,
                                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                     QtWidgets.QMessageBox.Yes)
            if response == QtWidgets.QMessageBox.Yes:
                self.selectedItem.open()
            else:
                self.selectedItem.openScene()
        else:
            self.selectedItem.open()

    def saveFile(self, out=False, chk=False):
        verifiedPath = self.verifyScenePath()
        if verifiedPath:
            self.selectedItem.save(author=self.userInfo[0], publish2Chk=chk, publish2Out=out)

    def publishOut(self):
        self.saveFile(out=True, chk=False)

    def publishChk(self):
        self.saveFile(out=False, chk=True)

    def downloadFile(self):
        self.selectedItem.download()

    def populateMainContainer(self, fileObj, addHistory=True):
        if isinstance(fileObj, Folder):
            self.currentFolder = fileObj
            self.mainContainer.clear()
            self.mainContainer.setIconSize(QtCore.QSize(200,200))
            for childFile, childDpxMetadata in fileObj.remote_children:
                listItem = QtWidgets.QTreeWidgetItem(self.mainContainer)
                fileInstance, fileWidget = FileTypeChooser.getClass(childFile, includeWidget=True)
                newFile = fileInstance(childFile)
                newFileWidget = fileWidget(newFile, parent=self.mainContainer)
                self.setItemData(item=listItem,
                                 data=newFile,
                                 parentTree=self.mainContainer,
                                 widget=newFileWidget,
                                 dropboxMetadata=childDpxMetadata)
            if addHistory:
                self.addFolder2History(fileObj)

    def toFolderPath(self, path):
        fileInstance, fileWidget = FileTypeChooser.getClass(path, includeWidget=True)
        pathObj = fileInstance(path)
        self.populateMainContainer(fileObj=pathObj)

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

    def setItemData(self, item, data, parentTree, widget=None, dropboxMetadata=None):
        item.setData(0, QtCore.Qt.UserRole, data)
        parentTree.addTopLevelItem(item)
        if dropboxMetadata:
            if hasattr(dropboxMetadata, "client_modified"):
                date = getattr(dropboxMetadata, "client_modified")
                item.setText(1, str(date))
            if hasattr(dropboxMetadata, "size"):
                size = getattr(dropboxMetadata, "size")
                size = float(size)/1000000
                item.setText(2, "{0:.2f}MB".format(size))
        if widget:
            parentTree.setItemWidget(item, 0, widget)
            widgetSize = widget.sizeHint()
            item.setSizeHint(0, QtCore.QSize(widgetSize.width() + 20, widgetSize.height()))
        for column in xrange(parentTree.columnCount()):
            parentTree.resizeColumnToContents(column)

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


if __name__ == "__main__":
    from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
    import sys
    from Framework.lib.gui_loader import gui_loader

    app = QtWidgets.QApplication(sys.argv)
    widget = FileManager()
    obj = gui_loader.get_default_container(widget, "UPLOADER")
    obj.show()
    app.exec_()
