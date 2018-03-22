from genericFile import GenericFile
import os


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