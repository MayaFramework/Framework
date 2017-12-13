


"""

@author: Miguel Molledo
@Direction: miguel.molledo.alvarez@gmail.com

EXAMPLE:

dpx = DropboxManager(token="Yomp-8XE2CoAAAAAAAAAuQsiUXNm1_Fo4BbispgGAoV8-0NvNw2E3YgwoLH1pZBX")

TO UPLOAD FILES
dpx.uploadFile(r"s:/project/test/audiotest.m4v")
or
dpx.uploadFiles(["s:/project/test/audiotest.m4v", "s:/project/test/fileTest.txt"])


TO DOWNLOAD FILES
dpx.getFile("project/audiotest.m4v") 
or 
dpx.downloadFile("c:/project/audiotest.m4v")

or 
dpx.downloadFiles(["s:/project/test/audiotest.m4v", "s:/project/test/fileTest.txt"])


"""




import os
import re
from Framework.lib.ext_lib import dropbox
from Framework.lib.ext_lib.dropbox import files


class DropboxManager(object):
    __client = None
    __dpx = None
    _base_path = None
    __subfolder = "WORK"
    _base_path = "P:"
    def __init__(self, token, base_path="", subfolder = ""):
#         import dropbox
        self.DropBox = dropbox
#         self.__client = self.DropBox.client.DropboxClient(token)
        self.__dpx = self.DropBox.dropbox.Dropbox(token)
        if base_path:
            self._base_path = base_path
        if subfolder:
            self.__subfolder = subfolder

    def uploadFile(self, local_file, overwrite=True, target_file=None):
        """
        Get the correct file_path from dropbox
        Upload file using overwrite key to be forced on the upload
        """
        if not local_file.startswith(self._base_path):
            raise Exception("Wrong repository")

        if overwrite:
            mode= self.DropBox.dropbox.files.WriteMode.overwrite
        else:
            mode= self.DropBox.dropbox.files.WriteMode.add


        dropbox_path = self.getDropboxPath(local_file)
        with open(local_file, 'rb') as my_file:
            response = self.__dpx.files_upload(my_file.read(), dropbox_path, mode=mode)
            if response:
                msg = "UPLOADED FILE: %s" % local_file
                print msg
                return response

    def downloadFile(self, path):
        """
        Download file using self.__dpx class
        Create dirs folders
        """
        dropbox_path = self.getDropboxPath(path)
        target_path = self.getTargetPath(path)

        folder = target_path.rsplit("/", 1)[0]
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except Exception as e:
                print "Warning: %s" % e

        try:
            print "DOWNLOADING the file: %s" % dropbox_path
            self.__dpx.files_download_to_file(target_path, dropbox_path)
            print "DOWNLOADING FINISHED"
        except Exception as e:
            message = "Something was wrong downloading the file: %s " % dropbox_path
            message = message + "\n With the exception: %s" % e
            print message
            return False

        return True

    def uploadFiles(self, files):
        for file in files:
            self.uploadFile(self.normpath(file))


    def normpath(self, path):
        """
        Function to be sure the working format that this class is following
        """
        path = os.path.normpath(path).replace("\\", "/")
        return path

    def getDropboxPath(self,file_path):
        """
        Execute a few methods to transform the patin into a path supported by dropbox
        Also added base folders at the beginning of the file to fit the studio workflow
        """
        file_path = self.normpath(file_path)
        file_path = self.cleanBasePath(file_path)
        file_path = self.addBaseFolderPaths(file_path)
        return file_path
        

    def cleanBasePath(self, file_path):
        """
        Clean disk local rout from the path, P:/ or whatever defined in the statics
        parameters 
        """
        if file_path.startswith(self._base_path):
            return file_path.split(self._base_path, 1)[1]
        else:
            return file_path

    def addBaseFolderPaths(self,file_path):
        """
        Add base folders path to fit the way of working.
        NOTE: This depends on the studioso in the future change this kind of 
        hard code at the beginning of this class
        for something less ugly 
        """
        if file_path.startswith("/"):
            base,file_name = file_path[1:].split("/", 1)
        else:
            base, file_name = file_path.split("/", 1)
            
        path = os.path.join(base.lower() ,file_name)
        if path.startswith(self._base_path.lower()):
            path = path.split("/", 1)[1]

        if self.__subfolder:
            if path.startswith(self.__subfolder.lower()):
               return os.path.abspath(self.normpath(path))
            else:
                return "/" + self.__subfolder.lower() + self.format_path(self.normpath(path))
        else:
            return self.format_path(self.normpath(path))

    def existFile(self,file_path):
        try:
            dpx_local_path = self.getDropboxPath(file_path)
            self.__dpx.files_get_metadata(dpx_local_path)
            return True
        except Exception as e:
            print e
            return False

    def moveFile(self, resource_file , target_file, autorename=True):
        resource_file = self.getDropboxPath(resource_file)
        target_file = self.getDropboxPath(target_file)
        response = self.__dpx.files_move(resource_file, target_file, autorename=True)
        if response:
            msg = "MOVED File from: %s to %s" % (resource_file, target_file)
            print msg
            return response


    def format_path(self, path):
        """Normalize path for use with the Dropbox API.
    
        This function turns multiple adjacent slashes into single
        slashes, then ensures that there's a leading slash but
        not a trailing slash.
        """
        if not path:
            return path
    
        path = re.sub(r'/+', '/', path)
    
        if path == '/':
            return ''
        else:
            return '/' + path.strip('/')

    def getTargetPath(self, path):
        path = self.normpath(path)
        if path.startswith("/"):
            base,file_name = path[1:].split("/", 1)
