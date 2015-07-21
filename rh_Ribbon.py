#Title: RH_Ribbon.py
#Author:Suchan Raj Bajracharya
#Collaborator: Ryugasaki Hu
#Created: Dec 15, 2008
#Last Update: May 21, 2015 
#Version: 0.21
#Description: Enter the name Use this Tool to automatically create a ribbon system...
#AAAAAAAAttention: Only tested in maya 2013 and 2015 version,
                 # You need to change the hash manually 
                 # At line 74 or 77 base on the version of your maya!!!

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
    mc.floatSliderGrp('RH_R_WidthFSG',label = 'Width:',f = True,min = 0.1,max = 5.0,fmn = 0.1,fmx = 100,v = 1)
    mc.columnLayout(adjustableColumn = True)
    #lenth
    mc.floatSliderGrp('RH_R_LengthFSG',label = 'Length:',f = True,min = 0,max = 50,fmn = 0,fmx = 100,v = 5)
    mc.columnLayout(adjustableColumn = True)
    
    #U patch intSliderGrp 
    mc.intSliderGrp('RH_R_UISG',label = 'U patches:',field = True,min = 1,max = 10,fmn = 1,fmx = 100,v = 1)
    mc.columnLayout(adjustableColumn = True)
        
    #V patch intSliderGrp 
    mc.intSliderGrp('RH_R_VISG',label = 'V patches:',field = True,min = 1,max = 10,fmn = 1,fmx = 100,v = 5)
    mc.columnLayout(adjustableColumn = True)
    
    #button
    mc.button(label = 'Requesting for 105 shells!', command = 'Barrage()')
    mc.columnLayout(adjustableColumn = True)
    #Show the window
    mc.showWindow(winName)
    mc.window(winName, edit = True, width = 378, height = 210)
    
