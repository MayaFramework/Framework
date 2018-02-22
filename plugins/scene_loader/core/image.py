from remoteObject import RemoteObject
import os
from Framework import get_icon_path

ICON_PATH = get_icon_path()

class ImageFile(RemoteObject):

    def __init__(self, imagePath):
        super(ImageFile, self).__init__(path=imagePath)

        self.icon = os.path.join(ICON_PATH, "extension_images.png")
        self.associatedExtensions = [".jpg", ".png", ".exr", ".tiff", ".tx"]
