import maya.cmds as cmds

def addMultiAttr():
    #Create a variable for the window name
    winName = 'blend'
    winTitle = 'rh_addMultiAttr'
    #Delete the window if it exists
    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName, window=True)
    #Build the main window
    cmds.window(winName, title=winTitle, sizeable=True)
    cmds.textFieldButtonGrp('Obj',label='Object :', text='', ed = False,buttonLabel='Load Sel',bc = 'sel()')
    cmds.columnLayout(adjustableColumn=True)    
    cmds.textFieldGrp('Attr',l='Attribute:',text='')   

    cmds.columnLayout(adjustableColumn=True)  
    cmds.floatFieldGrp('minAttr', numberOfFields=1, label='Min Value', value1=0) 
       
    cmds.columnLayout(adjustableColumn=True) 
    cmds.floatFieldGrp('maxAttr', numberOfFields=1, label='Max Value', value1=0)
    
    cmds.columnLayout(adjustableColumn=True)        
    cmds.button(label='Contact', command='Connect()')
    cmds.columnLayout(adjustableColumn=True)
    #Show the window
    cmds.showWindow(winName)
    cmds.window(winName, edit=True, width=300, height=120)

def sel():
    object = cmds.ls(selection=True)
    if len(object) > 0:
        cmds.textFieldButtonGrp('Obj',e=True,tx=object[0])

def Connect():
    attrVal = cmds.textFieldGrp('Attr',query=True,text=True)
    attrNum = attrVal.count(',') + 1
    attrList = attrVal.split(',')
    minVal = cmds.floatFieldGrp('minAttr', q = True,v = True)
    maxVal = cmds.floatFieldGrp('maxAttr', q = True,v = True)
    obj = cmds.ls(selection=True)    
    
    for attr in range(len(attrList)):          
        cmds.addAttr(obj, ln = attrList[attr], at ="float",min = minVal[0],max = maxVal[0],dv =0,h = False,k = True )

addMultiAttr()
