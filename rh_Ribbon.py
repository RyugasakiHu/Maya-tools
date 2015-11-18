#Title: RH_Ribbon.py
#Author:Suchan Raj Bajracharya
#Collaborator: Ryugasaki Hu
#Created: May 21, 2015
#Last Update: Nov 18, 2015 
#Version: 0.21
#Description: Enter the name Use this Tool to automatically create a ribbon system...
#AAAAAAAAttention: Only tested in maya 2013 and 2015 version,

import maya.OpenMaya as OpenMaya
import pymel.core as pm

#name parpare
def getUniqueName(side,baseName,suf):
    
    security = 1000
    
    sides = ['l','m','r']
    suffix = ['grp','loc','jj','fk','cc','fol','folShape']
    
    if not side in sides:
        OpenMaya.MGlobal.displayError('Side is not valid')
        return
    
    if not suf in suffix:
        OpenMaya.MGlobal.displayError('Suffix is not valid')
        return
    
    name = side + '_' + baseName + '_' + str(0) +  '_' + suf
       
    i = 0
    while (pm.objExists(name) == 1):
        if(i < security):
            i += 1
            name = side + '_' + baseName + '_' + str(i) +  '_' + suf
            
    return name

#Rolling
def RH_Ribbon():
    #Create a variable for the window name
    winName = 'Ribbon'
    winTitle = 'RH_Ribbon_v0.3'
    #Delete the window if it exists
    if pm.window(winName, exists = True):
        pm.deleteUI(winName, window = True)
    #Build the main window
    pm.window(winName, title = winTitle, sizeable = True)
    #text field
    pm.textFieldGrp('RH_R_NameTFG',label = 'Ribbon_name:', text = 'Ribbon', ed = True)
    pm.columnLayout(adjustableColumn = True)
    
    #width
    pm.floatSliderGrp('RH_R_WidthFSG',label = 'Width:',f = True,min = 0.1,max = 5.0,fmn = 0.1,fmx = 100,v = 1)
    pm.columnLayout(adjustableColumn = True)
    
    #lenth
    pm.floatSliderGrp('RH_R_LengthFSG',label = 'Length:',f = True,min = 0,max = 50,fmn = 0,fmx = 100,v = 5)
    pm.columnLayout(adjustableColumn = True)
    
    #fol number
    pm.intSliderGrp('RH_R_FolNumIFG',l = 'fol Num : ',field = True,min = 5,max = 50,fmn = 1,fmx = 100,v = 5)
    pm.columnLayout(adjustableColumn = True)

    #U patch intSliderGrp 
    pm.intSliderGrp('RH_R_UISG',label = 'U patches:',field = True,min = 1,max = 10,fmn = 1,fmx = 100,v = 1)
    pm.columnLayout(adjustableColumn = True)
        
    #V patch intSliderGrp 
    pm.intSliderGrp('RH_R_VISG',label = 'V patches:',field = True,min = 1,max = 50,fmn = 1,fmx = 100,v = 5)
    pm.columnLayout(adjustableColumn = True)
    
    #button
    pm.button(label = 'Requesting for 105 shells!', command = 'Barrage()')
    pm.columnLayout(adjustableColumn = True)
    #Show the window
    pm.showWindow(winName)
    pm.window(winName, edit = True, width = 378, height = 210)
    
