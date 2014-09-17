import os, json


class Positionlist:
	path = ""
	content = None
	
	def __init__(self, path = None):
		if path != None:
			self.setPath(path)
			self.load()
			
	def setPath(self, path):
		self.path = path
		return self.path
		
	def saveAs(self, path = None):
		if path != None:
			self.path = path
		createJsonPositionList(self.content, self.path)			
			
	def load(self, path = None):
		if path != None:
			self.path = path
		self.content = loadJsonPositionList(self.path)
		if self.content != None:
			self.analyseContent()
		
	def loadAssetTypes(self, assetType = None):
		self.analyseContent()
	
		if assetType == 'Prop':
			return self.props
		elif assetType == 'Character':
			return self.characters
		elif assetType == 'Set':
			return self.sets
		elif assetType == 'Vehicle':
			return self.vehicles
		elif assetType == 'Camera':
			return self.cameras
		elif assetType == 'Light':
			return self.lights
		else:
			return self.others
	
	def addAsset(self, assetDict):
		self.content[assetDict["name"]] = assetDict
		
	def analyseContent(self):
		self.props = []
		self.characters = []
		self.sets = []
		self.vehicles = []
		self.cameras = []
		self.lights = []
		self.others = []
		
		for c in self.content:
			if self.content[c]["assetType"] == 'Prop':
				self.props.append(c)
			elif self.content[c]["assetType"] == 'Character':
				self.characters.append(c)
			elif self.content[c]["assetType"] == 'Set':
				self.sets.append(c)
			elif self.content[c]["assetType"] == 'Vehicle':
				self.vehicles.append(c)
			elif self.content[c]["assetType"] == 'Camera':
				self.cameras.append(c)
			elif self.content[c]["assetType"] == 'Light':
				self.lights.append(c)
			else:
				self.others.append(c)

	def getList(self):
		return self.content
		
	def setAssetDict(name, asset, assetType, longName = None, animated = None, position = [0,0,0], rotation = [0,0,0], scale = [1,1,1], parentAssets = []):
		tempDict = {}
		tempDict["name"] = name
		tempDict["longName"] = longName
		tempDict["asset"] = asset
		tempDict["assetType"] = assetType
		tempDict["animated"] = animated
		tempDict["position"] = position
		tempDict["rotation"] = rotation
		tempDict["scale"] = scale
		tempDict["parentAssets"] = parentAssets
		return tempDict		
		
	def createJsonPositionList(input, targetPath = None):
		toBeSaved = json.dumps(input, sort_keys=True, ensure_ascii=True, indent=4)
		
		if targetPath != None:
			if not os.path.exists(os.path.dirname(targetPath)):
				os.makedirs(os.path.dirname(targetPath))
				
			with open(targetPath, 'w') as file:
				file.write(toBeSaved)
			
		return toBeSaved
		
	def loadJsonPositionList(sourcePath):
		lines = ""

		if not os.path.exists(sourcePath):
			return None
		
		with open(sourcePath, 'r') as file:
			readFileLines = file.readlines()
			for l in readFileLines:
				lines += l
				
		return json.loads(lines)

	
def main():
	path = r"C:/test.txt"
	# createJsonPositionList({"bush001": {"animated": "", "asset": "bush", "assetType": "Prop", "longName": "PRP_bush001", "name": "bush001", "parentAssets": ["SUB_villageBakeryExt", "villageTest"], "position": [-1183.0890655517578, -223.82111549377441, -1715.1634216308594], "rotation": [-89.999995674288982, 180.00000500895632, 180.00000500895632], "scale": [1.0, 1.0, 1.0]}}, path)
	# poslist = Positionlist(path)

if __name__ == "__main__":
	main()