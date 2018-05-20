from genericFile import GenericFile
import os
from Framework.lib.ext_lib.dropbox.files import FolderMetadata
from Framework.plugins.dependency_loader.dependency_loader_window import DependencyLoaderWidget


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
        return self.dpx.getFolderChildrenFromFolder(self.local_path)

    @property
    def remote_children_maya_files(self):
        return self.dpx.getFilesChildren(self.local_path, ".ma")

    @property
    def remote_children_files(self):
        return self.dpx.getFilesChildren(self.local_path)

    @property
    def remote_children(self):
        return self.dpx.getChildren(self.local_path, includeMetadata=True)

    def download(self, open=False):
        dependenciesList = list()
        recursiveFiles = Folder.getRecursiveFiles(self.local_path, dependenciesList)
        dialog = DependencyLoaderWidget()
        dialog.show()
        dialog.execute_upload_process(recursiveFiles)

    @staticmethod
    def getRecursiveFiles(path, lista):
        f = Folder(path)
        for dependency in f.remote_children:
            if isinstance(dependency[1], FolderMetadata):
                Folder.getRecursiveFiles(dependency[0], lista)
            else:
                lista.append(os.path.normpath(dependency[0]))
        return lista