import getpass
import json
import os
from datetime import datetime

import metadata


def generate_metadata_path(scene_path):
    scene_name = os.path.basename(scene_path)
    scene_folder = os.path.dirname(scene_path)
    return os.path.join(scene_folder, "metadata", 
                        "{}.metadata".format(scene_name.split(".")[0])
                        ).replace("\\", "/")


def make_metadata_from_local(metadata_file):
    if not is_metadata_file(metadata_file):
        raise Exception("{} must be a valid Metadata File".format(os.path.basename(metadata_file)))
    with open(metadata_file) as json_data:
        metadata_data = json.load(json_data)
    return metadata.Metadata(metadata_data)


def is_metadata_file(metadata_file):
    return os.path.splitext(metadata_file)[1] == ".metadata"


def generate_metadata_from_scene(save=True):
    pass

def get_metadata_of_scene():
    pass



def open_maya_file(metadata_file):
    pass

def generate_snapshot(image_path):
    pass
