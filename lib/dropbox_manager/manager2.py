import os
import re
from Framework.lib.ext_lib import dropbox
from Framework.lib.ext_lib.dropbox import files
from Framework.lib.ext_lib.dropbox import file_properties
from Framework.lib.singleton import Singleton
from Framework.lib.config.config import Config
from dropboxMetadata import DropboxMetadata


class DropboxManager2(Singleton):

    # FILENAME = "/WORK/BM2/elm/gafasGato_TEST/mod/high/main/wip/bm2_elmmod_elm_gafasGato_mod_high_main_default_none_wip.0001.ma"
    TOKENID = "JRK_a6mrxaAAAAAAAAAFAVrk1F0DewHl7V_eQrtBo7d6671VCUMaA3ylJ915VkTv"
    TEMPLATEID = "ptid:JRK_a6mrxaAAAAAAAAAFAw"
    USERID = "dbmid:AAB3VU3cmHRAMVZZwYwvzzKnR_NQKEYTHN8"
    __subfolder = "WORK"
    _base_path = "P:"

    def __init__(self):
        self._apiObj = dropbox.Dropbox(DropboxManager2.TOKENID,
                                       headers={"Dropbox-Api-Select-User":DropboxManager2.USERID})

    def normpath(self, path):
        """
        Function to be sure the working format that this class is following
        """
        path = os.path.normpath(path).replace("\\", "/")
        return path

    def getDropboxPath(self, file_path):
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

    def addBaseFolderPaths(self, file_path):
        """
        Add base folders path to fit the way of working.
        NOTE: This depends on the studioso in the future change this kind of
        hard code at the beginning of this class
        for something less ugly
        """
        if file_path.startswith("/"):
            base, file_name = file_path[1:].split("/", 1)
        else:
            base, file_name = file_path.split("/", 1)

        path = os.path.join(base.lower(), file_name)
        if path.startswith(self._base_path.lower()):
            path = path.split("/", 1)[1]

        if self.__subfolder:
            if path.startswith(self.__subfolder.lower()):
                return "/" + self.normpath(path)
            else:
                return "/" + self.__subfolder.lower() + self.format_path(self.normpath(path))
        else:
            return self.format_path(self.normpath(path))

    def getTargetPath(self, path):
        path = self.normpath(path)
        if path.startswith("/"):
            base, file_name = path[1:].split("/", 1)
            #         else:
            #             base,file_name = path.split("/", 1)

            path = self.normpath(os.path.join(base.lower(), file_name))

            if path.startswith(self.__subfolder.lower()):
                return self.normpath(os.path.join(self._base_path + "/", path.split("/", 1)[1]))
            else:
                return self.normpath(os.path.join(self._base_path + "/", path))
        else:
            if path.startswith(self.__subfolder.lower()):
                base, file_name = path.split("/", 1)
                return self.normpath(os.path.join(self._base_path + "/", file_name))
            elif path.startswith(self._base_path):
                disk, base, file_name = path.split("/", 2)
                return self.normpath(os.path.join(disk.upper() + "/", base.lower(), file_name))

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

    def fileExists(self, path):
        try:
            self.getMetadata(path)
            return True
        except Exception as e:
            return False

    def getAllChildren(self, folder, recursive=False):
        print folder
        childList = list()
        child = self._apiObj.files_list_folder(folder, recursive=recursive)
        childList.append(child)
        if recursive:
            while child.has_more:
                child = self._apiObj.files_list_folder_continue(child.cursor)
                childList.append(child)
        result = []
        for child_ in childList:
            for entry in child_.entries:
                result.append(entry)
        return sorted(result, key=lambda x: x.name)

    def downloadFile(self, filePath):

        """
        Download file using self.__dpx class
        Create dirs folders
        """
        dropbox_path = self.getDropboxPath(filePath)
        target_path = self.getTargetPath(filePath)

        folder = target_path.rsplit("/", 1)[0]
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except Exception as e:
                print "Warning: %s" % e

        try:
            print "DOWNLOADING the file: %s" % dropbox_path
            self._apiObj.files_download_to_file(target_path, dropbox_path)
            print "DOWNLOADING FINISHED"
        except Exception as e:
            message = "Something was wrong downloading the file: %s " % dropbox_path
            message = message + "\n With the exception: %s" % e
            print message
            raise(e)

        return True

    def getMetadata(self, path, customProperties=False):
        if customProperties:
            return DropboxMetadata(self._apiObj.files_alpha_get_metadata(path, include_property_templates=[DropboxManager2.TEMPLATEID]))
        return DropboxMetadata(self._apiObj.files_alpha_get_metadata(path))

    def updateMetadata(self, path, **properties):
        metadata = self.getMetadata(path, customProperties=True)
        if not metadata.customProperties:
            propertyGroup = metadata.addCustomProperties()
            self._apiObj.file_properties_properties_add(path, propertyGroup)
            metadata = self.getMetadata(path, customProperties=True)
        propertyGroupUpdate = metadata.updateCustomProperties(**properties)
        self._apiObj.file_properties_properties_update(path, propertyGroupUpdate)

if __name__ == "__main__":

    FILENAME = "/WORK/BM2/elm/gafasGato_TEST/mod/high/main/wip/bm2_elmmod_elm_gafasGato_mod_high_main_default_none_wip003.ma"
    dpx = DropboxManager2()
    print dpx.getMetadata(FILENAME, customProperties=True)
    properties = {
        "cAuthor":"TEST",
        "cVersion":"2",
        "cThumbnail": "AAA"
    }
    dpx.updateMetadata(FILENAME, **properties)
    print dpx.getMetadata(FILENAME, customProperties=True)
