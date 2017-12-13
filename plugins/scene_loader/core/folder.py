import os
from Framework.lib.dropbox_manager.manager import DropboxManager


class Folder(object):
    def __init__(self, folder_path, dropbox_instance=None):

        self.local_path, self.remote_path = self.validate_folder_path(folder_path)

        if not dropbox_instance:
            dropbox_instance = DropboxManager("MspKxtKRUgAAAAAAAAA1OnMGBw6DOOG2Cz38E83-YJaxw7Jv2ihc2Afd-82vmZkI")

        self.dropbox_instance = dropbox_instance

    def validate_folder_path(self, folder_path):
        if folder_path.startswith("P:/"):
            local_path = folder_path
            remote_path = folder_path.replace("P:/BM2/", "/work/bm2/")
        elif folder_path.startswith("/work"):
            local_path = folder_path.replace("/work", "P:/")
            remote_path = folder_path
        else:
            raise Exception
        return local_path, remote_path

    @property
    def dir_name(self):
        return self.local_path.split("/")[-1]

    @property
    def children(self):
        return os.listdir(self.local_path)

    @property
    def remote_children_folders(self):
        return self.dropbox_instance.getFolderChildrenFromFolder(self.local_path)

    @property
    def remote_children_maya_files(self):
        return self.dropbox_instance.getFilesChildren(self.local_path, ".ma")