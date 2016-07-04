import maya.cmds as mc
import math

def fixDirection():
    #Create a variable for the window name
    winName = 'dirt'
    winTitle = 'fix_Direction'
    #Delete the window if it exists
    if mc.window(winName, exists=True):
        mc.deleteUI(winName, window=True)
    #Build the main window
    mc.window(winName, title=winTitle, sizeable=True)
    mc.textFieldButtonGrp('locatorCoord',label='locator_Coord:', text='', ed = False,buttonLabel='sel Loc',bc = 'selLoc()')
    mc.columnLayout(adjustableColumn=True)
    mc.text(l='')
    mc.textFieldButtonGrp('leaveObj',label='leave_Object:', text='', ed = False,buttonLabel='sel Leave',bc = 'selLeave()')
    mc.columnLayout(adjustableColumn=True)
    mc.text(l='')
    mc.button(label='contact', command='contact()')
    mc.columnLayout(adjustableColumn=True)
    #Show the window
    mc.showWindow(winName)
    mc.window(winName, edit=True, width=378, height=210)
        
def selLoc():
    
    global locList,locPosList
    locList = []
    locPosList = []
    
    locSel = mc.ls(sl=1)
    
    if len(locSel) > 0:
        mc.textFieldButtonGrp('locatorCoord',e=True,tx=len(locSel))
    
    for locator in locSel:
        locList.append(locator)
        
    for loc in locList:
        pos = mc.xform(loc,q = 1,t = 1,ws = 1)
        locPosList.append(pos)

def selLeave():
    global leaveList,leavePosList
    leaveList = []
    leavePosList = []
    
    leaveSel = mc.ls(sl=1)
    
    if len(leaveSel) > 0:
        mc.textFieldButtonGrp('leaveObj',e=True,tx=len(leaveSel))
    
    for leave in leaveSel:
        leaveList.append(leave)
        
    for leave in leaveList:
        pos = mc.xform(leave,q = 1,t = 1,ws = 1)
        #locPosList.append(loc)
        leavePosList.append(pos)
        
def contact():    
    #getMindistance
    for leaf in leaveList:
        pos = mc.xform(leaf,q = 1,t = 1,ws = 1)
        #tempList = []
        tempDict = {}
        for loc in locList:            
            #get the min dist
            locPos = mc.xform(loc,q = 1,t = 1,ws = 1)
            dist = math.sqrt(pow(pos[0] - locPos[0],2) + pow(pos[1] - locPos[1],2) + pow(pos[2] - locPos[2],2))
            #tempList.append(dist)
            tempDict.setdefault(loc,dist)
        #minDist = min(tempList)
        #print 'leaf' + str(minDist)
        minDistVal = min(distVal for distVal in tempDict.values())
        
        for dist in tempDict.items():
            if minDistVal in dist:
                minDistLoc = dist[0]
        #aimCnst(minDistLoc,leaf)
        mc.aimConstraint(minDistLoc,leaf,mo = 0,aim = (0,0,1),u = (0,1,0),wut = 'scene')
    
fixDirection()
