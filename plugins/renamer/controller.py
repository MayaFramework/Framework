import os
import re
# path example:
# "P:\bm2\chr\gato\out\rigging\thinHigh\out\bm2_chrout_chr_gato_out_rigging_thinHigh_default_none_out.ma " 
from Framework.lib.config.config import Config
import propierties
class Renamer(object):
    FILE_PATH_FORMAT = "{disk}/{show}/{department}/{asset}/{task}/{details}/{main}/{folder}/{filename}"
    FILE_NAME = "{show}_{department}{task}_{department}_{asset}_{task}_{details}_{main}_{default}_{none}_{folder}.{extension}"
    REG_EXP = '{[a-z]*}'


    ATTR_DISK = "disk"
    ATTR_SHOW = "show"
    ATTR_DEPARTMENT = "department"
    ATTR_ASSET = "asset"
    ATTR_TASK = "task"
    ATTR_DETAILS = "details"
    ATTR_MAIN = "main"
    ATTR_FOLDER = "folder"
    ATTR_FILENAME = "filename"


    
    def __init__(self):
        self._config = Config.instance()


    def check_file_path_format(self, file_path):
        fields_data = self.get_fields_from_file_path
        self.check_fields_value(fields_data)
    
    def check_fields_value(self, fields_data=""):
        '''
        checks field dict matching possible values
        :param fields_data: dict
        :return (bool)
        '''
        for key, value in fields_data:
            if key == self.ATTR_DISK and key not in propierties.ATTR_DISK_AVAILABLE:
                return False
            if key == self.ATTR_SHOW and key not in propierties.ATTR_SHOW_AVAILABLE:
                return False
            if key == self.ATTR_DEPARTMENT and key not in propierties.ATTR_DEPARTMENT_AVAILABLE:
                return False
        return True
    
    def get_fields_from_file_path(self, file_path):
        '''
        file_path to extract fields
        :param file_path: (str)
        '''
        file_path = os.path.normpath(file_path)
        fields = file_path.rsplit("\\")
        fields_data = {
                        self.ATTR_DISK:fields[0],
                        self.ATTR_SHOW: fields[1],
                        self.ATTR_DEPARTMENT: fields[2],
                        self.ATTR_ASSET: fields[3],
                        self.ATTR_TASK: fields[4],
                        self.ATTR_DETAILS: fields[5],
                        self.ATTR_MAIN: fields[6],
                        self.ATTR_FOLDER: fields[7],
                        self.ATTR_FILENAME: fields[8]
                        }
        return fields_data

    
    def generete_complete_file_path(self, fields):
        '''
        format file name matchin fields with the static attr FILE_NAME
        '''
        base_fields = {
            self.ATTR_DISK: self._confing.environ[self.ATTR_DISK],
            self.SHOW: self._config.environ[self.SHOW]}
        base_fields.update(fields)

        file_name = self.generate_file_name(base_fields)

        base_fields.update({self.ATTR_FILENAME: file_name})

        file_path = self.FILE_PATH_FORMAT.format(base_fields)
        result = re.findall(self.REG_EXP, file_path)
        if len(result)>0:
            raise Exception("Need to specify the next values: %s" % (" ".join(result)))
        return file_path

    def generate_file_name(self, fields):
        '''
        format file name matchin fields with the static attr FILE_NAME
        '''
        base_fields = {
            self.SHOW: self._config.environ[self.SHOW]}
        base_fields.update(fields)

        file_name = Renamer.FILE_NAME.format(fields)
        result = re.findall(Renamer.REG_EXP, file_name)
        if len(result)>0:
            raise Exception("Need to specify the next values: %s" % (" ".join(result)))
        return file_name



if __name__ == "__main__":
    file_path = r"P:\bm2\chr\gato\out\rigging\thinHigh\out\bm2_chrout_chr_gato_out_rigging_thinHigh_default_none_out.ma"
    fields = {
        Renamer.ATTR_ASSET: "",
            
        }
    rename = Renamer()
    print rename.generateCompleteFilePath(**fields)
    
