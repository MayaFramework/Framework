import os
from functools import partial
import urllib
import datetime
import threading
from Framework.lib.gui_loader import gui_loader
from Framework.lib.ui.qt.QT import QtCore, QtWidgets, QtGui
from Framework.lib.shotgun.shotgunInit import ShotgunInit
from Framework.plugins.dependency_loader.dependency_loader_window import DependencyLoaderWidget
from Framework.lib.dropbox_manager.manager import DropboxManager


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
PROJECT_ROOT = "/work/bm2"

form, base = gui_loader.load_ui_type(os.path.join(
    os.path.dirname(__file__), "gui", "main.ui"))

class FileManager(form, base):

    DOWNLOAD = 0
    DOWNLOAD_FILE_ONLY = 1
    DOWNLOAD_DEPENDENCIES_ONLY = 2

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
        self.beforeBT.setIcon(QtGui.QIcon(previousArrow))
        self.afterBT.setIcon(QtGui.QIcon(forwardArrow))

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
        self.pathLE.returnPressed.connect(self.pathChanged)
        self.createFileBT.clicked.connect(self.showNewFileDialog)

    def _itemDoubleClicked(self, item):
        folderObj = item.data(0, QtCore.Qt.UserRole)
        print folderObj.local_path, folderObj.remote_path
        self.populateMainContainer(fileObj=folderObj)

    def _itemClicked(self, item):
        itemObj = item.data(0, QtCore.Qt.UserRole)
        if isinstance(itemObj, Maya):
            self.showMetadataInfo(itemObj=itemObj)
        self.selectedItem = itemObj

    def _handleBackButton(self):
        self.history.pop(-1)
        previousFolder = self.history[-1]
        self.populateMainContainer(previousFolder, addHistory=False)
        self.pathLE.setText(os.path.normpath(previousFolder.local_path).replace("\\", "/"))

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

    def pathChanged(self):
        path = os.path.normpath(self.pathLE.text()).replace("\\", "/")

        folderObj = Folder(path=path)
        self.populateMainContainer(fileObj=folderObj, addHistory=True)
        self.selectedItem = folderObj

    def refresh(self):
        self.populateMainContainer(fileObj=self.selectedItem, addHistory=True)

    def _fileDropped(self, files):
        # isCorrectDir = self.compareFilesPath(files[0])
        # if not isCorrectDir:
        #     msg = "You are trying to upload a file from<br><br><b>{}</b><br>to<br><b>{}</b><br><br>".format(
        #                                                     os.path.normpath(self.currentFolder.local_path),
        #                                                     os.path.normpath(os.path.dirname(files[0]))
        #                                                 )
        #     msg += "Please, move the file to the current folder that you have open in the File Explorer\n"
        #     msg += "or navigate to the file path within the File Explorer"
        #     QtWidgets.QMessageBox.critical(self, "Check your file/folder!", msg)
        # else:
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
        dpx = DropboxManager()
        for selectedFile in files:
            if not os.path.isdir(os.path.dirname(selectedFile)):
                os.makedirs(os.path.dirname(selectedFile))

            newFileLocation = os.path.normpath(os.path.join(self.selectedItem.remote_path, os.path.basename(selectedFile))).replace("\\", "/")
            dpx.uploadFile(local_file=os.path.normpath(selectedFile), target_file=newFileLocation, check_repository=False)
        QtWidgets.QMessageBox.information(self, "Upload Succesfully", "Files uploaded succesfully to {}".format(self.selectedItem.local_path))
        self.refresh()
        # dialog = UploaderBackgroundWidget(files, max_threads=5)
        # dialog.show()
        # dialog.execute_upload_process()

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

        def createNewAction(actionName, connectTo, menu, *args, **kwargs):
            newAction = QtWidgets.QAction(actionName, menu)
            newAction.triggered.connect(partial(connectTo, *args, **kwargs))
            menu.addAction(newAction)
            return newAction

        menu = QtWidgets.QMenu(self)
        # newFileAction = createNewAction("Create new File", self.showNewFileDialog, menu)
        menu.addSeparator()
        downloadFile = createNewAction("Download", self.downloadFile, menu, FileManager.DOWNLOAD)
        downloadFileOnly = createNewAction("Download File only", self.downloadFile, menu, FileManager.DOWNLOAD_FILE_ONLY)
        downloadDependencies = createNewAction("Download Dependencies only", self.downloadFile, menu, FileManager.DOWNLOAD_DEPENDENCIES_ONLY)
        menu.addSeparator()
        # createNewAction("Open", self.openFile, menu)
        if not isinstance(self.selectedItem, Maya):
            # newFileAction.setDisabled(True)
            downloadFileOnly.setDisabled(True)
            downloadDependencies.setDisabled(True)
        if itemData:
            menu.addAction("Copy path", partial(self.copyPath, itemData))
        return menu

    def copyPath(self, itemData):
        itemData = itemData.data(0, QtCore.Qt.UserRole)
        clipboard = QtGui.QClipboard()
        clipboard.setText(os.path.normpath(itemData.local_path).replace("\\", "/"))

    def showNewFileDialog(self):
        dialog = newfileDialog.NewFileDialog(currentDir=self.selectedItem.local_path.replace("BM2", "bm2"), parent=self)
        dialog.createFile.connect(self.createNewFile)
        dialog.show()

    def createNewFile(self, newFile):
        dpx = DropboxManager()
        if not os.path.isdir(os.path.dirname(newFile)):
            os.makedirs(os.path.dirname(newFile))

        createFile = open(newFile, "w")
        newFileLocation = os.path.normpath(os.path.join(self.selectedItem.remote_path, os.path.basename(newFile))).replace("\\", "/")
        dpx.uploadFile(local_file=os.path.normpath(newFile), target_file=newFileLocation, check_repository=False)
        QtWidgets.QMessageBox.information(self, "Upload Succesfully", "Files uploaded succesfully to {}".format(self.selectedItem.local_path))
        self.refresh()

    def compareFilesPath(self, file):
        currentFolderDir = os.path.normpath(self.currentFolder.local_path).lower()
        fileFolderDir = os.path.normpath(os.path.dirname(file)).lower()
        return True if str(currentFolderDir) == str(fileFolderDir) else False

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

    def downloadFile(self, downloadOption=0):
        if isinstance(self.selectedItem, Folder):
            # print "Downloading Folder"
            files = self.selectedItem.allChildren()
            files = [entry.path_display.replace("/work/", "P:/") for entry in files]
            downloader = DependencyLoaderWidget(parent=self)
            downloader.execute_update_process(extra_files_to_download=files)
        else:
            if downloadOption == FileManager.DOWNLOAD:
                if isinstance(self.selectedItem, Maya):
                    self.selectedItem.downloadAll(parent=self)
                else:
                    self.selectedItem.download()
            elif downloadOption == FileManager.DOWNLOAD_FILE_ONLY:
                self.selectedItem.download()
                QtWidgets.QMessageBox.information(self, "Download successfully", "File downloaded")
            elif downloadOption == FileManager.DOWNLOAD_DEPENDENCIES_ONLY:
                raise NotImplementedError("Download dependencies only is not implemented")
            else:
                raise ValueError("downloadOption must be 0, 1 or 2")
            # self.selectedItem.download()

    def populateMainContainer(self, fileObj, addHistory=True):
        if isinstance(fileObj, Folder):
            self.setUpdatesEnabled(False)
            self.currentFolder = fileObj
            self.mainContainer.clear()
            self.mainContainer.setIconSize(QtCore.QSize(200,200))
            for childDpxMetadata in fileObj.remote_children():
                childFile = childDpxMetadata.path_display
                listItem = QtWidgets.QTreeWidgetItem()
                fileInstance, fileWidget = FileTypeChooser.getClass(childFile, includeWidget=True)
                newFile = fileInstance(childFile)
                newFileWidget = fileWidget(newFile, parent=self.mainContainer)
                self.setItemData(item=listItem,
                                 data=newFile,
                                 parentTree=self.mainContainer,
                                 widget=newFileWidget,
                                 dropboxMetadata=childDpxMetadata)
            self.setUpdatesEnabled(True)
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
        self.pathLE.setText(os.path.normpath(folder.local_path).replace("\\", "/"))

    def setItemData(self, item, data, parentTree, widget=None, dropboxMetadata=None):
        self.setUpdatesEnabled(False)
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
        self.setUpdatesEnabled(True)

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
    obj = gui_loader.get_default_container(widget, "Update All", style=False, simple_bar=False)
    obj.show()
    app.exec_()
