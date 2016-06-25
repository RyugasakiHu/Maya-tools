import pymel.core as pm

ptList = []
curveList = []

part = pm.ls(sl = 1)[0]
timeMin = pm.playbackOptions(q = 1,min = 1)
timeMax = pm.playbackOptions(q = 1,max = 1)
countList = []
    
def createCurve(particlePoint):
    ptPos = pm.getParticleAttr(particlePoint,at = 'position')
    ptCurve = pm.curve(d = 3,p = ptPos[0:3])
    curveList.append(ptCurve)
    print ptPos
    
def addCurvePoint(particlePoint):
    ptPos = pm.getParticleAttr(particlePoint,at = 'position')
    ptCurve = pm.listConnections(particlePoint, source = True, destination = False, connections = False, plugs = True )
    print ptCurve
    #pm.curve(a = 1,p = ptPos[0:3])   
        
def loopTime():
    for time in range(int(timeMin),int(timeMax)):
        count = pm.particle(part,q = 1,ct = 1)
        for num in range(0,count):
            pt = part + '.pt[' + str(num) + ']'
            if pt not in ptList:
                ptList.append(pt)
                createCurve(pt)
            else :
                addCurvePoint(pt)           

        pm.currentTime(time + 1)
        print ptList   
  
#    for pt in ptList:
#        ptPos = pm.getParticleAttr(pt,at = 'position')
#        ptCurve = pm.curve(d = 3,p = ptPos[0:3])
#        curveList.append(ptCurve)
    
def getUniqueName():
    pass    

if pm.currentTime() != timeMin :
    pm.currentTime(timeMin)
    loopTime()
    
else :
    loopTime()
#    pm.currentTime(time + 1)
#    for num,pt in enumerate(ptList):
#        ptPos = pm.getParticleAttr(pt,at = 'position')
#        pm.curve(curveList[0],a = 1,p = ptPos)
        
