import maya.cmds as mc
import pymel.core as pm 

nameSpaceInput = 'shader'
impShader = pm.importFile("C:/Users/hzhuyongshuo/Desktop/shaderddd.ma",i = 1,typ = 'mayaAscii',
                          iv = 1,ra = 1,mnc = 0,ns = nameSpaceInput,op = 'v=0;p=17;f=0',pr = 1)
impFiles = mc.ls(nameSpaceInput + ':*')
impFileList = [] #which include some unmaterial List#
repeatShadedList = [] #temp Trash List #
shadedList = [] #objectShaded in the old file#
oldMaterialList = [] #objectShaded material in the old file#
newMaterialList = [] #new material which use for the old file#

for impFileString in impFiles:
    impFile = impFileString.split(':')
    impFileList.append(impFile[1])

for impFile in impFileList:   
    pm.hyperShade(objects=impFile)
    shadedObjShape = pm.ls(sl = 1)[0]
    shadedObj = shadedObjShape.getParent()
    repeatShadedList.append(shadedObj)

shadedList = list(set(repeatShadedList))

for shadedObj in shadedList:
    shadingEngine = pm.listConnections(shadedObj.getShape(),type = 'shadingEngine')
    if pm.connectionInfo(shadingEngine[0] + '.surfaceShader',isDestination=True):
        oldMaterial =  pm.connectionInfo(shadingEngine[0] + '.surfaceShader',sourceFromDestination=True) 
        oldMaterialList.append(oldMaterial.split('.')[0])
      
for oldMaterial in oldMaterialList:
    newPreShadedMaterial = nameSpaceInput + ':' + oldMaterial
    newMaterialList.append(newPreShadedMaterial)
    
for num,newMaterial in enumerate(newMaterialList):
    pm.select(shadedList[num])
    SG= mc.sets(renderable=True,noSurfaceShader=True,empty=True,n = newMaterial + 'SG')
    #connect shader to sg surface shader
    mc.connectAttr('%s.outColor' %newMaterial ,'%s.surfaceShader' %SG)
    mc.sets(e = 1, fe = SG)
