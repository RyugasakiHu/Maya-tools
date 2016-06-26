import pymel.core as pm

ptList = []
curveList = []
countList = []

part = pm.ls(sl = 1)[0]
timeMin = pm.playbackOptions(q = 1,min = 1)
timeMax = pm.playbackOptions(q = 1,max = 1)

def getUniqueName(basename,suffix):
    
    security = 1000    
    name = basename + '_' + str(0) +  '_' + suffix       
    i = 0
    while (pm.objExists(name) == 1):
        if(i < security):
            i += 1
            name = basename + '_' + str(i) +  '_' + suffix            
    return name      
    
def createCurve(particlePoint):
    ptPos = pm.getParticleAttr(particlePoint,at = 'position')
    ptCurve = pm.curve(d = 3,p = ptPos[0:3],n = getUniqueName(part,'cur'))
    curveList.append(ptCurve)

    
def addCurvePoint(particlePoint,createdCurve):
    ptPos = pm.getParticleAttr(particlePoint,at = 'position')
    pm.curve(createdCurve,a = 1,p = ptPos[0:3])   
        
def loopTime():
    for time in range(int(timeMin),int(timeMax)):
        count = pm.particle(part,q = 1,ct = 1)
        for num in range(0,count):
            pt = part + '.pt[' + str(num) + ']'
            if pt not in ptList:
                ptList.append(pt)
                createCurve(pt)
            else :
                addCurvePoint(pt,curveList[num])
        pm.currentTime(time + 1) 

if pm.currentTime() != timeMin :
    pm.currentTime(timeMin)
    loopTime()
    
else :
    loopTime()   

curveGrp = pm.group(em = 1,n = getUniqueName(part,'grp'))

for curve in curveList:
    curve.setParent(curveGrp)

         
