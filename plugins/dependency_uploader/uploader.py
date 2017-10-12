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
    _work_environ = ""
    def __init__(self):
        self._config = get_environ_config()
        self.dpx = DropboxManager(self._config["dpx_token"])
        self._ma_reader = MaReader()


    @property
    def work_environ(self):
        """
        Work environ works to know which dependencies are the target to be uploaded
        """
        return self._work_environ
    
    @work_environ.setter
    def work_environ(self, value):
        self._work_environ = value if isinstance(value, (str,unicode)) else ""

    def get_dependencies(self, file_path):
        """
        Get dependencies usign Ma reader
        and later organize this result for keys filtered or not filtered
        FILTER_PATH Used to filter the result
        """
        if not file_path.endswith(".ma"):
            return False

        self.work_environ = file_path.rsplit("/",2)[0]
        dependencies = self._ma_reader.get_references(file_path)
        if dependencies and isinstance(dependencies, dict):
            aux_dict = {}
            aux_dict[self.FILTERED_KEY] = []
            aux_dict[self.NOT_FILTERED_KEY] = []
            for dependency in dependencies:
                if self.pass_filter(dependency):
                    aux_dict[self.FILTERED_KEY].append(dependency)
                else:
                    aux_dict[self.NOT_FILTERED_KEY].append(dependency)

            dependencies = aux_dict


        return dependencies

    def pass_filter(self, file_path):
        """
        Args:
            file_path(str/unicode): File Root

        return:
            True: if it pass every check
            False: if it didnt pass any check

        """
        # check Format
        if not isinstance(file_path, (str, unicode)):
            return False

        # Check if the content exists
        if not os.path.exists(file_path):
            return False

        # Check work environ
        if file_path.startswith(self.work_environ):
            return False

        return True

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
        file_path = self.dpx.normpath(file_path)
        if not self.check_file_structure(file_path):
            return False
        # check folder
        parent_folder = self.get_parent_folder(file_path)
        if parent_folder in ["mps","chk","wip"]:
            target = file_path.replace("/"+parent_folder+"/", "/"+os.path.join(parent_folder,"_old")+"/")
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
    a = Uploader()
    path = a.dpx.normpath(r"P:\bm2\seq\tst\sho\440\render\out\bm2_shoscn_seq_tst_sho_440_scncmp_gato_turnArroundNeutralLigh_out.ma")
    print path.split("/")[-3]
    
