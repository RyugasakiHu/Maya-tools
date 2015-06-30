#Title: rh_connectBlend.py
#Author: Jason Schleifer`s
#Collaborator: Ryugasaki Hu
#Created: I don`t know maybe decade year`s ago~
#Last Update: April 17, 2015 
#Version: 1.1
#Description: I found this script from Jason Schleifer`s
             # Animator Friendly Rigging mel script
             #js_connectBlendUI () and js_connectBlend ()
             #which connect a color blend between two select objects
             #then output to a target objects
             #finally use a fourth object`s Attribute to ctrl it
             #in Jason Schleifer`s lesson he use that to IK/FK switch

import maya.cmds as cmds

def ConnectBlend():
    #Create a variable for the window name
    winName = 'blend'
    winTitle = 'Connect_Blend'
    #Delete the window if it exists
    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName, window=True)
    #Build the main window
    cmds.window(winName, title=winTitle, sizeable=True)
    cmds.textFieldButtonGrp('Obj1',label='Object 1(blender=0):', text='', ed = False,buttonLabel='Load Sel',bc = 'sel1()')
    cmds.columnLayout(adjustableColumn=True)
    cmds.textFieldButtonGrp('Obj2',label='Object 2(blender=1):', text='', ed = False,buttonLabel='Load Sel',bc = 'sel2()')
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(l='')
    cmds.textFieldButtonGrp('Tar',label='Target Object:', text='', ed = False,buttonLabel='Load Sel',bc = 'selT()')
    cmds.columnLayout(adjustableColumn=True)
    cmds.textFieldGrp('Attr',l='Attribute:',text='')
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(l='')
    cmds.textFieldGrp('Driv',l='Driver (optional):',text='')
    cmds.columnLayout(adjustableColumn=True)
    cmds.button(label='Contact', command='Connect()')
    cmds.columnLayout(adjustableColumn=True)
    #Show the window
    cmds.showWindow(winName)
    cmds.window(winName, edit=True, width=378, height=210)

def sel1():
    global object1
    object1 = cmds.ls(selection=True)
    if len(object1) > 0:
        cmds.textFieldButtonGrp('Obj1',e=True,tx=object1[0])
        
def sel2():
    global object2
    object2 = cmds.ls(selection=True)
    if len(object1) > 0:
        cmds.textFieldButtonGrp('Obj2',e=True,tx=object2[0])   

def selT():
    global target
    target = cmds.ls(selection=True)
    if len(target) > 0:
        cmds.textFieldButtonGrp('Tar',e=True,tx=target[0])      
          
def Connect():
    global attrval,drivenval
    
    #get value
    obj1val = cmds.textFieldButtonGrp('Obj1',e=True,tx=object1[0])
    obj2val = cmds.textFieldButtonGrp('Obj2',e=True,tx=object2[0])
    toval = cmds.textFieldButtonGrp('Tar',e=True,tx=target[0])    
    attrval = cmds.textFieldGrp('Attr',query=True,text=True)
    drivenval = cmds.textFieldGrp('Driv',query=True,text=True)
    
    if drivenval.find('.') == -1:
        cmds.error('Driver must be object.attribute')
    else:    
        #create node 
        BC = cmds.createNode('blendColors',n = target[0] + '_' + attrval + '_BCN')
    
        #connect node    
        cmds.connectAttr((object1[0] + '.' + attrval),(BC + '.color2'))
        cmds.connectAttr((object2[0] + '.' + attrval),(BC + '.color1'))
        cmds.connectAttr((BC + '.output'),(target[0] + '.' + attrval))
        cmds.connectAttr(drivenval,(BC + '.blender'))

ConnectBlend() 
