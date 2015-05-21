#Title: RH_Ribbon.py
#Author: Ryugasaki Hu
#Created: May 19, 2015
#Last Update: May 21, 2015 
#Version: 0.1
#Description: This script is a Reverse Engineer Research from 
            

import maya.cmds as mc

def RH_Ribbon():
    #Create a variable for the window name
    winName = 'Ribbon'
    winTitle = 'RH_Ribbon_v0.2'
    #Delete the window if it exists
    if mc.window(winName, exists = True):
        mc.deleteUI(winName, window = True)
    #Build the main window
    mc.window(winName, title = winTitle, sizeable = True)
    #text field
    mc.textFieldGrp('RH_R_NameTFG',label = 'Ribbon_name:', text = 'Ribbon', ed = True)
    mc.columnLayout(adjustableColumn = True)
    #width
    mc.floatSliderGrp('RH_R_WidthFSG',label = 'Width:',f = True,min = 0.1,max = 5.0,fmn = 0.1,fmx = 100,v = 0.1)
    mc.columnLayout(adjustableColumn = True)
    #lenth
    mc.floatSliderGrp('RH_R_LengthFSG',label = 'Length:',f = True,min = 0,max = 50,fmn = 0,fmx = 100,v = 5)
    mc.columnLayout(adjustableColumn = True)
    
    #U patch intSliderGrp 
    mc.intSliderGrp('RH_R_UISG',label = 'U patches:',field = True,min = 1,max = 10,fmn = 1,fmx = 100,v = 5)
    mc.columnLayout(adjustableColumn = True)
        
    #V patch intSliderGrp 
    mc.intSliderGrp('RH_R_VISG',label = 'V patches:',field = True,min = 1,max = 10,fmn = 1,fmx = 100,v = 5)
    mc.columnLayout(adjustableColumn = True)
    
    #radioButtonGrp 
    mc.radioButtonGrp('RH_R_ORBG',nrb = 2,label = 'Ribbon options:',la2 = ['Follicle','Non - Follicle'],sl = 1)	
    mc.columnLayout(adjustableColumn = True)
    mc.button(label = 'Requesting for 105 shells!', command = 'Barrage()')
    mc.columnLayout(adjustableColumn = True)
    #Show the window
    mc.showWindow(winName)
    mc.window(winName, edit = True, width = 378, height = 210)
    
