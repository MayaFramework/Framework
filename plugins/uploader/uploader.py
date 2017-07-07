'''
Created on Jul 2, 2017

@author: Miguel
'''
from pprint import pprint
from Framework.lib.dropbox_manager.manager import DropboxManager
from Framework.lib.ma_utils.reader import MaReader

class Uploader(object):
    '''
    This class handles the way of uploading the current maya work and their dependencies
    '''
    def __init__(self):
        self.dpx = DropboxManager(token="MspKxtKRUgAAAAAAAAAHPJW-Ckdm7XX_jX-sZt7RyGfIC7a7egwG-JqtxVNzOSJZ")
        self._ma_reader = MaReader()
        self.get_dependencies(file)

    def get_dependencies(self, file):
        file = r"P:\bm2\elm\gafasGato_TEST\sha\high\shading\chk\bm2_elmsha_elm_gafasGato_sha_high_shading_default_none_chk_0011.ma"
        if not file.endswith(".ma"):
            return False

        dependencies = self._ma_reader.get_references(file)
        return dependencies

    def upload_files(self, files, call_back_func=None, **callback_args):
        for file in files:
            result = self.dpx.uploadFile(file)
            if result and call_back_func:
                call_back_func(**callback_args)

    def upload_file(self, file):
        result = self.dpx.uploadFile(file)
        return result
        

if __name__ == "__main__":
    Uploader()