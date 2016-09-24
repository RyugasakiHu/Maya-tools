import pymel.core as pm

def isKeyAble(name):
    keyable = 0
    
    if (pm.getAttr(name,l = 1) == False) and (len(pm.listConnections(name,s = 1,d = 0)) == 0):
        keyable = 1

    return keyable


path = "C:/Users/AUV/Documents/maya/projects/default/asdd.ma"
#maya.cmds.file(path,i = 1,typ = "mayaAscii",iv = 1,ra = 1,mnc = 0,ns = '',op = 'v = 0',pr = 1)

importLoc = pm.ls('asdd:*',typ = 'locator')
importLocList = []

for loc in importLoc:
    #print loc
    if 'transform' in str(loc):
        transformLoc = loc.getParent()
        importLocList.append(transformLoc)
    
    elif 'rotate' in str(loc):
        rotateLoc = loc.getParent()
        importLocList.append(rotateLoc)
     
    elif 'custom' in str(loc):
        customLoc = loc.getParent()
        importLocList.append(customLoc)
        
for loc in importLocList:

    locAttrList = pm.listAttr(loc,k = 1)
    #print locAttrList
    
    for locAttr in locAttrList: 
        ctrlName = locAttr.split('__')[0]
        attrName = locAttr.split('__')[1]
     
        if pm.objExists(ctrlName + '.' + attrName):
            #print ctrlName + '.' + attrName
            connList = pm.listConnections(loc + '.' + locAttr,s = 1,d = 0,scn = 1)
            if isKeyAble(ctrlName + '.' + attrName):
                if len(connList) != 0:
                    if 'animCurve' in pm.nodeType(connList[0]):
                        pm.connectAttr((connList[0] + '.output'),(ctrlName + '.' + attrName),f = 1) 
                        
                    else :
                        value = pm.getAttr(loc + '.' + locAttr)
                        pm.setAttr((ctrlName + '.' + attrName),value)
                    
            else :
                print ctrlName + '.' + attrName + ' is locked or connected, skipping~~~'
                
        else:
            print 'can not find ' + ctrlName + '.' + attrName + ' in the scene, skipping...'
                
