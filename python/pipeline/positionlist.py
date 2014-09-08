import os, json


class Positionlist:
	path = ""
	content = None
	
	def __init__(self, path):
		self.setPath(path)
		self.load()
		return None
			
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
		self.content = loadJsonPositionList(path)
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
			if c[assetType] == 'Prop':
				self.props.append(c)
			elif c[assetType] == 'Character':
				self.characters.append(c)
			elif c[assetType] == 'Set':
				self.sets.append(c)
			elif c[assetType] == 'Vehicle':
				self.vehicles.append(c)
			elif c[assetType] == 'Camera':
				self.cameras.append(c)
			elif c[assetType] == 'Light':
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
	lines = None
	
	if not os.path.exists(sourcePath):
		return None
	
	with open(sourcePath, 'r') as file:
		lines = file.readlines()

	return json.loads(lines)

	
def main():
	poslist = Positionlist()
	print poslist.getList()

if __name__ == "__main__":
	main()