#Title: RH_dynamicJoint.py
#Author:Ryugasaji Hu
#Specicsal thanks:Light Chaser Animation
#Created: Dec 15, 2008
#Last Update: May 21, 2015
#Type: Prototype 
#Version: 0.21
#Description:

import pymel.core as pm
maya.cmds.file(f = 1,new = 1)
### initial
jointGuides = []


###function def
def getUniqueName(side,basename,suf):
    
    security = 1000
    
    sides = ['l','m','r']
    suffix = ['grp','loc']
    
    if not side in sides:
        OpenMaya.MGlobal.displayError('Side is not valid')
        return
    
    if not suf in suffix:
        OpenMaya.MGlobal.displayError('Suffix is not valid')
        return
    
    name = side + '_' + basename + '_' + str(0) +  '_' + suf
       
    i = 0
    while (cmds.objExists(name) == 1):
        if(i < security):
            i += 1
            name = side + '_' + basename + '_' + str(i) +  '_' + suf
            
    return name    
###main def
def RH_dynamicJoint():
    #Create a variable for the window name
    winName = 'DynamicJoint'
    winTitle = 'RH_DynamicJoint_prototype_v0.1'
    #Delete the window if it exists
    if pm.window(winName, exists = True):
        pm.deleteUI(winName, window = True)
    #Build the main window
    pm.window(winName, title = winTitle, sizeable = True)
    #name field
    pm.textFieldGrp('NameTFG',label = 'Set up name:', text = 'Ribbon45hp', ed = True)
    pm.columnLayout(adjustableColumn = True)
    #joint number
    pm.intSliderGrp('Joint_Num',label = 'Number Of Joints:',f = True,min = 4,max = 99,fmn = 1,fmx = 100,v = 4)
    pm.columnLayout(adjustableColumn = True)
    #stiffness
    pm.floatSliderGrp('Stiffness_Para',label = 'Stiffness:',f = True,min = 0.1,max = 50,fmn = 0.1,fmx = 100,v = 0.1)
    pm.columnLayout(adjustableColumn = True)
    #Damp
    pm.floatSliderGrp('Damp_Para',label = 'Damp:',f = True,min = 0.1,max = 50,fmn = 0.1,fmx = 100,v = 0.1)
    pm.columnLayout(adjustableColumn = True)        
    #Friction
    pm.floatSliderGrp('Friction_Para',label = 'Friction:',f = True,min = 1,max = 10,fmn = 0.1,fmx = 100,v = 0.1)
    pm.columnLayout(adjustableColumn = True)
    
    #button
    pm.button(label = 'Ready For Tasking', command = 'Inbound()')
    pm.columnLayout(adjustableColumn = True)
    #Show the window
    pm.showWindow(winName)
    pm.window(winName, edit = True, width = 378, height = 210)
    
def Inbound():
    
    global jointGuides
    
    setUpName = pm.textFieldGrp('NameTFG', tx = True,q = True)
    print setUpName
    numOfJoints = pm.intSliderGrp('Joint_Num',q = True,v = True)   
    print numOfJoints
        
    for num in range(numOfJoints):
        loc = pm.spaceLocator(n = getUniqueName('m',setUpName,'loc'))
        pm.move(0,num * 2,0,loc)
        jointGuides.append(loc)
        #print jointGuides
    
RH_dynamicJoint()    
