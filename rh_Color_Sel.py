import maya.cmds as mc

def Color():
    #Create a variable for the window name
    winName = 'Color'
    winTitle = 'Color Selection'
    #Delete the window if it exists
    if mc.window(winName, exists = True):
        mc.deleteUI(winName, window = True)
    #Build the main window
    mc.window(winName, title = winTitle, sizeable = True)
    #radioButtonGrp 
    mc.radioButtonGrp('RH_col',nrb = 3,label = 'Color:',la3 = ['Red','Blue','Yellow'],sl = 1)	
    mc.columnLayout(adjustableColumn = True)
    mc.button(label = 'Shape Spotted!', command = 'Set_ShapeCoordinate()')
    mc.columnLayout(adjustableColumn = True)
    mc.button(label = 'Target Acquire!', command = 'Set_Coordinate()')
    mc.columnLayout(adjustableColumn = True)
    #Show the window
    mc.showWindow(winName)
    mc.window(winName, edit = True, width = 378, height = 50)
    
def Set_ShapeCoordinate():
    #collection coordinate
    colorSel = mc.radioButtonGrp('RH_col',q = True,sl = True)
    sel = mc.ls(sl = 1)
    for all in sel:
        mc.setAttr (all + "Shape" + ".overrideEnabled",1)        
        if colorSel == 1:
            mc.setAttr (all + "Shape" + ".overrideColor",13)
        elif colorSel == 2:
            mc.setAttr (all + "Shape" + ".overrideColor",6)
        elif colorSel == 3:
            mc.setAttr (all + "Shape" + ".overrideColor",17)
            
def Set_Coordinate():
    #collection coordinate
    colorSel = mc.radioButtonGrp('RH_col',q = True,sl = True)
    sel = mc.ls(sl = 1)
    for all in sel:
        mc.setAttr (all + ".overrideEnabled",1)        
        if colorSel == 1:
            mc.setAttr (all + ".overrideColor",13)
        elif colorSel == 2:
            mc.setAttr (all + ".overrideColor",6)
        elif colorSel == 3:
            mc.setAttr (all + ".overrideColor",17)            
Color()    
