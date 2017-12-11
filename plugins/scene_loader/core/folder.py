import os

class Folder(object):
    def __init__(self, folder_path, dropbox_instance):
        self.folder_path = folder_path
        self.local_folder_path = folder_path.replace("/work", "P:/")
        self.dropbox_instance = dropbox_instance

    @property
    def dir_name(self):
        return self.folder_path.split("/")[-1]

    @property
    def children(self):
        return os.listdir(self.folder_path)

    @property
    def folders_from_db(self):
        return self.dropbox_instance.getFolderChildrenFromFolder(self.local_folder_path)

    @property
    def maya_files_from_db(self):
        return self.dropbox_instance.getChildrenFromFolder(self.local_folder_path)

    @property
    def children_full_path(self):
        return sorted([os.path.join(self.folder_path, child).replace("\\", "/") for child in os.listdir(self.folder_path) \
                if os.path.isdir(os.path.join(self.folder_path, child).replace("\\", "/")) or child.endswith(".ma")])

    @property
    def children_maya_files(self):
        maya_files = [os.path.join(self.folder_path, child).replace("\\", "/") for child in os.listdir(self.folder_path) \
                        if child.endswith(".ma")]
        maya_files.sort(key=lambda s: os.path.getmtime(s), reverse=True)
        return maya_files