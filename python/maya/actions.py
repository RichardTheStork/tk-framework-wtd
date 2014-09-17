import maya.cmds as cmds

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

def instanceObjects(mainObject, instanceLocators):
	for o in instanceLocators:
		if o == mainObject:
			continue
		print o
		pos, rot, scl = getPosition(o)
		instObj = cmds.instance(mainObject, name = "%s_inst" %o)
		setPosition(instObj[0], pos, rot, scl)
		cmds.delete(o)
		cmds.rename(instObj, o)

