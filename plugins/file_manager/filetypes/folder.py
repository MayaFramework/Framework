from genericFile import GenericFile
import os
from Framework.lib.ext_lib.dropbox.files import FolderMetadata
# from Framework.plugins.dependency_loader.dependency_loader_window import DependencyLoaderWidget
from threading import Thread


class Folder(GenericFile):

    def __init__(self, path):
        super(Folder, self).__init__(path)

    @property
    def dir_name(self):
        return self.local_path.split("/")[-1]

    @property
    def children(self):
        return os.listdir(self.local_path)

    @property
    def remote_children_folders(self):
        return self.dpx.getAllChildren(self.local_path)

    @property
    def remote_children_maya_files(self):
        return self.dpx.getFilesChildren(self.local_path, ".ma")

    @property
    def remote_children_files(self):
        return self.dpx.getFilesChildren(self.local_path)

    @property
    def remote_children(self):
        # return self.dpx.getChildren(self.local_path, includeMetadata=True)
        return self.dpx.getAllChildren(self.remote_path)

    def download(self, open=False):
        # dependenciesList = list()
        # recursiveFiles = Folder.getRecursiveFiles(self.local_path, dependenciesList)
        # dialog = DependencyLoaderWidget()
        # dialog.show()
        # dialog.execute_upload_process(recursiveFiles)
        pass

    def allChildren(self):
        return self.dpx.getAllChildren(self.remote_path, recursive=True)

# path = "P:/bm2/elm/altavozPie"
# b = list()
# a = Folder.getRecursiveFiles(path, b)
# print a
path = "/work/bm2/elm"
f = Folder(path)
metadata = f.dpx.getFileMetadata(f.remote_path)



# print f.local_path
# print f.remote_children
# # a = dpx.getAllChildren(path)
# # print a
