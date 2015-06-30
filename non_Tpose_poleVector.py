from maya import cmds,OpenMaya

sel = cmds.ls(sl = 1)

start = cmds.xform(sel[0],q = 1,ws = 1,t = 1)
mid = cmds.xform(sel[1],q = 1,ws = 1,t = 1)
end = cmds.xform(sel[2],q = 1,ws = 1,t = 1)

startV = OpenMaya.MVector(start[0],start[1],start[2])
midV = OpenMaya.MVector(mid[0],mid[1],mid[2])
endV = OpenMaya.MVector(end[0],end[1],end[2])

startEnd = endV - startV
startMid = midV - startV

dotP = startMid * startEnd
#dotP is a vector which vertical the plane

proj = float(dotP) / float(startEnd.length())
#(shadow of a )
startEndN = startEnd.normal()

projV = startEndN * proj

arrowV = startMid - projV

finalV = arrowV + midV


loc = cmds.spaceLocator()[0]

cmds.xform(loc,ws = 1,t = (finalV.x * 2,finalV.y * 2,finalV.z * 2))

