'''
Created on Jul 2, 2017

@author: Miguel
'''
from pprint import pprint
from Framework.lib.dropbox_manager.manager import DropboxManager
from Framework.lib.ma_utils.reader import MaReader
import os
class Uploader(object):
    '''
    This class handles the way of uploading the current maya work and their dependencies
    '''
    FILTER_PATH = "/mps/"
    FILTERED_KEY = "filtered"
    NOT_FILTERED_KEY = "not_filtered"
    def __init__(self):
        self.dpx = DropboxManager(token="5e9ZZ9cN4roAAAAAAAACWFj1dK-eg6oDDYFu8a9EdloBJFw8SAOVL7KtK2WqDAl4")
        self._ma_reader = MaReader()

    def get_dependencies(self, file_path):
        if not file_path.endswith(".ma"):
            return False

        dependencies = self._ma_reader.get_references(file_path)
        if dependencies and isinstance(dependencies, dict):
            aux_dict = {}
            aux_dict[self.FILTERED_KEY] = []
            aux_dict[self.NOT_FILTERED_KEY] = []
            for dependency in dependencies:
                if self.FILTER_PATH in dependency:
                    aux_dict[self.FILTERED_KEY].append(dependency)
                else:
                    aux_dict[self.NOT_FILTERED_KEY].append(dependency)

            dependencies = aux_dict


        return dependencies

    def upload_files(self, files, call_back_func=None, **callback_args):
        for file in files:
            file = self.dpx.getDropboxPath(self.dpx.normpath(file))
            result = self.dpx.uploadFile(file)
            if result and call_back_func:
                call_back_func(**callback_args)

    def upload_file(self, file):
        if not self.check_file_structure(file):
            return False
        result = self.dpx.uploadFile(file)
        if result:
            return True

    def check_file_structure(self, file):
        if not os.path.exists(file):
            return False
        if not file.startswith(self.dpx._base_path):
            return False
        return True

if __name__ == "__main__":
    Uploader()