#         else:
#             base,file_name = path.split("/", 1)

            path = self.normpath(os.path.join(base.lower() ,file_name))

            if path.startswith(self.__subfolder.lower()) :
                return self.normpath(os.path.join(self._base_path + "/", path.split("/",1)[1]))
            else:
                return self.normpath(os.path.join(self._base_path + "/", path))
        else:
            if path.startswith(self.__subfolder.lower()):
                base,file_name = path.split("/", 1)
                return  self.normpath(os.path.join(self._base_path + "/",file_name))
            elif path.startswith(self._base_path):
                disk,base,file_name = path.split("/", 2)
                return self.normpath(os.path.join(disk.upper()+"/",base.lower(), file_name))

    def getChildrenFromFolder(self,folder):
        folder = self.getDropboxPath(folder)
#         metadata = self.__client.metadata(folder)
        try:
            metadata = self.__dpx.files_list_folder(folder)
        except Exception as e:
            print e
            return []
        children_path = []
        for file_metadata in metadata.entries:
            # Try to find a method defin within metadata but it looks bad
            if len(file_metadata.path_display.split(".")) == 2:
                children_path.append(file_metadata.path_display)
        return children_path

    def getFolderChildrenFromFolder(self, folder):
        # TODO Change this shitty method
        if folder == "bm2":
            folder = "/work/bm2/"
        else:
            folder = self.getDropboxPath(folder)
        #         metadata = self.__client.metadata(folder)
        try:
            metadata = self.__dpx.files_list_folder(folder)
        except Exception as e:
            print e
            return []
        children_path = []
        for file_metadata in metadata.entries:
            if isinstance(file_metadata, files.FolderMetadata):
                children_path.append(file_metadata.path_display)
        return sorted(children_path)

    def getFilesChildren(self, folder, extension=None):
        folder = self.getDropboxPath(folder)
        try:
            metadata = self.__dpx.files_list_folder(folder)
        except Exception as e:
            print e
            return []
        children_path = []
        for file_metadata in metadata.entries:
            # Try to find a method defin within metadata but it looks bad
            if isinstance(file_metadata, files.FileMetadata):
                if extension:
                    if os.path.splitext(file_metadata.path_display)[-1] == extension:
                        children_path.append(file_metadata.path_display)
                else:
                    children_path.append(file_metadata.path_display)
        return children_path

    def getAllrecursiveChildren(self, folder):
        children = self.__dpx.files_list_folder(folder, recursive=True)
        return children



if __name__ == "__main__":
    file_path = r"P:/bm2/lib/LIG/preLightingSet/neutralLig/main/mps"
    dpx = DropboxManager()
#     file_path  = r"P:/bm2/seq/tst/sho/1000/hair/mps/v02"
#     print dpx.getDropboxPath(file_path)
#     dpx.downloadFile(file_path)
#     dpx.cleanBasePath(file_path)
#     dpx.uploadFile(file_path, overwrite=True)
    print dpx.getChildrenFromFolder(file_path)
# #     print dpx.getTargetPath(file_path)
# #     file_path = r"\\bm2\\elm\\gafasGato_TEST\\sha\\high\\shading\\chk\\bm2_elmsha_elm_gafasGato_sha_high_shading_default_none_chk_0011.ma"
# #     print dpx.getTargetPath(file_path)
# #     file_path = r"work\\bm2\\elm\\gafasGato_TEST\\sha\\high\\shading\\chk\\bm2_elmsha_elm_gafasGato_sha_high_shading_default_none_chk_0011.ma"
# #     print dpx.getTargetPath(file_path)
# #     file_path = r"\\work\\bm2\\elm\\gafasGato_TEST\\sha\\high\\shading\\chk\\bm2_elmsha_elm_gafasGato_sha_high_shading_default_none_chk_0011.ma"
# #     print dpx.getTargetPath(file_path)
#     path = "/work/BM2/elm"
#     print dpx.getAllrecursiveChildren(dpx.normpath(path))
#     "work/bm2/elm/gafasGato_TEST/sha/high/shading/wip/bm2_elmsha_elm_gafasGato_sha_high_shading_default_none_wip_0011.ma"

# dpx.getChildrenFromFolder(r"P:/BM2/seq/tst/sho/300/footage/mps")