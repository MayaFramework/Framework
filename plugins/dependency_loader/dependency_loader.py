
import sys
sys.path.append(r"D:\Miguel\Programming\project\bm2")
import os
import pprint
import re
from Framework.lib.dropbox_manager.dropbox_manager import DropboxManager
reg_expression = "file\s-r\s(-ns\s\"[a-zA-z]*\")+.*(-rfn\s\"[a-zA-z]*\d*?\")+.*(\"P:/BM2/.*)\;"
# Import Widget 
# from Framework.lib.dropbox_manager import dropbox_manager
# from Framework.lib.dropbox_manager import dropbox_manager
# from Framework.lib.maya_scenefile_parser import ascii



class MaParser(object):
	def __init__(self,file):
		self._file = file


	def get_references(self):
		_references = {}
		with open(self._file) as file:
			lines = file.readlines()
			for line in lines:
				match_result = re.findall(reg_expression, line)
				if match_result:
					name_space = match_result[0][0].split("-ns ",1)[1].replace('"',"")
					reference_node = match_result[0][1].split("-rfn ",1)[1].replace('"',"")
					file_dir = match_result[0][2].replace('"', "")
					_references[reference_node] = {}
					_references[reference_node]["NameSpace"] = name_space
					_references[reference_node]["File"] = file_dir
			if _references:
				return _references


dbx = DropboxManager(token="MspKxtKRUgAAAAAAAAAC5dSK9dEi5LdS5Z0UlDrrXjny7U3LDMgQr6jupy9DK7iz")
ma_file =r"D:\Miguel\Programming\project\bm2\tests\bm2_shocam_seq_tst_sot_0010_camera_default_scene_wip001.ma"
test = MaParser(file =ma_file)

myReferences = test.get_references()
if myReferences:
	for key,values in myReferences.iteritems():
		path_dir = values["File"].replace("P:","WORK")
		try:
			dbx.downloadFile(path_dir)
		except Exception as e:
			print "Something was wrong downloading the file: %s "%path_dir
			print e

	


# dbx.downloadFile
class DependecyLoader(object):
	def __init__(self):
		pass

	def update_dependecies_file(self, ma_file):
		if not ma_file:
			raise Exception("Not Ma defined")

