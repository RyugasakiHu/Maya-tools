import maya.cmds as mc
import maya.mel as mel
import math

mc.select('pCylinder1')
geo = mc.ls(sl = 1)[0]
skinCluster = mel.eval('findRelatedSkinCluster '+ geo)
vertex = mc.polyEvaluate(geo,v = 1)
joints = mc.skinCluster(skinCluster,q = 1,inf = 1)
skinList = {}

for num in range(0,vertex):
    vertex = geo + '.vtx[' + str(num) + ']'
    vertPos = mc.xform(vertex,q = 1,t = 1,ws = 1)
    tempDict = {}

    for joint in joints:
        jntPos = mc.xform(joint,q = 1,t = 1,ws = 1)
        dist = math.sqrt(pow(vertPos[0] - jntPos[0],2) + pow(vertPos[1] - jntPos[1],2) + pow(vertPos[2] - jntPos[2],2))
        tempDict.setdefault(joint,dist)
        
    minDistVal = min(distVal for distVal in tempDict.values())

    for joint in tempDict.keys(): 
        if minDistVal == tempDict[joint]:
            if joint not in skinList:
                skinList[joint] = []
            skinList[joint].append(vertex)
            
for item in skinList.items():
    joint =  item[0]
    vertex = item[1]
    for vert in vertex:
        mc.skinPercent(skinCluster,vert,transformValue = (joint,1))
        
        
        
        
        
