from Framework.lib.dropbox_manager.manager import DropboxManager
from Framework.plugins.dependency_loader.dependency_loader_window import DependencyLoaderWidget
from Framework.plugins.dependency_uploader.uploader_window import UploaderWindow
from Framework.lib.gui_loader import gui_loader


import os


class GenericFile(object):

    def __init__(self, path):

        self._allowSave = False
        self._allowDownload = True
        self._allowOpen = False
        self._openCommand = None
        self._name = None
        self._icon = None
        self._associatedExtensions = list()
        self._local_path, self._remote_path = self.validate_scene_path(path)
        self.dpx = DropboxManager()

    @property
    def name(self):
        return os.path.basename(self._local_path)

    @property
    def local_path(self):
        return self._local_path

    @local_path.setter
    def local_path(self, value):
        self._local_path = value

    @property
    def remote_path(self):
        return self._remote_path

    @property
    def extension(self):
        return os.path.splitext(self.local_path)[1]

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value

    @property
    def couldBeOpened(self):
        return self._allowOpen

    @couldBeOpened.setter
    def couldBeOpened(self, value):
        self._allowOpen = value

    @property
    def couldBeSaved(self):
        return self._allowSave

    @couldBeSaved.setter
    def couldBeSaved(self, value):
        self._allowSave = value

    @property
    def couldBeDownloaded(self):
        return self._allowDownload

    @couldBeDownloaded.setter
    def couldBeDownloaded(self, value):
        self._allowDownload = value

    @property
    def openCommand(self):
        return self._openCommand

    @openCommand.setter
    def openCommand(self, value):
        self._openCommand = value

    def validate_scene_path(self, path):
        if path.startswith("P:/"):
            local_path = path
            remote_path = path.replace("P:/BM2/", "/work/bm2/")
        elif path.startswith("/work"):
            local_path = path.replace("/work", "P:/")
            remote_path = path
        elif path.startswith("bm2"):
            local_path = "bm2"
            remote_path = "bm2"
        else:
            raise Exception
        return local_path, remote_path

    @staticmethod
    def getExtension(path):
        return os.path.splitext(path)[1]

    def open(self):
        self.download()
        if self.couldBeOpened:
            exec(self.openCommand.format(self.local_path.replace("\\", "/")))

    def download(self):
        tool = DependencyLoaderWidget(self.local_path)
        self.obj = gui_loader.get_default_container(tool, "Update All")
        self.obj.show()
        tool.execute_update_process()

    def save(self):
        widget = UploaderWindow(self.local_path)
        self.obj = gui_loader.get_default_container(widget, "UPLOADER")
        self.obj.show()
        widget.execute_analize_process()