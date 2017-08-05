


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


class DropboxManager(object):
    __client = None
    __dpx = None
    _base_path = None
    __subfolder = "WORK"
    _base_path = "P:"
    def __init__(self, token, base_path="", subfolder = ""):
        from Framework.lib.ext_lib import dropbox
        self.DropBox = dropbox
        self.__client = self.DropBox.client.DropboxClient(token)
        self.__dpx = self.DropBox.dropbox.Dropbox(token)
        if base_path:
            self._base_path = base_path
        if subfolder:
            self.__subfolder = subfolder

    def uploadFile(self, local_file, overwrite=True):
        """
        Get the correct file_path from dropbox
        Upload file using overwrite key to be forced on the upload
        """
        if not local_file.startswith(self._base_path):
            raise Exception("Wrong repository")

        dropbox_path = self.getDropboxPath(local_file)
        with open(local_file, 'rb') as my_file:
            response = self.__client.put_file(dropbox_path, my_file, overwrite=overwrite)
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
            self.__dpx.files_download_to_file(target_path,dropbox_path)
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
        base,file_name = file_path.rsplit("/", 1)
        path = os.path.join(base.lower() ,file_name)
        if path.startswith(self._base_path.lower()):
            path = path.split("/", 1)[1]

        if self.__subfolder:
            if path.startswith(self.__subfolder.lower()):
               return self.DropBox.client.format_path(self.normpath(path))
            else:
                return "/" + self.__subfolder.lower() + self.DropBox.client.format_path(self.normpath(path))
        else:
            return self.DropBox.client.format_path(self.normpath(path))

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

    def getTargetPath(self, path):
        if path.startswith("/"):
            base,file_name = path.rsplit("/", 1)
            path = os.path.join(base.lower() ,file_name).split("/",1)[1]

            if path.startswith(self.__subfolder.lower()) :
                return self.normpath(os.path.join(self._base_path, path.split("/",1)[1]))
            else:
                return self.normpath(os.path.join(self._base_path, path))
        else:
            if path.startswith(self.__subfolder.lower()):
                base,file_name = path.rsplit("/", 1)
                return  self.normpath(os.path.join(self._base_path,base.split("/",1)[1].lower(),file_name))
            elif path.startswith(self._base_path):
                base,file_name = path.rsplit("/", 1)
                return self.normpath(os.path.join(base.lower().replace(self._base_path.lower(), self._base_path.upper()),file_name))


    def getChildrenFromFolder(self,folder):
        folder = self.getDropboxPath(folder)
        metadata = self.__client.metadata(folder)
        children_path = []
        for my_data in metadata["contents"]:
            if len(metadata["contents"]) >1:
                children_path.append(my_data["path"])
        return children_path


    def getAllrecursiveChildren(self, folder):
        children = self.__dpx.files_list_folder(folder, recursive=True)
        return children



if __name__ == "__main__":
    dpx = DropboxManager(token="5e9ZZ9cN4roAAAAAAAACWFj1dK-eg6oDDYFu8a9EdloBJFw8SAOVL7KtK2WqDAl4")
    file_path = r"P:\\bm2\\elm\\gafasGato_TEST\\sha\\high\\shading\\chk\\bm2_elmsha_elm_gafasGato_sha_high_shading_default_none_chk_0011.ma"
    print dpx.existFile(file_path)

# dpx.getChildrenFromFolder(r"P:/BM2/seq/tst/sho/300/footage/mps")