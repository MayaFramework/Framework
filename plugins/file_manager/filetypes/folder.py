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

    def remote_children(self):
        # return self.dpx.getChildren(self.local_path, includeMetadata=True)
        return self.dpx.getAllChildren(self.remote_path)
    
    def remote_children_old(self):
        return self._old_dpx.getChildren(self.remote_path, includeMetadata=True)

    def download(self, open=False):
        # dependenciesList = list()
        # recursiveFiles = Folder.getRecursiveFiles(self.local_path, dependenciesList)
        # dialog = DependencyLoaderWidget()
        # dialog.show()
        # dialog.execute_upload_process(recursiveFiles)
        pass

    def allChildren(self):
        return self._old_dpx.getChildren(self.remote_path, recursive=True)
        # PETA CON SUBCARPETAS
#         return self.dpx.getAllChildren(self.remote_path, recursive=True)

# path = "P:/bm2/elm/altavozPie"
# b = list()
# a = Folder.getRecursiveFiles(path, b)
# print a
# path = "/work/bm2/elm"
# f = Folder(path)
# metadata = f.dpx.getFileMetadata(f.remote_path)



# print f.local_path
# print f.remote_children
# # a = dpx.getAllChildren(path)
# # print a
