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

    @staticmethod
    def has_dependencies(ma_file):
        with open(ma_file) as file:
            lines = file.readlines()
            for line in lines:
                match_result = re.findall(REG_EXPRESSION, line)
                if match_result:
                    return True
        return False

    @staticmethod
    def get_references(ma_file):
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
            return None

    @staticmethod
    def get_all_references(dependencies_list, db_instance, path):
        dependencies = MaReader.get_references(path)
        if dependencies:
            for dp in dependencies.keys():
                if not dp in dependencies_list:
                    dependencies_list.append(dp)
                if dp.endswith(".ma"):
                    if not os.path.exists(dp):
                        db_instance.downloadFile(dp)
                        MaReader.get_all_references(dependencies_list, db_instance, dp)
        return dependencies_list

        