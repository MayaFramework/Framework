from Framework.lib.dropbox_manager.manager import DropboxManager
import os
from Framework.lib.logger import logger


class RemoteObject(object):

    def __init__(self, path):

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

    @property
    def remote_path(self):
        return self._remote_path

    @property
    def extension(self):
        return os.path.splitext(self.local_path)[1]

    @property
    def associatedExtensions(self):
        return self._associatedExtensions

    @associatedExtensions.setter
    def associatedExtensions(self, value):
        self._associatedExtensions = value

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value

    def validate_scene_path(self, path):
        if path.startswith("P:/"):
            local_path = path
            remote_path = path.replace("P:/BM2/", "/work/bm2/")
        elif path.startswith("/work"):
            local_path = path.replace("/work", "P:/")
            remote_path = path
        else:
            raise Exception
        return local_path, remote_path

    def download_file(self):
        # if not os.path.exists(self.local_path):
        #     # This method should work either with local or remote metadata
        if self.dpx.existFile(self.local_path):
            self.dpx.downloadFile(self.local_path)
            logger.info("File: {} downloaded!".format(self.name))

    @staticmethod
    def getExtension(path):
        return os.path.splitext(path)[1]