def Barrage():
    global UVal,VVal
    #collection coordinate
    ribbonName = pm.textFieldGrp('RH_R_NameTFG', tx = True,q = True)
    widthVal = pm.floatSliderGrp('RH_R_WidthFSG',q = True,v = True)
    lengthVal = pm.floatSliderGrp('RH_R_LengthFSG',q = True,v = True)
    folNum = pm.intSliderGrp('RH_R_FolNumIFG',q = True,v = True)
    UVal = pm.intSliderGrp('RH_R_UISG',q = True,v = True)
    VVal = pm.intSliderGrp('RH_R_VISG',q = True,v = True)
    
    #create burbs plane
    ribbonGeo = pm.nurbsPlane(p = (0,0,0),ax = (0,1,0),w = widthVal,lr = lengthVal,d = 3,u = UVal,v = VVal,ch = 1,n = (ribbonName + '_Rbbn01_geo_01_'))

    #rebuild ribbon geo
    if VVal > UVal:
        pm.rebuildSurface(ribbonGeo[0],ch = 1,rpo = 1,rt = 0,end = 1,kr = 0,kcp = 0,kc = 0,su = UVal,du = 1,sv = VVal,dv = 3,tol = 0.000155,fr = 0,dir = 2)
    if UVal > VVal:
        pm.rebuildSurface(ribbonGeo[0],ch = 1,rpo = 1,rt = 0,end = 1,kr = 0,kcp = 0,kc = 0,su = UVal,du = 3,sv = VVal,dv = 1,tol = 0.000155,fr = 0,dir = 2)
    
    #CREATE THE HAIR FOLLICLES
    folGrp = pm.group(em = 1,n = getUniqueName('m',ribbonName + '_Fol','grp')) 
    folList = []
    
    for fol in range(folNum):
        
        #createNodeName
        follicleTransName = getUniqueName('m',ribbonName,'fol')
        follicleShapeName = getUniqueName('m',ribbonName,'folShape')
        
        #createNode
        follicleShape = pm.createNode('follicle',n = follicleShapeName)
        follicleTrans = pm.listRelatives(follicleShape, parent=True)[0]
        follicleTrans = pm.rename(follicleTrans, follicleTransName)
        
        # connect the surface to the follicle
        if ribbonGeo[0].getShape().nodeType() == 'nurbsSurface':
            pm.connectAttr((ribbonGeo[0] + '.local'), (follicleShape + '.inputSurface'))
            
        #Connect the worldMatrix of the surface into the follicleShape
        pm.connectAttr((ribbonGeo[0] + '.worldMatrix[0]'), (follicleShape + '.inputWorldMatrix'))
        
        #Connect the follicleShape to it's transform
        pm.connectAttr((follicleShape + '.outRotate'), (follicleTrans + '.rotate'))
        pm.connectAttr((follicleShape + '.outTranslate'), (follicleTrans + '.translate'))
        
        #Set the uValue and vValue for the current follicle
        pm.setAttr((follicleShape + '.parameterU'), 0.5)
        pm.setAttr((follicleShape + '.parameterV'), float(1.0 / folNum) * fol + (1.0 / (folNum * 2)))
        
        #Lock the translate/rotate of the follicle
        pm.setAttr((follicleTrans + '.translate'), lock=True)
        pm.setAttr((follicleTrans + '.rotate'), lock=True)
        
        #parent
        folList.append(follicleTrans)
        follicleTrans.setParent(folGrp)
        follicleTrans.v.set(0)
      
    #CREATE JOINTS SNAPPED AND PARENTED TO THE FOLLICLE---
    jj = []
    for num,fol in enumerate(folList):
        jJoint = pm.joint(n = ribbonName + '_Rbbn0' + str(num) + '_jj',p = (0,0,0),rad = min(widthVal,lengthVal) * 1.5)
        jJoint.setParent(fol)
        jJoint.translate.set(0,0,0)
        jj.append(jJoint)
 
    #CREATE SOME TEMPORARY CLUSTERS TO PLACE THE POS LOCATORS---
    if UVal > VVal:
        vNo = UVal + 2
        pm.select(ribbonName + '_Rbbn01_geo_01_.cv[' + str(vNo) + '][0:1]',r = 1)
        pm.cluster(n = 'spCltr')
        pm.select(ribbonName + '_Rbbn01_geo_01_.cv[0][0:1]',r = 1)
        pm.cluster(n = 'epCltr')
         
    if VVal > UVal:
        vNo = VVal + 2
        pm.select(ribbonName + '_Rbbn01_geo_01_.cv[0:1][' + str(vNo) + ']',r = 1)
        pm.cluster(n = 'spCltr')
        pm.select(ribbonName + '_Rbbn01_geo_01_.cv[0:1][0]',r = 1)
        pm.cluster(n = 'epCltr')        
         
    #CREATE SOME LOCATORS---
    #CREATE START POINT LOCATORS AND PARENT THEM PROPERLY---
    spLocPos = pm.spaceLocator(p = (0,0,0), n = ribbonName + '_RbbnSp01_pos')
    spLocAim = pm.spaceLocator(p = (0,0,0), n = ribbonName + '_RbbnSp01_aim')
    spLocUp = pm.spaceLocator(p = (0,0,0), n = ribbonName + '_RbbnSp01_up')
    pm.select(spLocUp)
    spLocUpSl = pm.selected()
     
    pm.parent(spLocAim,spLocPos)
    pm.parent(spLocUp,spLocPos)
     
    #CREATE MID POINT LOCATORS AND PARENT THEM PROPERLY---
    mpLocPos = pm.spaceLocator(p = (0,0,0), n = ribbonName + '_RbbnMp01_pos')
    mpLocAim = pm.spaceLocator(p = (0,0,0), n = ribbonName + '_RbbnMp01_aim')
    mpLocUp = pm.spaceLocator(p = (0,0,0), n = ribbonName + '_RbbnMp01_up')
     
    pm.parent(mpLocAim,mpLocPos)
    pm.parent(mpLocUp,mpLocPos)    
     
    #CREATE END POINT LOCATORS AND PARENT THEM PROPERLY---
    epLocPos = pm.spaceLocator(p = (0,0,0), n = ribbonName + '_RbbnEp01_pos')
    epLocAim = pm.spaceLocator(p = (0,0,0), n = ribbonName + '_RbbnEp01_aim')
    epLocUp = pm.spaceLocator(p = (0,0,0), n = ribbonName + '_RbbnEp01_up')
    pm.select(epLocUp)
    epLocUpSl = pm.selected()
     
    pm.parent(epLocAim,epLocPos)
    pm.parent(epLocUp,epLocPos)    
     
    #CONSTRAINT EACH LOCATORS PROPERLY---                                                   
    pm.pointConstraint('spCltrHandle',spLocPos,o = (0,0,0),w = 1)                                    
    pm.delete(ribbonName + '_RbbnSp01_pos_pointConstraint1')
     
    pm.pointConstraint('epCltrHandle',epLocPos,o = (0,0,0),w = 1)                                    
    pm.delete(ribbonName + '_RbbnEp01_pos_pointConstraint1')
     
    pm.pointConstraint(spLocPos,epLocPos,mpLocPos,o = (0,0,0),w = 1)    
    pm.pointConstraint(spLocUp,epLocUp,mpLocUp,o = (0,0,0),w = 1)
     
    #OFFSET THE POSITION OF THE UP LOCATOR---
    spLocUpSl[0].ty.set(min(lengthVal,widthVal) * .5)
    epLocUpSl[0].ty.set(min(lengthVal,widthVal) * .5)     
                 
    #CREATE CTRL JOINTS
    pm.select(cl = 1)
    tx = tz = 0.0
    if VVal > UVal:
        tz = lengthVal * .2
         
    if UVal > VVal:
        tx = widthVal * .2    
     
    #FOR START POINT JOINT---
    pm.joint(p = (0,0,0),rad = min(widthVal,lengthVal) * 3 ,n = ribbonName + '_RbbnSp01_jc')
    pm.select()
    spJc = pm.selected()
    pm.joint(p = (tx * .6,0,tz * .6),rad = min(widthVal,lengthVal) * 3 ,n = ribbonName + '_RbbnSp02_jc')
    pm.joint(e = 1,zso = 1,oj = 'xyz',sao = 'yup',n = ribbonName + '_RbbnSp02_jc')

     
    #FOR MIDDLE POINT JOINT---
    pm.select(cl = 1)
    pm.joint(p = (0,0,0),rad = min(widthVal,lengthVal) * 3 ,n = ribbonName + '_RbbnMp01_jc')
    pm.select()
    mdJc = pm.selected()
    pm.joint(e = 1,zso = 1,oj = 'xyz',sao = 'yup',n = ribbonName + '_RbbnMp01_jc')
     
      
    #FOR END POINT JOINT---
    pm.select(cl = 1)
    pm.joint(p = (0,0,0),rad = min(widthVal,lengthVal) * 3 ,n = ribbonName + '_RbbnEp01_jc')
    pm.select()
    edJc = pm.selected()
    pm.joint(p = (tx * -0.6,0,tz * -0.6),rad = min(widthVal,lengthVal) * 3 ,n = ribbonName + '_RbbnEp02_jc')
    pm.joint(e = 1,zso = 1,oj = 'xyz',sao = 'yup',n = ribbonName + '_RbbnEp02_jc')   
      
    #PARENT THE CONTROL JOINTS APPROPRIATLY---
    spJc[0].setParent(spLocAim)
    mdJc[0].setParent(mpLocAim)
    edJc[0].setParent(epLocAim)
    
    spJc[0].t.set(0,0,0)
    mdJc[0].t.set(0,0,0)
    edJc[0].t.set(0,0,0)
    #APPLY THE AIM CONSTRINTS---
    aTz = 0
    if VVal > UVal:
        aTz = 1
          
    aTx = 0
    if UVal > VVal:
        aTx = 1
      
    #FOR MIDDLE POINT---
    pm.aimConstraint(ribbonName + "_RbbnSp01_pos",ribbonName + "_RbbnMp01_aim",o = (0,0,0),w = 1,aim = (aTx * -1,0,aTz *  -1),u = (0,1,0),wut = 'object',wuo = ribbonName + '_RbbnMp01_up')
    #FOR START POINT---
    pm.aimConstraint(ribbonName + "_RbbnMp01_jc",ribbonName + "_RbbnSp01_aim",o = (0,0,0),w = 1,aim = (aTx,0,aTz),u = (0,1,0),wut = 'object',wuo = ribbonName + '_RbbnSp01_up')
    #FOR END POINT---
    pm.aimConstraint(ribbonName + "_RbbnMp01_jc",ribbonName + "_RbbnEp01_aim",o = (0,0,0),w = 1,aim = (aTx * -1,0,aTz *  -1),u = (0,1,0),wut = 'object',wuo = ribbonName + '_RbbnEp01_up')
  
    #APPLY SKINCLUSTER---
    pm.select(cl = 1)
    pm.skinCluster(ribbonName + "_RbbnSp01_jc",ribbonName + "_RbbnMp01_jc",ribbonName + "_RbbnEp01_jc",ribbonName + "_Rbbn01_geo_01_",tsb = 1,ih = 1,mi = 3,dr = 4,rui = 1)
      
    #CLEAN UP
    pm.delete('spCltrHandle')
    pm.delete('epCltrHandle')
    pm.rename(ribbonName + '_Rbbn01_geo_01_',ribbonName + '_Rbbn01_geo_01')
      
    #GROUP THEM ALL
  
    pm.group(folGrp,ribbonName + '_Rbbn01_geo_01',ribbonName + '_RbbnSp01_pos',ribbonName + '_RbbnMp01_pos',ribbonName + '_RbbnEp01_pos',n = ribbonName + "_Rbbn01_grp")
    pm.xform(os = 1,piv = (0,0,0))
             
          
    print 'Target Neutralize'    
RH_Ribbon()    
