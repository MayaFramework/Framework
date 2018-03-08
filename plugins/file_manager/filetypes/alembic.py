from genericFile import GenericFile
from Framework.lib.dropbox_manager.manager import DropboxManager


class Alembic(GenericFile):

    def __init__(self, path):
        super(Alembic, self).__init__(path)

        self.couldBeOpened = True
        self.couldBeSaved = False # TODO Except of a normal save, publish
        self.couldBeDownloaded = True

        self.dpx = DropboxManager()


    def download(self):
        """
        Overriding download from GenericFile
        :return:
        """

        self.dpx.downloadFile(self.local_path)