def Barrage():
    global UVal,VVal
    #collection coordinate
    ribbonName = mc.textFieldGrp('RH_R_NameTFG', tx = True,q = True)
    widthVal = mc.floatSliderGrp('RH_R_WidthFSG',q = True,v = True)
    lengthVal = mc.floatSliderGrp('RH_R_LengthFSG',q = True,v = True)
    UVal = mc.intSliderGrp('RH_R_UISG',q = True,v = True)
    VVal = mc.intSliderGrp('RH_R_VISG',q = True,v = True)
    
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
    
    #CREATE THE HAIR FOLLICLES
    mc.select(ribbonGeo[0],r = 1)
    #2013
    #mc.CreateHair(VVal,UVal,10,0,0,0,0,5,0,1,1,1)
    #2015
    mc.CreateHair(VVal,UVal,0,0,0,0,0,5,0,3,1,1)
    
    selFols = mc.select(ribbonName + '_Rbbn01_geo_01' + '*Follicle*',r = 1)
    folGrp = mc.group(n = ribbonName + '_Rbbn01_fol_grp')
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
        mc.joint(n = ribbonName + '_Rbbn0' + str(b) + '_jj',p = (0,0,0),rad = min(widthVal,lengthVal) * .25)
        mc.parent(ribbonName + '_Rbbn0' + str(b) + '_jj',ribbonName + '_Rbbn0' + str(b) + '_fol',r = True)
        mc.select(cl = 1)

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
     
    mc.setAttr(spLocUp[0] + '.ty',min(lengthVal,widthVal) * .5)
    mc.setAttr(epLocUp[0] + '.ty',min(lengthVal,widthVal) * .5)       
                
    #CREATE CTRL JOINTS
    mc.select(cl = 1)
    tx = tz = 0.0
    if VVal > UVal:
        tz = lengthVal * .2
        
    if UVal > VVal:
        tx = widthVal * .2    
    
    #FOR START POINT JOINT---
    mc.joint(p = (0,0,0),rad = min(widthVal,lengthVal) * .5,n = ribbonName + '_RbbnSp01_jc')
    mc.joint(p = (tx * .6,0,tz * .6),rad = min(widthVal,lengthVal) * .5,n = ribbonName + '_RbbnSp02_jc')
    mc.joint(e = 1,zso = 1,oj = 'xyz',sao = 'yup',n = ribbonName + '_RbbnSp02_jc')
    
    #FOR MIDDLE POINT JOINT---
    mc.select(cl = 1)
    mc.joint(p = (0,0,0),rad = min(widthVal,lengthVal) * .5,n = ribbonName + '_RbbnMp01_jc')
    mc.joint(e = 1,zso = 1,oj = 'xyz',sao = 'yup',n = ribbonName + '_RbbnMp01_jc')
    
    #FOR END POINT JOINT---
    mc.select(cl = 1)
    mc.joint(p = (0,0,0),rad = min(widthVal,lengthVal) * .5,n = ribbonName + '_RbbnEp01_jc')
    mc.joint(p = (tx * -0.6,0,tz * -0.6),rad = min(widthVal,lengthVal) * .5,n = ribbonName + '_RbbnEp02_jc')
    mc.joint(e = 1,zso = 1,oj = 'xyz',sao = 'yup',n = ribbonName + '_RbbnEp02_jc')   
    
    #PARENT THE CONTROL JOINTS APPROPRIATLY---     
    mc.parent(ribbonName + "_RbbnSp01_jc",spLocAim[0],r = 1)
    mc.parent(ribbonName + "_RbbnMp01_jc",mpLocAim[0],r = 1)
    mc.parent(ribbonName + "_RbbnEp01_jc",epLocAim[0],r = 1)
    
    #APPLY THE AIM CONSTRINTS---
    aTz = 0
    if VVal > UVal:
        aTz = 1
        
    aTx = 0
    if UVal > VVal:
        aTx = 1
    
    #FOR MIDDLE POINT---
    mc.aimConstraint(ribbonName + "_RbbnSp01_pos",ribbonName + "_RbbnMp01_aim",o = (0,0,0),w = 1,aim = (aTx * -1,0,aTz *  -1),u = (0,1,0),wut = 'object',wuo = ribbonName + '_RbbnMp01_up')
    #FOR START POINT---
    mc.aimConstraint(ribbonName + "_RbbnMp01_jc",ribbonName + "_RbbnSp01_aim",o = (0,0,0),w = 1,aim = (aTx,0,aTz),u = (0,1,0),wut = 'object',wuo = ribbonName + '_RbbnSp01_up')
    #FOR END POINT---
    mc.aimConstraint(ribbonName + "_RbbnMp01_jc",ribbonName + "_RbbnEp01_aim",o = (0,0,0),w = 1,aim = (aTx * -1,0,aTz *  -1),u = (0,1,0),wut = 'object',wuo = ribbonName + '_RbbnEp01_up')

    #APPLY SKINCLUSTER---
    mc.select(cl = 1)
    mc.skinCluster(ribbonName + "_RbbnSp01_jc",ribbonName + "_RbbnMp01_jc",ribbonName + "_RbbnEp01_jc",ribbonName + "_Rbbn01_geo_01_",tsb = 1,ih = 1,mi = 3,dr = 4,rui = 1)
    
    #CLEAN UP
    mc.delete('spCltrHandle')
    mc.delete('epCltrHandle')
    mc.rename(ribbonName + '_Rbbn01_geo_01_',ribbonName + '_Rbbn01_geo_01')
    
    #GROUP THEM ALL

    mc.delete('nucleus1')
    mc.group(ribbonName + '_Rbbn01_fol_grp',ribbonName + '_Rbbn01_geo_01',ribbonName + '_RbbnSp01_pos',ribbonName + '_RbbnMp01_pos',ribbonName + '_RbbnEp01_pos',n = ribbonName + "_Rbbn01_grp")
    mc.xform(os = 1,piv = (0,0,0))
           
        
    print 'Target Neutralize'    
RH_Ribbon()    
