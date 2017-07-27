'''
Created on Jul 2, 2017

@author: Miguel Molledo
@Direction: miguel.molledo.alvarez@gmail.com
'''
from pprint import pprint
from Framework.lib.dropbox_manager.manager import DropboxManager
from Framework.lib.ma_utils.reader import MaReader
import os
from Framework import get_environ_config
class Uploader(object):
    '''
    This class handles the way of uploading the current maya work and their dependencies
    '''
    FILTER_PATH = "/mps/"
    FILTERED_KEY = "filtered"
    NOT_FILTERED_KEY = "not_filtered"
    def __init__(self):
        self._config = get_environ_config()
        self.dpx = DropboxManager(self._config["dpx_token"])
        self._ma_reader = MaReader()

    def get_dependencies(self, file_path):
        """
        Get dependencies usign Ma reader
        and later organize this result for keys filtered or not filtered
        FILTER_PATH Used to filter the result
        """
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
        """
        NOT USING.
        Pending to check
        """

        for file in files:
            file = self.dpx.getDropboxPath(self.dpx.normpath(file))
            result = self.dpx.uploadFile(file)
            if result and call_back_func:
                call_back_func(**callback_args)

    def upload_file(self, file_path):
        """
        Upload the file and move the existing file to an old folder at the same level
        check the file structure
        Extract parent folder
        try to move the file from the source to the target
        upload the new file ino the source path
        """
        if not self.check_file_structure(file_path):
            return False
        # check folder
        parent_folder = self.get_parent_folder(file_path)
        if parent_folder in ["mps","chk","wip"]:
            target = file_path.replace("/"+parent_folder+"/", "/"+os.path.join(parent_folder,"old")+"/")
#             if self.dpx.existFile(file_path):
            try:
                """
                First Im trying to move the file from the source to the target.
                The thing here is that DROPBOX doesn't have any fileexists.
                So the fastest way to check it its trying and if it fails i dont care.
                """
                self.dpx.moveFile(resource_file=file_path,target_file=target, autorename=True)
            except Exception as e:
                msg = "Trying to move a file that could be no exists [THX DROPBOX]"
                print msg
                print e
        result = self.dpx.uploadFile(file_path, overwrite=True)
        if result:
            return True

    def get_parent_folder(self,path):
        """
        Return the parent folder, means split one level back
        """
        path = self.dpx.normpath(path)
        base_path, parent_folder, file_name = path.rsplit("/",2)
        return parent_folder


    def check_file_structure(self, file):
        """
        Check file structure by checking if the file exists and base path
        Its possible to just call a function from within dpx
        """
        if not os.path.exists(file):
            return False
        if not file.startswith(self.dpx._base_path):
            return False
        return True

if __name__ == "__main__":
    Uploader()