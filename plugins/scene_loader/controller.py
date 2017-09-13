import os
import maya.cmds as cmds


TEMPPATH = r"C:\Users\Alberto\Documents\P\bm2"


def generate_paths_info(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    paths_dict = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], paths_dict)
        parent[folders[-1]] = subdir
    return paths_dict

def generate_snapshot(image_path):
    cmds.select(cl=True)
    cmds.playblast( frame=1,
                    format="image",
                    completeFilename="{}".format(image_path),
                    sequenceTime=0,
                    clearCache=1,
                    viewer=0,
                    offScreen=True,
                    fp=0,
                    percent=100,
                    compression="png",
                    quality=100,
                    widthHeight=(120,120),
                    showOrnaments=False )
    return image_path

def generate_paths_info2(path):
    return sorted(os.listdir(path))