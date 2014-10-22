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

def listCams(shotName,all=False):
	camList = []
	selectetShots = [['name':""],""]
	if all:
		sel = cmds.ls(type="camera")
	else:
		sel = cmds.ls(sl=True)
	for cam in sel:
		par = cmds.listRelatives(cam,parent=True,fullPath=True)
		if par != None:
			cam = str.split(str(par[0]),'|')[1]
		if cam not in camList and "_s" in cam:
			camList += [cam]
			selectetShots["name"] += [str.split(str(cam),'_')[-1]]
	result = False
	return [selectetShots,camList]

def publishCamera():
	tk = tank.tank_from_path("W:/RTS/Tank/config")   
	scenePath = cmds.file(q=True,sceneName=True)
	scene_template = tk.template_from_path(scenePath)
	flds = scene_template.get_fields(scenePath)
	pb_template = tk.templates["shot_camera_maya_publish"]
	pb_template = tk.templates["shot_camera_work"]
	selectedCams = listCams(flds['Sequence'])
	#   faor all cams add True in list cams:
	selectedCams = listCams(flds['Sequence'],all=True)
	
	for cam in selectedCams[0]:
		flds['Shot'] = flds['Sequence']+"_"+cam
		pbPath = pb_template.apply_fields(flds)
		pathFolder = os.path.dirname(pbPath)
		if not os.path.exists(pathFolder):
			os.makedirs(pathFolder)
		cmds.select(selectedCams[i],r=True)
		cmds.file(pbPath,typ="mayaAscii",es=True)

def testDef(testVar):
	print("ultra test def! plus test var:" + str(testVar))



prevSelList = []
def selectParentLocator():
	global prevSelList
	
	sel = cmds.ls(sl=True)
	
	#if prevSelList != []:
	#	cmds.select(prevSelList)
	curPanel = cmds.getPanel(withFocus=True)
	mod = cmds.getModifiers()
	if mod == 0 and len(sel) > 1:
		print "executed"
		mod = 1 # if extra selection is more than one object but shift is not pressed clear selection and set mod to 1 so the selection is not only one object
		for obj in prevSelList:
			if obj not in sel:
				cmds.select(obj,d=True)
		prevSelList = []
	for s in sel:
		if "PRP_" in s or "PRX_" in s: # so other objects get ignored
			shape = cmds.listRelatives(s,shapes=True,fullPath=True)
			if cmds.objectType(shape[0]) != "locator":
				cmds.select(s,d=True) # clear to get rid of a selected object that might not be a locator
				parentString = cmds.listRelatives(s,parent=True,fullPath=True)
				parentList = []
				#print parentString
				if parentString != None:
					parentString = parentString[0]
					parentList += [parentString]
					for i in range(0,parentString.count('|')-1):
						parentString = str.rsplit(str(parentString),"|",1)[0]
						parentList += [parentString]
					#print parentList
					locList = []# store all parent locators in here
					for par in parentList:
						shape = cmds.listRelatives(par,shapes=True,fullPath=True)
						if shape!=None:
							if cmds.objectType(shape) == "locator":
								#print par
								locList += [par]
					if locList != []:
						loc = locList[0]
						#print loc
						#print mod
						if curPanel in cmds.getPanel(type="modelPanel"):
							if mod == 1:
								cmds.select(loc,add=True)
							if mod == 0:
								cmds.select(loc)
							prevSelList = cmds.ls(sl=True) # save the curr selection to use when adding extra selection stuff
						if curPanel in cmds.getPanel(type="outlinerPanel"):
							if mod == 1 or mod == 4:
								cmds.select(loc,add=True)
							if mod == 0:
								cmds.select(loc)
							prevSelList = cmds.ls(sl=True) # save the curr selection to use when adding extra selection stuff

# if job allready exists, delete it first
for job in cmds.scriptJob(listJobs=True):
	if "protected=True, event=['SelectionChanged', 'selectParentLocator()']" in job:
		jobNum = int(str.split(str(job),":")[0])
		cmds.scriptJob( kill=jobNum, force=True)
jobNum = cmds.scriptJob(event=["SelectionChanged","selectParentLocator()"],protected=True)