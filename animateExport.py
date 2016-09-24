import pymel.core as pm

def animateExportUI():
    
    winName = 'animateUI'
    if(pm.window(winName,q=1,ex=1)):
        pm.deleteUI(winName)
    pm.window(winName,ret=1,mb=1)
    pm.columnLayout('columnLayout8',adj=1)
    pm.checkBoxGrp('exportType',ncb=3, label='export Type  :  ', 
                     la3=[':  transform', ':  rotate', ':  custom'])
    pm.textFieldGrp('exportPath',l = 'export Path  :  ',adj = 0,
                      cl2 = ['right','center'],tx = 'asdd')
    pm.button('export',c = 'animateExport()')
    
    pm.showWindow(winName)
 
def animateExport():
    trans = pm.checkBoxGrp('exportType',q = 1,v1 = 1)
    rotate = pm.checkBoxGrp('exportType',q = 1,v2 = 1)
    custom = pm.checkBoxGrp('exportType',q = 1,v3 = 1)
    path = pm.textFieldGrp('exportPath',q = 1,tx = 1)
    animExport(trans,rotate,custom,path)
    
def animExport(trans,rotate,custom,path):
    
    #get all Ctrl
    ctrlList = pm.ls(sl = 1)
    print ctrlList
    
    exportLocatorList = []
    
    #prepare loc collect info
    transformLocName = 'transform_AnimExport_Loc'
    rotateLocName = 'rotate_AnimExport_Loc'
    customLocName = 'custom_AnimExport_Loc'
    
    #check loc
    #trans Loc
    if trans == 1:
        if pm.objExists(transformLocName) == False:
            transLoc = pm.spaceLocator(n = transformLocName)
            exportLocatorList.append(transLoc)
        
    #rotate Loc
    if rotate == 1:
        if pm.objExists(rotateLocName) == False:
            rotateLoc = pm.spaceLocator(n = rotateLocName)
            exportLocatorList.append(rotateLoc)
        
    #custom Loc
    if custom == 1:
        if pm.objExists(customLocName) == False:
            customLoc = pm.spaceLocator(n = customLocName)
            exportLocatorList.append(customLoc)
    
    if trans == 0 and rotate == 0 and custom == 0:         
        
        print 'plz select at least one kind of type'
        
    for item in ('tx','ty','tz','rx','ry','rz','sx','sy','sz','v'):
        if trans == 1:
            pm.setAttr(transformLocName + '.' + item,l = 1,k = 0)    
        
        if rotate == 1:
            pm.setAttr(rotateLocName + '.' + item,l = 1,k = 0) 
        
        if custom == 1:
            pm.setAttr(customLocName + '.' + item,l = 1,k = 0)
    
    ##########
    #get each ctrl 
    for ctrl in ctrlList:
        
        #get keyable attr
        allAttrList = pm.listAttr(ctrl,k = 1,u = 1,ud = 0)
        baseAttrList = allAttrList
        cusAttrList = pm.listAttr(ctrl,k = 1,u = 1,ud = 1)
        
        for cusAttr in cusAttrList:
            if cusAttr in baseAttrList:
                baseAttrList.remove(cusAttr)
        
        #print allAttrList
        #print baseAttrList
        #print cusAttrList        
        
        #print ctrl
        for attr in baseAttrList:
            #get connList
            #print attr
            connList = pm.listConnections(ctrl + '.' + attr,s = 1,d = 0)
            #trans
            if trans == 1:
                if 'translate' in attr:
                    #print ctrl + '.' + attr
                    #print connList
                    if pm.objExists(transformLocName + '.' + ctrl + '_' + attr) == False:
                           pm.addAttr(transformLocName,ln = (ctrl + '_' + attr),at = 'double')
                           pm.setAttr(transformLocName + '.' + ctrl + '_' + attr,k = 1)
                    
                    if connList == None:
                        pm.setAttr(transformLocName + '.' + ctrl + '_' + attr,
                                   pm.getAttr(transformLocName + '.' + ctrl + '.' + attr))
                    
                    #trans attr
                    else :
                        for conn in connList:
                            if 'animCurve' in pm.nodeType(conn):
                               print (ctrl + '.' + attr + ' has connection')
                               #print pm.objExists(transformLocName + ctrl + '_' + attr)
                               pm.connectAttr((conn + '.output'),(transformLocName + '.' + ctrl + '_' + attr),f = 1)
                
            #rotate
            if rotate == 1:
                if 'rotate' in attr:
                    #print ctrl + '.' + attr
                    #print connList
                    if pm.objExists(rotateLocName + '.' + ctrl + '_' + attr) == False:
                       pm.addAttr(rotateLocName,ln = (ctrl + '_' + attr),at = 'double')
                       pm.setAttr(rotateLocName + '.' + ctrl + '_' + attr,k = 1)
                   
                    if connList == None:
                        pm.setAttr(rotateLocName + '.' + ctrl + '_' + attr,
                                   pm.getAttr(rotateLocName + '.' + ctrl + '.' + attr))
                    
                    #rotate attr
                    else:
                        for conn in connList:
                            if 'animCurve' in pm.nodeType(conn):
                               print (ctrl + '.' + attr + ' has connection')
                               #print pm.objExists(rotateLocName + ctrl + '_' + attr)
                               pm.connectAttr((conn + '.output'),(rotateLocName + '.' + ctrl + '_' + attr),f = 1)    
        
        for attr in cusAttrList:
            #get connList
            #print attr
            connList = pm.listConnections(ctrl + '.' + attr,s = 1,d = 0)
            
            if pm.objExists(customLocName + '.' + ctrl + '_' + attr) == False:
               pm.addAttr(customLocName,ln = (ctrl + '_' + attr),at = 'double')
               pm.setAttr(customLocName + '.' + ctrl + '_' + attr,k = 1)
            
            if connList == None:
                pm.setAttr(customLocName + '.' + ctrl + '_' + attr,
                           pm.getAttr(customLocName + '.' + ctrl + '.' + attr))
                    
            #print ctrl + '.' + attr
            #print connList
            else:
                #cus attr
                if custom == 1:
                    for conn in connList:
                        if 'animCurve' in pm.nodeType(conn):
                           print (ctrl + '.' + attr + ' has connection')
                           #print pm.objExists(customLocName + ctrl + '_' + attr)
                           pm.connectAttr((conn + '.output'),(customLocName + '.' + ctrl + '_' + attr),f = 1)
    pm.select(cl = 1)
                     
    for exportLoc in exportLocatorList:
        pm.select(exportLoc,add = 1)
        
    maya.cmds.file(path,f = 1,op = 'v = 0;',typ = 'mayaAscii',pr = 1,es = 1)
    print 'drop Completed'

animateExportUI()



# 
# import pymel.core as pm
# import maya.cmds as mc
# sels = pm.ls(sl = 1)
# 
# print val
# print len(val)
#
#count ctrl
#create loc
#find time
#find inout angle
#key trans one by one
# 
# for sel in sels:
#     allAttr = pm.listAttr(sel,k = 1)
#     for attr in allAttr:
#         if 'translate' in attr:
#             translate = attr
#             keyCount = pm.keyframe(sel + '.' + translate,q = 1,kc=True)
#             time = pm.keyframe(sel + '.' + translate,q = 1) 
#             value = pm.keyframe(sel + '.' + translate,q = 1, t = 1) 
#             val = pm.keyTangent(sels,t = (0,24),
#                      q = 1, at='translateY',outAngle = 1,inAngle = 1,itt = 1,ott = 1)           
