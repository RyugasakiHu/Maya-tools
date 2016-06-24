import pymel.core as pm

ptList = []
curveList = []

part = pm.ls(sl = 1)[0]
timeMin = pm.playbackOptions(q = 1,min = 1)
timeMax = pm.playbackOptions(q = 1,max = 1)
countList = []

if time != timeMin :
    pm.currentTime(timeMin)

    for time in range(int(timeMin),int(timeMax)):
    
        count = pm.particle(part,q = 1,ct = 1)
        for num in range(0,count):
            pt = part + '.pt[' + str(num) + ']'
            if pt not in ptList:
                ptList.append(pt)
            
        #for pt in ptList:
         #   ptPos = pm.getParticleAttr(pt,at = 'position')
     #       ptCurve = pm.curve(d = 3,p = ptPos[0:3])
      #      curveList.append(ptCurve)
        print count
        #print curveList
        pm.currentTime(time + 1)
        
        
#    for pt in ptList:
#        ptPos = pm.getParticleAttr(pt,at = 'position')
#        ptCurve = pm.curve(d = 3,p = ptPos[0:3])
#        curveList.append(ptCurve)
    


#    pm.currentTime(time + 1)
#    for num,pt in enumerate(ptList):
#        ptPos = pm.getParticleAttr(pt,at = 'position')
#        pm.curve(curveList[0],a = 1,p = ptPos)
        
