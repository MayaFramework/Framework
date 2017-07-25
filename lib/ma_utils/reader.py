"""
@author: Miguel Molledo
@Direction: miguel.molledo.alvarez@gmail.com
"""

import sys

import os
import pprint
import re
from Framework.lib.dropbox_manager.manager import DropboxManager
# reg_expression = "file\s-r\s(-ns\s\"[a-zA-z]*\")+.*(-rfn\s\"[a-zA-z]*\d*?\")+.*(\"P:/BM2/.*)\;"
REG_EXPRESSION = "(\"P:/.*);"
# P:/BM2/
# Import Widget
# from Framework.lib.dropbox_manager import dropbox_manager
# from Framework.lib.dropbox_manager import dropbox_manager
# from Framework.lib.maya_scenefile_parser import ascii


class MaReader(object):

    def __init__(self):
        pass

    def get_references(self, ma_file):
        _references = {}
        with open(ma_file) as file:
            lines = file.readlines()
            for line in lines:
                match_result = re.findall(REG_EXPRESSION, line)
                if match_result:
                    path = match_result[0].replace("\"", "")
                    _references[path] = {}

            if _references:
                return _references

        