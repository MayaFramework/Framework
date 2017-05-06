"""
author = ["miguel.molledo.alvarez@gmail.com"]


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
    __base_path = None
    __subfolder = "WORK"
    __base_path = "P:/"
    def __init__(self, token, base_path="", subfolder = ""):
        from Framework.lib.ext_lib import dropbox
        self.DropBox = dropbox
        self.__client = self.DropBox.client.DropboxClient(token)
        self.__dpx = self.DropBox.dropbox.Dropbox(token)
        if base_path:
            self.__base_path = base_path
        if subfolder:
            self.__subfolder = subfolder
    def uploadFile(self, local_file):
        if not local_file.startswith(self.__base_path):
            raise Exception("Wrong repository")

        dropbox_path = self.getDropboxPath(local_file.split(self.__base_path, 1)[1])
        with open(local_file, 'rb') as my_file:
            self.__client.put_file(dropbox_path, my_file)

    def downloadFile(self, path):
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

    def downloadFiles(self, files):
        for file in files:
            self.getFile(self.normpath(file))

    def normpath(self, path):
        path = os.path.normpath(path).replace("\\", "/")
        return path

    def getDropboxPath(self,path):
        base,file_name = path.rsplit("/", 1)
        path = os.path.join(base.lower() ,file_name)
        if path.startswith(self.__base_path.lower()):
            path = path.split("/", 1)[1]

        if self.__subfolder:
            if path.startswith(self.__subfolder.lower()):
               return self.DropBox.client.format_path(self.normpath(path))
            else:
                return "/" + self.__subfolder.lower() + self.DropBox.client.format_path(self.normpath(path))
        else:
            return self.DropBox.client.format_path(self.normpath(path))


    def getTargetPath(self, path):


        if path.startswith("/"):
            base,file_name = path.rsplit("/", 1)
            path = os.path.join(base.lower() ,file_name).split("/",1)[1]

            if path.startswith(self.__subfolder.lower()) :
                return self.normpath(os.path.join(self.__base_path, path.split("/",1)[1]))
            else:
                return self.normpath(os.path.join(self.__base_path, path))
        else:
            if path.startswith(self.__subfolder.lower()):
                base,file_name = path.rsplit("/", 1)
                return  self.normpath(os.path.join(self.__base_path,base.split("/",1)[1].lower(),file_name))
            elif path.startswith(self.__base_path):
                base,file_name = path.rsplit("/", 1)
                return self.normpath(os.path.join(base.lower().replace(self.__base_path.lower(), self.__base_path.upper()),file_name))


    def getChildrenFromFolder(self,folder):
        folder = self.getDropboxPath(folder)
        metadata = self.__client.metadata(folder)
        children_path = []
        for my_data in metadata["contents"]:
            if len(metadata["contents"]) >1:
                children_path.append(my_data["path"])
        return children_path

#
# dpx = DropboxManager(token="MspKxtKRUgAAAAAAAAAHPJW-Ckdm7XX_jX-sZt7RyGfIC7a7egwG-JqtxVNzOSJZ")
# dpx.getChildrenFromFolder(r"P:/BM2/seq/tst/sho/300/footage/mps")