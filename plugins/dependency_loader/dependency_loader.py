
import sys
import os
import pprint
import re
sys.path.append(r"C:\project")
from Framework.lib.dropbox_manager.dropbox_manager import DropboxManager

# Import Widget 
# from Framework.lib.dropbox_manager import dropbox_manager
# from Framework.lib.dropbox_manager import dropbox_manager
# from Framework.lib.maya_scenefile_parser import ascii



class MaParser(object):
	def __init__(self,file):
		self._file = file


	def get_references_nodes_dependencies(self):
		reg_expression = "file\s-r\s(-ns\s\"[a-zA-z]*\")+.*(-rfn\s\"[a-zA-z]*\d*?\")+.*(\"P:/BM2/.*)\;"
		_references = {}
		with open(self._file) as file:
			lines = file.readlines()
			for line in lines:
				match_result = re.findall(reg_expression, line)
				if match_result:
					name_space = match_result[0][0].split("-ns ",1)[1].replace('"',"")
					reference_node = match_result[0][1].split("-rfn ",1)[1].replace('"',"")
					file_dir = match_result[0][2].replace('"', "")
					_references[file_dir] = {}
					_references[file_dir]["NameSpace"] = name_space
					_references[file_dir]["RefNode"] = reference_node
					_references[file_dir]["Type"] = "RefNode"
					_references[file_dir]["Command"] = line
			if _references:
				return _references



	def get_attr_dependencies(self):
		reg_expression = "setAttr.*(\"P:/BM2/.*\")\;"
		_references = {}
		with open(self._file) as file:
			lines = file.readlines()
			for line in lines:
				match_result = re.findall(reg_expression, line)
				if match_result:
					file_dir = match_result[0].replace('"',"")
					_references[file_dir] = {}
					_references[file_dir]["Type"] = "Attr"
					_references[file_dir]["Command"] = line
			if _references:
				return _references


	def get_all_dependencies(self):
		aux_dict = self.get_references_nodes_dependencies()
		aux_dict.update(self.get_attr_dependencies())
		if aux_dict:
			return aux_dict


dbx = DropboxManager(token="MspKxtKRUgAAAAAAAAAEao_1Ahw7pNPi1YzKSkwPzA7kzoQzPfrLwx95gNcxWXPN")
ma_file = r"WORK/BM2/seq/tst/sho/010/camera/wip/bm2_shocam_seq_tst_sot_0010_camera_default_scene_wip001.ma"
local_file = dbx.downloadFile(ma_file)
# local_file = r"P:\WORK\BM2\seq\tst\sho\010\camera\wip\bm2_shocam_seq_tst_sot_0010_camera_default_scene_wip001.ma"
maParser = MaParser(file =local_file)
references = maParser.get_all_dependencies()
import pprint

# pprint.pprint(references)
if references and isinstance(references, dict):
	for key,values in references.iteritems():
		if key:
			try:
				print "DOWNLOADING...."
				print key
				dbx.downloadFile(key)
				print "DOWNLOADED SUCCESS"
			except Exception as e:
				print "Something was wrong downloading the file: %s "%key
				print e
		else:
			print "Wrong Key", key
		

