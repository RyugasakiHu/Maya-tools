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
    
