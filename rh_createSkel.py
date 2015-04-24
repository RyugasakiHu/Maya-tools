#Title: rh_createSkel.py
#Author: Ryugasaki Hu
#Created: April 22, 2015
#Last Update: April 24, 2015 
#Version: 1.0
#Description:

import maya.cmds as mc

def rh_createSkelGeo(input):
    input = mc.ls(sl = 1,type='joint')
    if len(input) == 0:
        print 'please select joint!'
    if len(input) > 0:
        for joints in input: 
           
        #print len(input)
        #children = mc.listRelatives(input,c=1,type='joint') 
        #for child in children:
        #print child
                
        #for joints in input:
        #print joints[]
    
def createSkelGeolength():
    joints = mc.ls(sl=1,type='joint')
    cube = mc.polyCube(n='joint1' + '_geo',sx=1,sy=1,sz=1) 
    mc.parent(cube[0],joints)
    tx = mc.getAttr(joints[0] + '.tx')
    ty = mc.getAttr(joints[0] + '.ty')
    tz = mc.getAttr(joints[0] + '.tz')
    
    abtx = abs(tx)
    abty = abs(ty)
    abtz = abs(tz)
    mc.setAttr(cube[0] + '.tx',tx * 0.5)
    mc.setAttr(cube[0] + '.ty',ty * 0.5)
    mc.setAttr(cube[0] + '.tz',tz * 0.5)
    
    mc.setAttr(cube[0] + '.r',0,0,0)
    
    radius = mc.getAttr(joints[0] + '.radius')
    
    if abtx > 0.001:
        sx = abtx
    else :    
        sx = radius
        
    if abty > 0.001:
        sy = abty
    else :    
        sy = radius
        
    if abtz > 0.001:
        sz = abtz
    else :    
        sz = radius            
    
    mc.setAttr(cube[0] + '.sx',sx)
    mc.setAttr(cube[0] + '.sy',sy)
    mc.setAttr(cube[0] + '.sz',sz)
    

    mc.select(cube[0])
    mc.makeIdentity(cube[0],t=1,s=1,r=1,a=1)

    
createSkelGeolength()    
    
rh_createSkelGeo(input)    
