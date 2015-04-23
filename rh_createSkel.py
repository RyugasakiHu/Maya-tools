#Title: rh_createSkel.py
#Author: Ryugasaki Hu
#Created: April 22, 2015
#Last Update: April 22, 2015 
#Version: 1.0
#Description:

import maya.cmds as mc
#mc.parent('pCube1','joint_geo')    
#cube = mc.polyCube(n='joint' + '_geo',sx=1,sy=1,sz=1) 
#tx = 1
#mc.setAttr(cube[0] + '.tx',tx * 2)
joints = mc.ls(type='joint')
radius = mc.getAttr(joints[0] + '.radius')
print radius
#print tx

def createSkelGeolength():
    joints = mc.ls(type='joint')
    cube = mc.polyCube(n='joint' + '_geo',sx=1,sy=1,sz=1) 
    tx = mc.getAttr(child[0] + '.tx')
    ty = mc.getAttr(child[0] + '.tz')
    tz = mc.getAttr(child[0] + '.tz')
    
    abtx = abx(tx)
    abty = abx(ty)
    abtz = abx(tz)
    
    mc.setAttr(cube[0] + '.tx',tx * 0.5)
    mc.setAttr(cube[0] + '.tx',ty * 0.5)
    mc.setAttr(cube[0] + '.tx',tz * 0.5)
    mc.setAttr(cube[0] + '.r',0,0,0)
    
    radius = mc.getAttr(joints[0] + '.radius')
    
    
    print 
createSkelGeolength()
