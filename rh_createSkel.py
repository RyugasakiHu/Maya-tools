#Title: rh_createSkel.py
#Author: Ryugasaki Hu
#Created: April 22, 2015
#Last Update: May 14, 2015 
#Version: 1.0
#Description:

import maya.cmds as mc

def createSkelGeolength():
    a = 1
    count = 0
    joints = mc.ls(sl=1,type='joint')       
    realchild = mc.listRelatives(c=1) 
    for child in joints:        
        cube = mc.polyCube(n='joints' + '_geo0' + str(a),sx=1,sy=1,sz=1)
        mc.parent(cube,child)
        if count < (len(joints)-1):
            tx = mc.getAttr(realchild[count] + '.tx')
            ty = mc.getAttr(realchild[count] + '.ty')
            tz = mc.getAttr(realchild[count] + '.tz')
                    
            abtx = abs(tx)
            abty = abs(ty)
            abtz = abs(tz)
            
            mc.setAttr(cube[0] + '.tx',tx * 0.5)
            mc.setAttr(cube[0] + '.ty',ty * 0.5)
            mc.setAttr(cube[0] + '.tz',tz * 0.5)
            mc.setAttr(cube[0] + '.r',0,0,0)
        
            radius = mc.getAttr(child + '.radius')
        
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

            #clear history
            mc.select(cube[0])
            mc.makeIdentity(cube[0],t=1,s=1,r=1,a=1)
            
            a += 1
            count += 1
    #break the cycle delete the last one        
    mc.delete('joints' + '_geo0' + str(a))
 
createSkelGeolength()        


import maya.cmds as mc

def shadertest():   
    green = mc.shadingNode('lambert', asShader=True,n='green')
    mc.setAttr(green + '.color',0,1,0,type = "double3")
    blue = mc.shadingNode('lambert', asShader=True,n='blue')
    mc.setAttr(blue + '.color',0,0,1,type = "double3")
    
    cube = mc.polyCube(n='joints' + '_geo0',sx=1,sy=1,sz=1)
    sl = mc.select(cube[0] + '.f[0]')
    sl = mc.select(cube[0] + '.f[2]',add=True)
    mc.sets(sl,e=True,fe = 'greenSG')
    #setAttr ($lambert2[0] + ".color") -type double3 0.834 0.618693 0.323592 ;

shadertest()
