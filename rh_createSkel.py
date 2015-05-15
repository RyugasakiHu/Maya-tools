#Title: rh_createSkel.py
#Author: Ryugasaki Hu
#Created: April 22, 2015
#Last Update: May 15, 2015 
#Version: 1.0
#Description: This script is a Reverse Engineer Research from 
             #Jason Schleifer`s Animator Friendly Rigging mel script
             #js_createSkelGeo()
             #which select root joint first and generate proxy geometry on that 
             #after that he assign different color on the geo faces
             #so that it will easily to see the proxy geometry twist 
           
import maya.cmds as mc

def createSkelGeolength():
    #initial set:
    a = 1
    count = 0
    joints = mc.ls(sl=1,type='joint')       
    realchild = mc.listRelatives(c=1) 
    #shader ckeck:
    if not cmds.objExists('green'):
        green = mc.shadingNode('lambert', asShader=True,n='green')
        mc.setAttr(green + '.color',0,1,0,type = "double3")
        mc.sets(r=True,nss=True,em=True,n='greenSG') 
        mc.connectAttr('green.outColor','greenSG.surfaceShader',f=True)
        
        red = mc.shadingNode('lambert', asShader=True,n='red')
        mc.setAttr(red + '.color',1,0,0,type = "double3") 
        mc.sets(r=True,nss=True,em=True,n='redSG') 
        mc.connectAttr('red.outColor','redSG.surfaceShader',f=True)

    #ready to roll:
    for child in joints:        
        cube = mc.polyCube(n=str(child) + '_geo0' + str(a),sx=1,sy=1,sz=1)
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
            
            #set material
            sl = mc.select(cube[0] + '.f[0]')
            sl = mc.select(cube[0] + '.f[2]',add=True)
            mc.sets(fe = 'greenSG',e=True)
            
            sl = mc.select(cube[0] + '.f[1]')
            sl = mc.select(cube[0] + '.f[3]',add=True)
            mc.sets(fe = 'redSG',e=True)

            #clear history
            mc.select(cube[0])
            mc.makeIdentity(cube[0],t=1,s=1,r=1,a=1)
            
            #go head TAC-com
            a += 1
            count += 1
            
    #break the cycle delete the tail       
    mc.delete(str(child) + '_geo0' + str(a))
 
createSkelGeolength()        
