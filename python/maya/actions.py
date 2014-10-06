import maya.cmds as cmds
import maya.OpenMaya as om

def setPosition(objName, pos, rot, scl):
	cmds.setAttr("%s.translateX" %objName, pos[0])
	cmds.setAttr("%s.translateY" %objName, pos[1])
	cmds.setAttr("%s.translateZ" %objName, pos[2])
	
	cmds.setAttr("%s.rotateX" %objName, rot[0])
	cmds.setAttr("%s.rotateY" %objName, rot[1])
	cmds.setAttr("%s.rotateZ" %objName, rot[2])
	
	cmds.setAttr("%s.scaleX" %objName, scl[0])
	cmds.setAttr("%s.scaleY" %objName, scl[1])
	cmds.setAttr("%s.scaleZ" %objName, scl[2])

def getPosition(objName):
	pos = cmds.xform(objName, ws=True, q=True, t=True)
	rot = cmds.xform(objName, ws=True, q=True, ro=True)
	scl = cmds.xform(objName, r=True, q=True, s=True)
	return pos, rot, scl
	
def instanceObjectFromObjects(mainObject, instanceLocators):
	for o in instanceLocators:
		if o == mainObject:
			continue
		pos, rot, scl = getPosition(o)
		cmds.delete(o)
		instanceObject(mainObject, o, pos, rot, scl)

def instanceObject(mainObject, name, pos=[0,0,0], rot=[0,0,0], scl=[1,1,1]):
	instObj = cmds.instance(mainObject, name = "%s_inst" %name)
	setPosition(instObj[0], pos, rot, scl)
	cmds.rename(instObj, name)
	return instObj

def getInstances():
	instances = []
	iterDag = om.MItDag(om.MItDag.kBreadthFirst)
	amount = 0
	while not iterDag.isDone():
		instanced = om.MItDag.isInstanced(iterDag)
		if instanced:
			instances.append(iterDag.fullPathName())
		iterDag.next()
		if amount > 2500:
			return False
		amount += 1
		
	return instances
	
def uninstance(instancesList = None):
	instances = getInstances()
	amount = 0
	while len(instances):
		parent = cmds.listRelatives(instances[0], parent=True, fullPath=True)[0]
		cmds.duplicate(parent, renameChildren=True)
		cmds.delete(parent)
		instances = getInstances()
		if amount > 10:
			return False
		amount += 1
	
def uninstanceObject(object):
	newObj = cmds.duplicate(object, name = "TempNew%s" %object, renameChildren=False)
	cmds.delete(object)
	newObj = cmds.rename(newObj[0], object)
	return newObj
		
def uninstanceFromSelection():
	selectionList = cmds.ls(selection = True)
	for o in selectionList:
		uninstanceObject(o)
	# print 'Todo uninstanceFromObject!'
	
def applyChildTransform():
	sel_objs = cmds.ls(selection = True)
	print sel_objs

	for obj in sel_objs:
		parentPos = getPosition(obj)
		children = selectChildren(sel_objs)
		print children
		if len(children) >1:
			print "offset not find - too many children"
		else:
			childPos = getPosition(children[0])
		print "parent", parentPos
		print "child", childPos
		
		setPosition(obj, childPos[0], childPos[1], childPos[2])
		setPosition(children[0],[0,0,0],[0,0,0],[1,1,1])
		
def loadReference(file, name, pos = [0,0,0], rot = [0,0,0], scl = [1,1,1]):
	print "Todo loadReference"
	
def loadProp(file, name, pos = [0,0,0], rot = [0,0,0], scl = [1,1,1], reference = True, instance = None):
	print "Load Prop : %s" %name
	prop = None
	
	if instance != None:
		prop = instanceObject(instance, name, pos, rot, scl)
		return prop
		
	if reference:
		prop = createPropReference(file, name, pos, rot, scl)
	else:
		prop = importProp(file, name, pos, rot, scl)
	return prop
	
def loadChar(file, name, pos = [0,0,0], rot = [0,0,0], scl = [1,1,1]):
	print "Todo: loadChar"
	
def importCamera(file, name):
	print 'Todo importCamera'
	loadReference(file, name)
	
def setFrameRange(in_frame, out_frame):
	# self.engine.applications["tk-multi-setframerange"]
	
	# set frame ranges for plackback
	cmds.playbackOptions(minTime=in_frame, maxTime=out_frame, animationStartTime=in_frame, animationEndTime=out_frame)
	
	# set frame ranges for rendering
	cmds.setAttr("defaultRenderGlobals.startFrame", in_frame)
	cmds.setAttr("defaultRenderGlobals.endFrame", out_frame)
	
def importProp(file, objectname, pos, rot, scl):
	print 'TODO import prop no ref.'
	
def createPropReference(file, objectname, pos, rot, scl):
	tempObjName = objectname + "_tempDouble"
	loc = cmds.spaceLocator(name = "%s_tempDouble" %objectname)
	
	tempRef = cmds.file(file, iv=True, type='mayaAscii', r=True, lrd='all', op='v=0', pn=True, ns = ":", usingNamespaces = True, returnNewNodes = True)
	
	topLevelObjects = []
	for i in tempRef:
		top = cmds.listRelatives(i, parent = True, pa = True)
		if top == None:
			topLevelObjects.append(i)
		print top
		
	cmds.parent(topLevelObjects, loc, r = True)	
	setPosition(loc,pos,rot,scl)
	tempLoc = cmds.rename(loc, objectname)
	print loc, " - ", tempLoc
	return loc