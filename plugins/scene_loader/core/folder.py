import os

class Folder(object):
    def __init__(self, folder_path):
        self.folder_path = folder_path

    @property
    def dir_name(self):
        return self.folder_path.split("/")[-1]

    @property
    def children(self):
        return os.listdir(self.folder_path)

    @property
    def children_full_path(self):
        return sorted([os.path.join(self.folder_path, child).replace("\\", "/") for child in os.listdir(self.folder_path) \
                if os.path.isdir(os.path.join(self.folder_path, child).replace("\\", "/")) or child.endswith(".ma")])