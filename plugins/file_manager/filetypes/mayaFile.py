from genericFile import GenericFile
import os
from Framework.plugins.dependency_loader.dependency_loader_window import DependencyLoaderWidget
import threading



class Maya(GenericFile):

    def __init__(self, path):
        super(Maya, self).__init__(path)

    # def download(self, open=False):
    #     downloader = DependencyLoaderWidget(file_path=self.local_path)
    #     downloader.show()

    def downloadAll(self):
        downloader = DependencyLoaderWidget(file_path=self.local_path)
        downloader.external_open_file = False
        downloader.show()