def Barrage():
    #collection coordinate
    ribbonName = mc.textFieldGrp('RH_R_NameTFG', tx = True,q = True)
    widthVal = mc.floatSliderGrp('RH_R_WidthFSG',q = True,v = True)
    lengthVal = mc.floatSliderGrp('RH_R_LengthFSG',q = True,v = True)
    UVal = mc.intSliderGrp('RH_R_UISG',q = True,v = True)
    VVal = mc.intSliderGrp('RH_R_VISG',q = True,v = True)
    ribbonOptionVal = mc.radioButtonGrp('RH_R_ORBG',q = True,sl = True)
    print ribbonName,widthVal,lengthVal,UVal,VVal,ribbonOptionVal
    
    #create burbs plane
    ribbonGeo = mc.nurbsPlane(p = (0,0,0),ax = (0,1,0),w = widthVal,lr = lengthVal,d = 3,u = UVal,v = VVal,ch = 1,n = (ribbonName + '_Rbbn01_geo_01_'))

    #rebuild ribbon geo
    if VVal > UVal:
        mc.rebuildSurface(ribbonGeo[0],ch = 1,rpo = 1,rt = 0,end = 1,kr = 0,kcp = 0,kc = 0,su = UVal,du = 1,sv = VVal,dv = 3,tol = 0.000155,fr = 0,dir = 2)
    if UVal > VVal:
        mc.rebuildSurface(ribbonGeo[0],ch = 1,rpo = 1,rt = 0,end = 1,kr = 0,kcp = 0,kc = 0,su = UVal,du = 3,sv = VVal,dv = 1,tol = 0.000155,fr = 0,dir = 2)
        
    #clear history of ribbonGeometry
    mc.select(ribbonGeo[0],r = 1)
    mc.DeleteHistory
    mc.delete(ch = 1)
    
    #CREATE THE HAIR FOLLICLES	OR POINT ON SURFACE INFO NODES ACCORDING TO THE OPTIONS SELECTED---
    if ribbonOptionVal == 1:
        mc.select(ribbonGeo[0],r = 1)
        mc.CreateHair(VVal,UVal,10,0,0,0,0,5,0,1,1,1)
        selFols = mc.select(ribbonName + '_Rbbn01_geo_01' + '*Follicle*',r = 1)
        folGrp = mc.group(n = ribbonName + 'Rbbn01_fol_grp')
        mc.parent(w = 1)
        mc.delete('hairSystem*')
        
        selFols = mc.select(ribbonName + '_Rbbn01_geo_01' + '*Follicle*',r = 1)
        sel = mc.ls(sl = 1)
        
        for i in range(len(sel)/2):
            j = i + 1
            newName = (ribbonName + '_Rbbn0' + str(j) + '_fol')
            mc.rename(sel[i],newName)
        
        #CREATE JOINTS SNAPPED AND PARENTED TO THE FOLLICLE---
        mc.select(cl = 1)    
        for a in range(len(sel)/2):
            b = a + 1
            mc.joint(n = ribbonName + '_Rbbn0' + str(b) + '_jj',p = (0,0,0))
            mc.parent(ribbonName + '_Rbbn0' + str(b) + '_jj',ribbonName + '_Rbbn0' + str(b) + '_fol',r = True)
            mc.select(cl = 1)
            
    #FOR POINT ON SURFACE METHOD---     
    if ribbonOptionVal == 2:
        
        #ON THE BASIS OF POINT ON SURFACE INFO NODE---	
        mc.select(ribbonGeo[0])
        mc.pickWalk(d = 'down')
        ribbonGeoShape = mc.ls(sl = 1)
        
        #VERIFICATION
        if UVal > VVal:
            
            no  = UVal
            
        if VVal > UVal:    
        
            no  = VVal
        
        ribbonPosGrpVal = mc.group(em = True,n = ribbonName + '_Rbbn01_pos_grp')
        mc.xform(ws = True,piv = (0,0,0))    
        
        #EXECUTE THE MAIN LOOP---
        for i in range(no):
            POSINode = mc.createNode('pointOnSurfaceInfo')
            newName = ribbonName + '_Rbbn0' + str(i) + '_posi'
            POSIName = mc.rename(POSINode,newName)
            
            mc.connectAttr(ribbonGeoShape[0] + '.worldSpace[0]',POSIName + '.inputSurface',f = 1)
        
            if VVal > UVal :
                normVVal = abs((1.0/no) *i)
                mc.setAttr(POSIName + '.parameterV',normVVal)
                mc.setAttr(POSIName + '.parameterU',0.5)
            
            if UVal > VVal :
                normUVal = abs((1.0/no) *i)
                mc.setAttr(POSIName + '.parameterV',0.5)
                mc.setAttr(POSIName + '.parameterU',normUVal)
                
            posGrp = mc.group(em = True,n = POSIName + 'Rbbn0'+ str(i) + '_pos') 
            upGrp = mc.group(em = True,n = POSIName + 'Rbbn0'+ str(i) + '_up')  
            aimGrp = mc.group(em = True,n = POSIName + 'Rbbn0'+ str(i) + '_aim') 
        
            mc.parent(upGrp,posGrp)
            mc.parent(aimGrp,posGrp)
            mc.parent(posGrp,ribbonPosGrpVal)
            
            mc.connectAttr(POSIName + '.position',posGrp + '.translate',f = 1)
            mc.connectAttr(POSIName + '.tangentU',upGrp + '.translate',f = 1)
            mc.connectAttr(POSIName + '.tangentV',aimGrp + '.translate',f = 1)
            
            mc.select(cl = 1)
            
            JJ = mc.joint(p = (0,0,0),n = ribbonName + 'Rbbn0' + str(i) + '_jj')
            mc.parent(JJ,posGrp,r = 1)
            
            mc.select(JJ,r = 1)
            JJOff = mc.group(n = ribbonName + 'Rbbn0' + str(i) + '_jj_off')
            
            mc.aimConstraint(aimGrp,JJOff,o = (0,0,0),w = 1,aim = (0,0,1),wut = 'object',wuo = upGrp,n = 'aimConstraint_0' + str(i))

    #CREATE SOME TEMPORARY CLUSTERS TO PLACE THE POS LOCATORS---
    if UVal > VVal:
        vNo = UVal + 2
        mc.select(ribbonName + '_Rbbn01_geo_01_.cv[' + str(vNo) + '][0:1]',r = 1)
        mc.cluster(n = 'spCltr')
        mc.select(ribbonName + '_Rbbn01_geo_01_.cv[0][0:1]',r = 1)
        mc.cluster(n = 'epCltr')
        
    if VVal > UVal:
        vNo = VVal + 2
        mc.select(ribbonName + '_Rbbn01_geo_01_.cv[0:1][' + str(vNo) + ']',r = 1)
        mc.cluster(n = 'spCltr')
        mc.select(ribbonName + '_Rbbn01_geo_01_.cv[0:1][0]',r = 1)
        mc.cluster(n = 'epCltr')        
        
    #CREATE SOME LOCATORS---
    #CREATE START POINT LOCATORS AND PARENT THEM PROPERLY---
    spLocPos = mc.spaceLocator(p = (0,0,0), n = ribbonName + '_RbbnSp01_pos')
    spLocAim = mc.spaceLocator(p = (0,0,0), n = ribbonName + '_RbbnSp01_aim')
    spLocUp = mc.spaceLocator(p = (0,0,0), n = ribbonName + '_RbbnSp01_up')
    
    mc.parent(spLocAim,spLocPos)
    mc.parent(spLocUp,spLocPos)
    
    #CREATE MID POINT LOCATORS AND PARENT THEM PROPERLY---
    mpLocPos = mc.spaceLocator(p = (0,0,0), n = ribbonName + '_RbbnMp01_pos')
    mpLocAim = mc.spaceLocator(p = (0,0,0), n = ribbonName + '_RbbnMp01_aim')
    mpLocUp = mc.spaceLocator(p = (0,0,0), n = ribbonName + '_RbbnMp01_up')
    
    mc.parent(mpLocAim,mpLocPos)
    mc.parent(mpLocUp,mpLocPos)    
    
    #CREATE END POINT LOCATORS AND PARENT THEM PROPERLY---
    epLocPos = mc.spaceLocator(p = (0,0,0), n = ribbonName + '_RbbnEp01_pos')
    epLocAim = mc.spaceLocator(p = (0,0,0), n = ribbonName + '_RbbnEp01_aim')
    epLocUp = mc.spaceLocator(p = (0,0,0), n = ribbonName + '_RbbnEp01_up')
    
    mc.parent(epLocAim,epLocPos)
    mc.parent(epLocUp,epLocPos)    
    
    #CONSTRAINT EACH LOCATORS PROPERLY---                                                   
    mc.pointConstraint('spCltrHandle',spLocPos,o = (0,0,0),w = 1)	                                
    mc.delete(ribbonName + '_RbbnSp01_pos_pointConstraint1')
    
    mc.pointConstraint('epCltrHandle',epLocPos,o = (0,0,0),w = 1)	                                
    mc.delete(ribbonName + '_RbbnEp01_pos_pointConstraint1')
    
    mc.pointConstraint(spLocPos,epLocPos,mpLocPos,o = (0,0,0),w = 1)	
    mc.pointConstraint(spLocUp,epLocUp,mpLocUp,o = (0,0,0),w = 1)
    
    #OFFSET THE POSITION OF THE UP LOCATOR---
    if lengthVal > widthVal:
        offsetUp = lengthVal * .25
        
    if widthVal > lengthVal:
        offsetUp = widthVal * .25    
     
    mc.setAttr(spLocUp[0] + '.ty',offsetUp * .2)
    mc.setAttr(epLocUp[0] + '.ty',offsetUp * .2)       
                
    #CREATE CTRL JOINTS
    mc.select(cl = 1)
    tx = tz = 0.0
    if VVal > UVal:
        tz = lengthVal * .2
        
    if UVal > VVal:
        tx = widthVal * .2    
    
    #FOR START POINT JOINT---
    mc.joint(p = (0,0,0),n = ribbonName + '_RbbnSp01_jc')
    mc.joint(p = (tx * .1,0,tz * .1),n = ribbonName + '_RbbnSp02_jc')
    mc.joint(e = 1,zso = 1,oj = 'xyz',sao = 'yup',n = ribbonName + '_RbbnSp02_jc')
    
    #FOR MIDDLE POINT JOINT---
    mc.select(cl = 1)
    mc.joint(p = (0,0,0),n = ribbonName + '_RbbnMp01_jc')
    mc.joint(e = 1,zso = 1,oj = 'xyz',sao = 'yup',n = ribbonName + '_RbbnMp01_jc')
    
    #FOR END POINT JOINT---
    mc.select(cl = 1)
    mc.joint(p = (0,0,0),n = ribbonName + '_RbbnEp01_jc')
    mc.joint(p = (tx * -0.1,0,tz * -0.1),n = ribbonName + '_RbbnEp02_jc')
    mc.joint(e = 1,zso = 1,oj = 'xyz',sao = 'yup',n = ribbonName + '_RbbnEp02_jc')   
    
    #PARENT THE CONTROL JOINTS APPROPRIATLY---     
    mc.parent(ribbonName + "_RbbnSp01_jc",spLocAim[0],r = 1)
    mc.parent(ribbonName + "_RbbnMp01_jc",mpLocAim[0],r = 1)
    mc.parent(ribbonName + "_RbbnEp01_jc",epLocAim[0],r = 1)
    
    #APPLY THE AIM CONSTRINTS---
    
    
RH_Ribbon()    
