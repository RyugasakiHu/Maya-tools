#comes from Jeff`s Portfolio

import maya.cmds as mc

percentRange = .1

def getValue(x,range,max):
    value = (1 - x/(range * max)) / 2
    return clamp(value,0,1)

def clamp(value,low,high):
    
    if value < low :
        return low
    
    if value > high :
        return high
    
    return value

def getShapeNode(transform):
    return

#mc.listRelatives(transform,shapes = True)[0]
(sourceObj,targetObj) = mc.ls(sl = 1)
sourceShape = getShapeNode(sourceObj)

#look at number of verticies:
mc.select(sourceObj)
numVerts = mc.polyEvaluate(v = 1)

#figure out width of face(default x axis)
rgtX = 0
lftX = 0

for i in range(0,numVerts):
    testX = mc.pointPosition(targetObj + '.vtx[' + str(i) + ']',l = 1)[0]
    
    if testX < rgtX :
        rgtX = testX
    if testX > lftX :
        lftX = testX
#duplicate face twice(left x1,right x1)
mc.select(targetObj)
targetObj_Lft = mc.duplicate(n = 'l_' + targetObj)[0]
mc.move(rgtX * -2.1,0,0,r = 1)        

mc.select(targetObj)
targetObj_Rgt = mc.duplicate(n = 'r_' + targetObj)[0]
mc.move(rgtX * 2.1,0,0,r = 1)

side = 1

#on each object
for target in ([targetObj_Lft,targetObj_Rgt]):
    side *= -1
    for i in range(0,numVerts):
        
        #get vertposition
        sourcePos = mc.pointPosition(sourceObj + '.vtx[' + str(i) + ']', l = 1)
        targetPos = mc.pointPosition(target + '.vtx[' + str(i) + ']',l = 1)
        
        #find difference
        differencePos = (sourcePos[0] - targetPos[0],sourcePos[1] - targetPos[1],sourcePos [2] - targetPos[2])

        #get falloff amount from side obj
        testX = mc.pointPosition(sourceObj + '.vtx[' + str(i) + ']',l = 1)[0]
        falloff = getValue(testX, percentRange, rgtX * side)
        
        #move vert difference * fallorr amount
        mc.xform(target + '.vtx[' + str(i) + ']',rt = (differencePos[0] * falloff,differencePos[1] * falloff,differencePos[2] * falloff))
mc.select(cl = True)
