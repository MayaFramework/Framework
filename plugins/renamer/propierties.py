'''
Created on Apr 14, 2018

@author: Miguel
'''

ATTR_DISK_AVAILABLE = ["P:"]
ATTR_SHOW_AVAILABLE = ["bm2"]

ATTR_GROUP_AVAILABLE = ["aud","chr","edi","elm","foo","lib","loc", "aud"]
ATTR_AREA_AVAILABLE = ["art","cfx","fxx","lib","mod","out","rdx","rig","sha",
                       "lay","pos","pre","ppr","fed","ant","sho","hdr","fot",
                       "lig","scn","aud","cmp","mat","shot"]
ATTR_PIPE_AVAILABEL= ["out", "wip", "chk", "mps", "ref"]


'P://bm2/elm/ositoPeluche/sha/high/shading/chk/bm2_elmsha_elm_ositopeluche_sha_high_shading_default_scene_chk.ma'
FILE_PATH_FORMAT = "{disk}/{show}/{group}/{name}/{area}/{step}/{layer}/{pipe}/{filename}"
FILE_NAME = "{show}_{worktype}_{group}_{name}_{area}_{step}_{layer}_{partition}_{description}_{pipe}.{extension}"