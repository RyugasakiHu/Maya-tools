import maya.cmds as cmds

sel = cmds.ls(sl=True)
print sel
for i in sel:
    cmds.addAttr(i, ln = 'crul', at ="float",min = -10,max = 10,dv =0,h = False,k = True )
    cmds.addAttr(i, ln = 'scrunch', at ="float",min = -10,max = 10,dv =0,h = False,k = True )
    cmds.addAttr(i, ln = 'spread', at ="float",min = -10,max = 10,dv =0,h = False,k = True )
    cmds.addAttr(i, ln = 'crul_a', at ="float",min = -10,max = 10,dv =0,h = False,k = True )
    cmds.addAttr(i, ln = 'crul_b', at ="float",min = -10,max = 10,dv =0,h = False,k = True )
    cmds.addAttr(i, ln = 'crul_c', at ="float",min = -10,max = 10,dv =0,h = False,k = True )
    cmds.addAttr(i, ln = 'crul_d', at ="float",min = -10,max = 10,dv =0,h = False,k = True )
    
for i in sel:
    cmds.addAttr(i, ln = 'crul', at ="float",min = -10,max = 10,dv =0,h = False,k = True )
    cmds.addAttr(i, ln = 'thumb_crul', at ="float",min = -10,max = 10,dv =0,h = False,k = True )
    cmds.addAttr(i, ln = 'scrunch', at ="float",min = -10,max = 10,dv =0,h = False,k = True )
    cmds.addAttr(i, ln = 'thumb_scrunch', at ="float",min = -10,max = 10,dv =0,h = False,k = True )
    cmds.addAttr(i, ln = 'relax', at ="float",min = -10,max = 10,dv =0,h = False,k = True )
    cmds.addAttr(i, ln = 'cup', at ="float",min = -10,max = 10,dv =0,h = False,k = True )
    cmds.addAttr(i, ln = 'spread', at ="float",min = -10,max = 10,dv =0,h = False,k = True ) 
    cmds.addAttr(i, ln = 'thumb_spread', at ="float",min = -10,max = 10,dv =0,h = False,k = True )   


import maya.cmds as cmds

def addAttrTool():
    #Create a variable for the window name
    winName = 'blend'
    winTitle = 'rh_addAttr'
    #Delete the window if it exists
    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName, window=True)
    #Build the main window
    cmds.window(winName, title=winTitle, sizeable=True)
    cmds.textFieldButtonGrp('Obj',label='Object :', text='', ed = False,buttonLabel='Load Sel',bc = 'sel()')
    cmds.columnLayout(adjustableColumn=True)    
    cmds.textFieldGrp('Attr',l='Attribute:',text='')   

    cmds.columnLayout(adjustableColumn=True)  
    cmds.intFieldGrp(min, numberOfFields=1, label='Min Value', value1=0) 
       
    cmds.columnLayout(adjustableColumn=True) 
    cmds.intFieldGrp(max, numberOfFields=1, label='Max Value', value1=0)
    
    cmds.columnLayout(adjustableColumn=True)        
    cmds.button(label='Contact', command='Connect()')
    cmds.columnLayout(adjustableColumn=True)
    #Show the window
    cmds.showWindow(winName)
    cmds.window(winName, edit=True, width=378, height=210)

def sel():
    object = cmds.ls(selection=True)
    if len(object) > 0:
        cmds.textFieldButtonGrp('Obj',e=True,tx=object[0])

def Connect():
    attrVal = cmds.textFieldGrp('Attr',query=True,text=True)
    attrNum = attrVal.count(',') + 1
    attrLen = len(attrVal)
    new = attrVal.split(',')
    #return 0,',',',',','    
    #cmds.addAttr(i, ln = 'crul_a', at ="float",min = -10,max = 10,dv =0,h = False,k = True )
    
    print attrNum,attrLen,new,type(new),new[0]

addAttrTool()    
