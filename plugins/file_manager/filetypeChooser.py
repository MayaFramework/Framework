import os

from Framework.lib.ext_lib.dropbox import files
from Framework.lib.dropbox_manager.manager import DropboxManager

from filetypes.folder import Folder
from gui.filetypes.folder import FolderWidget
from filetypes.unknown import Unknown
from gui.filetypes.unknown import UnknownWidget
from filetypes.mayaFile import Maya
from gui.filetypes.maya import MayaWidget
from filetypes.images import Images
from gui.filetypes.images import ImagesWidget

class FileTypeChooser(object):

    FILETYPECLASSES = {
        "folder":{
            "extensions":[],
            "object":Folder,
            "widget":FolderWidget
        },
        "maya": {
            "extensions": [".ma", ".mb"],
            "object": Maya,
            "widget": MayaWidget
        },
        "images": {
            "extensions": [".png", ".jpg", ".jpeg", ".tx", ".tiff"],
            "object": Images,
            "widget": ImagesWidget
        },
        "unknown": {
            "extensions": [],
            "object": Unknown,
            "widget": UnknownWidget
        }
    }

    @staticmethod
    def validate_scene_path(path):
        if path.startswith("P:/"):
            remote_path = path.replace("P:/BM2/", "/work/bm2/")
        elif path.startswith("/work"):
            remote_path = path
        elif path.startswith("bm2"):
            remote_path = "bm2"
        else:
            raise Exception
        return remote_path

    @staticmethod
    def isFolder(path):
        # print path
        # dpx = DropboxManager()
        # metadata = dpx.getFileMetadata(path.replace("\\", "/"))
        # return isinstance(metadata, files.FolderMetadata)
        extension = os.path.splitext(path)[-1]
        return True if extension == "" else False

    @staticmethod
    def getClass(objectPath, includeWidget=False):
        if FileTypeChooser.isFolder(objectPath):
        # if objectPath == "a":
            folderObject = FileTypeChooser.FILETYPECLASSES["folder"].get("object")
            if includeWidget:
                folderWidget = FileTypeChooser.FILETYPECLASSES["folder"].get("widget")
                return folderObject, folderWidget
            return folderObject
        else:
            extension = os.path.splitext(objectPath)[-1]
            for k,v in FileTypeChooser.FILETYPECLASSES.iteritems():
                if extension not in v.get("extensions"):
                    continue
                fileObject = FileTypeChooser.FILETYPECLASSES[k].get("object")
                if includeWidget:
                    fileWidget = FileTypeChooser.FILETYPECLASSES[k].get("widget")
                    return fileObject, fileWidget
                return fileObject
            else:
                fileObject = FileTypeChooser.FILETYPECLASSES["unknown"].get("object")
                if includeWidget:
                    fileWidget = FileTypeChooser.FILETYPECLASSES["unknown"].get("widget")
                    return fileObject, fileWidget
                return fileObject


