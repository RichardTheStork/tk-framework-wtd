import sys
sys.path.append (r'Z:\Shotgun_Studio\install\core\python')

import sgtk


# class asset():
	# name = ""
	# id = None
	# entity = None
	# context = None

# class prop(asset):


class assetManager():
	projectPath = r"W:\RTS"
	tk = None
	
	def __init__(self, projectPath = None):
		if projectPath != None:
			self.projectPath = projectPath
		self.tk = sgtk.sgtk_from_path(self.projectPath)
		print 'Initialize Done.'
		
	def __str__(self):
		try:
			return "<assetManager path = %s>" %(self.tk.roots)
		except:
			return "<assetManager projectpath = %s>" %(self.projectPath)
			
	def findAssets(self, assetName = None, assetType = None):
		hier = self.tk.templates["asset_root"]
		fields = {}
		if assetName != None:
			fields["Asset"] = assetName
			print 'has name!'
		if assetType != None:
			fields["sg_asset_type"] = assetType
			print 'has type!'
			
		print 'testing fields : %s' %( fields )
		result = self.tk.abstract_paths_from_template(hier, fields)
		# result = self.tk.entity_from_path()
		return result
		
	def findAsset(self, assetName, assetType = None):
		assetList = self.findAssets(assetName = assetName, assetType = assetType)
		if len(assetList) >= 1:
			print assetList
			return assetList[0]
		else:
			return None
	
	def	getEntities(self, input):
		if type(input) == list:
			print 'is list'
			tempList = []
			for i in input:
				tempList.append(self.getEntity(i))
			return tempList
		else:
			return self.getEntity(input)
		
	def getEntity(self, input):
		return self.tk.context_from_path(input)
		
	def getPositionlistFolder(self, assetName, assetType = None):
		fields = {"Asset":assetName, "sg_asset_type":assetType}
		asset_positionlist_area = self.tk.templates["asset_positionlist"]
		result = self.tk.abstract_paths_from_template(asset_positionlist_area, fields)
		if len(result) > 0:
			return result[0]
		return result

	def getPositionlist(self, assetName, assetType = None, lastOnly = True):
		fields = {"Asset":assetName, "sg_asset_type":assetType}
		asset_positionlist_area = self.tk.templates["asset_positionlist"]
		result = self.tk.abstract_paths_from_template(asset_positionlist_area, fields)
		if len(result) > 0 and lastOnly == True:
			return result[0]
		return result

		
def main():
	Manager = assetManager()
	print Manager
	print "###############"
	tempVar1 = Manager.findAsset("banc", 'Prop')
	print 'found : '
	print tempVar1
	print "_________________"
	tempCtx = Manager.getEntities(tempVar1)
	print Manager.getPositionlist("villageTest" ,lastOnly = False)
	print Manager.getPositionlist("villageTest")
	print Manager.getPositionlistFolder("banc")
			
	# print "######################"
	# print "######################"
	
	# asset_data_root = Manager.tk.templates["asset_data_root"]
	# asset_positionlist = Manager.tk.templates["asset_positionlist_area"]
	# asset_positionlist2 = Manager.tk.templates["asset_positionlist"]
	# print asset_data_root
	# tk = Manager.tk
	# print tempCtx.as_template_fields(asset_data_root)
	
	# print "######################"
	# print Manager.tk.abstract_paths_from_template(asset_data_root, {"Asset": "banc" ,"sg_asset_type": "Prop"})
	# tempPath = Manager.tk.abstract_paths_from_template(asset_positionlist, {"Asset": "villageTest"})
	# print Manager.tk.abstract_paths_from_template(asset_positionlist, {"Asset": "villageTest"})
	# print Manager.tk.abstract_paths_from_template(asset_positionlist2, {"Asset": "villageTest"})
	# print Manager.tk.paths_from_template(asset_positionlist, {"Asset": "villageTest", "sg_asset_type": "Set"})
	# print tk.template_from_path(tempPath[0] + "\\poslist_villageTest_v001.txt")
	# fields = asset_positionlist2.get_fields(tempPath[0])
	# print fields
	# print tk.paths_from_template(asset_positionlist2, fields)
	print "#" * 20
	print "#" * 20
	
	
	
if __name__ == "__main__":
	main()
