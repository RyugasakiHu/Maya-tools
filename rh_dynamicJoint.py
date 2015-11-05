#Title: rh_dynamicJoint.py
#Author:Ryugasaki Hu
#Created: Nov,03,2015
#Last Update: Nov,05,2015
#Type: Prototype 
#Version: 0.23
#Description:

import pymel.core as pm
import maya.mel as mel
import maya.OpenMaya as OpenMaya
maya.cmds.file(f = 1,new = 1)

### initial
jointGuides = []
setUpName = None
jointGuidesGrp = None 
side = None
axis = None
mainCtrl = None
size = None

###function def
###name
def getUniqueName(side,baseName,suf):
    
    security = 1000
    
    sides = ['l','m','r']
    suffix = ['grp','loc','jj','fk','cc','iks','ik','cur','sys','fol','jc','BCN']
    
    if not side in sides:
        OpenMaya.MGlobal.displayError('Side is not valid')
        return
    
    if not suf in suffix:
        OpenMaya.MGlobal.displayError('Suffix is not valid')
        return
    
    name = side + '_' + baseName + '_' + str(0) +  '_' + suf
       
    i = 0
    while (pm.objExists(name) == 1):
        if(i < security):
            i += 1
            name = side + '_' + baseName + '_' + str(i) +  '_' + suf
            
    return name

###zero
def zero(obj):
    #get parent object 
    par = obj.getParent()
    
    #create group name
    name = obj.name()
    temp = name.split('_')
    groupName = getUniqueName(temp[0], temp[1], 'grp')
    if not groupName:
        OpenMaya.MGlobal.displayError('Error generating name')
        return
    
    #create group
    grp = pm.createNode('transform', n =groupName)
    
    #set martix
    matrix = obj.wm.get()
    grp.setMatrix(matrix)
    #rebuild hierachy
    obj.setParent(grp)
    if par:
        grp.setParent(par)
    return grp

###lockAndHideAttr
def lockAndHideAttr(objName,attrs):
    '''
    this function lock and Hide attrs
    @para attrs: list
    '''
    
    if not objName:
        return
    
    for attr in attrs:
        pm.setAttr(objName + "." + attr,l=True,k=False,cb=False)
def addFloatAttr(objName,attrs,minV,maxV):
    
    '''
    this function add single/multiple attr
    @para attrs: list 
    '''
    
    if not objName:
        return 
    for attr in attrs:
        pm.addAttr(objName, ln = attr, at ="double",min = minV,max = maxV,dv = 0,h = False,k = True )
###Control class
class Control(object):
    
    def __init__(self, side,baseName,size,aimAxis):
    
        self.baseName = baseName
        self.side = side
        self.size = size
        self.aimAxis = aimAxis
        self.control = None
        
    def circleCtrl(self):
        controlName = getUniqueName(self.side,self.baseName,'cc')
        if controlName :
            if self.aimAxis == 'x':
                dic = [1,0,0]
                
            elif self.aimAxis == 'y':
                dic = [0,1,0]
                
            elif self.aimAxis == 'z':
                dic = [0,0,1]
                
            self.control = pm.circle(name = controlName,ch = 0,o = 1 ,nr = dic,r = self.size)[0]
            pm.makeIdentity(self.control,apply = True,t = 0,r = 0,s = 1,n = 0,pn = 1)
            self.controlGrp = zero(self.control)     
            self.__colorSet()
    
    def __colorSet(self):
        for shape in self.control.getShapes():
            #open override
            shape.overrideEnabled.set(1)
            if self.side == 'm':
                shape.overrideColor.set(17) 
            elif self.side == 'l':
                shape.overrideColor.set(6) 
            elif self.side == 'r':        
                shape.overrideColor.set(13)           
    
###class def
###BoneChain class
class BoneChain(object):
    
    def __init__(self,baseName,side,type):
        '''
        Constructor
        '''
        self.baseName = baseName
        self.side = side
        self.type = type
        
        self.chain = []
        
    def fromList(self,posList = [],orientList = [],autoOrient = 1):
        
        for i in range(len(posList)):
            
            tempName = getUniqueName(self.side,self.baseName,self.type)
            if i == len(posList) - 1:
                tempName = getUniqueName(self.side,self.baseName,self.type)
                
            pm.select(cl = 1)
            
            if autoOrient == 1:
                
                tempJnt = pm.joint(n = tempName,position = posList[i])
                
            else :
                tempJnt = pm.joint(n = tempName,position = posList[i],orientation = orientList[i])
            
            self.chain.append(tempJnt)
        self.__parentJoints()
         
        if autoOrient == 1:
            #pm.joint(self.chain[0].name(),e = 1,oj = 'yzx',secondaryAxisOrient = 'zup',ch = 1)
            pm.joint(self.chain[0].name(),e = 1,oj = 'xyz',secondaryAxisOrient = 'zdown',ch = 1)

        self.__zeroOrientJoint(self.chain[-1])

    def chainLength(self):
        'return length'
         
        return len(self.chain)
    
    def __str__(self):
        
        result = 'BoneChain class , length : {l}, chain : '.format(l = self.chainLength()) 
        chainName = [obj.name() for obj in self.chain]        
        result += str(chainName)
        
        return result

    def __zeroOrientJoint(self,bone):
        'zero out the jointOrient'
        for a in ['jointOrientX','jointOrientY','jointOrientZ']:
            bone.attr(a).set(0)     
                    
    
    def __parentJoints(self):
        'parent a list of joints'
        reversedList = list(self.chain)
        reversedList.reverse()
         
        for i in range(len(reversedList)):
            if i != (len(reversedList)-1):
                pm.parent(reversedList[i],reversedList[i+1])
                
    @staticmethod           
    def blendTwoChains(chain1,chain2,resChain,attrHolder,attrName,baseName,side):
        
        blnTArray = []
        blnRArray = []
        blnSArray = []
        
        data = {'blendTranslate':blnTArray,
                'blendRotate':blnRArray,
                'blendScale':blnSArray
                }
        
        if attrHolder.hasAttr(attrName) == 0:
            attrHolder.addAttr(attrName,at = 'float',min = 0,max = 1,dv = 0,k = 1)
            
        for i,b in enumerate(resChain):
            
            blnT = getUniqueName(side,baseName + 'Tra','BCN')    
            blnR = getUniqueName(side,baseName + 'Rot','BCN') 
            blnS = getUniqueName(side,baseName + 'Sca','BCN') 
            
            if not blnT or not blnR or not blnS:
                return
            
            blnNodeT = pm.createNode('blendColors', n = blnT)
            blnNodeR = pm.createNode('blendColors', n = blnR)
            blnNodeS = pm.createNode('blendColors', n = blnS)
            
            chain1[i].t.connect(blnNodeT.color2)
            chain2[i].t.connect(blnNodeT.color1)
            
            chain1[i].r.connect(blnNodeR.color2)
            chain2[i].r.connect(blnNodeR.color1)
            
            chain1[i].s.connect(blnNodeS.color2)
            chain2[i].s.connect(blnNodeS.color1)
        
            blnNodeT.output.connect(b.t)
            blnNodeS.output.connect(b.s)
            blnNodeR.output.connect(b.r)
        
            blnTArray.append(blnNodeT)
            blnRArray.append(blnNodeR)
            blnSArray.append(blnNodeS)
            
            attrHolder.attr(attrName).connect(blnNodeT.blender)
            attrHolder.attr(attrName).connect(blnNodeR.blender)
            attrHolder.attr(attrName).connect(blnNodeS.blender)
        
        return data                

###fkChain Class
class FkChain(BoneChain):

    def __init__(self, baseName,side,size = 1.5,fkCcType = 'shape',type = 'fk',
                 pointCnst = 1,aimAxis = axis):
        '''
        Constructor
        '''
        self.baseName = baseName
        self.side = side
        self.size = size
        self.fkType = type
        self.fkCcType = fkCcType
        self.controlsArray = []
        self.pointCnst = pointCnst
        self.aimAxis = axis
        self.__acceptedCcTypes = ['shape','cc']
        self.__acceptedFkTypes = ['fk','jj']
                
        self.__checkFkType()
        
        if self.fkType == 'fk':
            BoneChain.__init__(self, baseName, side,type = self.fkType)
        
        else :    
            BoneChain.__init__(self, baseName, side,type = 'jj')
            
    def fromList(self,posList = [],orientList = [],autoOrient = 1,skipLast = 1):
        '''
        posList position
        orientList orient
        autoOrient bool whether use autoOrient List or not
        skipLast =whether add the last jj cc
        '''
        
        res = self.__checkCcType()
        if not res :
            return
        
        BoneChain.fromList(self, posList, orientList, autoOrient)
        
        self.__addControls(skipLast)        
        
        if self.fkCcType == self.__acceptedCcTypes[0]:        
            self.__finalizeFkChainShape()
            
        else:
            self.__finalizeFkChainOriCnst() 
        
    def __addControls(self,skipLast = 1):
        
        for i in range(self.chainLength()):
            #the last loop condition
            if skipLast == 1:
                if i ==(self.chainLength() - 1):
                    return
            #create control for each one    
            ctrl = Control(self.side,self.baseName,self.size,self.aimAxis) 
            ctrl.circleCtrl()
            #snap to the control
            #que xform
            pm.xform(ctrl.controlGrp,ws = 1,matrix = self.chain[i].worldMatrix.get())                        
            self.controlsArray.append(ctrl.controlGrp)                                
            
    def __finalizeFkChainOriCnst(self):        
           
        reversedList = list(self.controlsArray)
        reversedList.reverse()
            
        for i in range(len(reversedList)):
            if i != (len(reversedList)-1):
                pm.parent(reversedList[i][0].getParent(),reversedList[i+1][0])
                
        #orient cnst        
        for num,ctrl in enumerate(self.controlsArray):
            lockAndHideAttr(ctrl[0],["sx","sy","sz"])
            pm.orientConstraint(ctrl,self.chain[num],mo = 1)
            if self.pointCnst == 1:
                pm.pointConstraint(ctrl,self.chain[num],mo = 1)

    def __finalizeFkChainShape(self):
         
        reversedList = list(self.controlsArray)
        reversedList.reverse()
           
        #parent shape        
        for i,c in enumerate(self.controlsArray):
            pm.parent(c.getChildren()[0].getShape(),self.chain[i],r=1,s=1)
         
        #delete grp   
        for i in range(len(reversedList)):
            pm.delete(reversedList[i])         
            
    def __checkCcType(self):
        '''
        whether the Cc is valid
        @return:bool
        '''                 
        
        if not self.fkCcType in self.__acceptedCcTypes :
            OpenMaya.MGlobal.displayError('plz provide a valid type , accept value are :' + ','.join(self.__acceptedCcTypes))
            return False
        return True            
    
    def __checkFkType(self):
        '''
        whether the fkJj is valid
        @return:bool
        '''                 
        
        if not self.fkType in self.__acceptedFkTypes :
            OpenMaya.MGlobal.displayError('plz provide a valid type , accept value are :' + ','.join(self.__acceptedFkTypes))
            return False
        return True

###Dynamic Ik class
class dynamicIkChain(BoneChain):

    def __init__(self, baseName,side,size = 1,solver = 'ikSCsolver',
                 controlOrient = [0,0,0],type = 'ikSC'):    
        '''
        Constructor
        '''
        #init
        self.baseName = baseName
        self.side = side
        self.size = size
        self.solver = solver
        self.controlOrient = controlOrient
        self.type = type
        self.__acceptedSolvers = ['ikSCsolver','ikRPsolver']
        
        #cc
        self.dynMainGrp = None
        self.ikDymCtrl = None
        self.ikHandle = None
        self.ikEffector = None
        self.curve = None
        self.hairFol = None
        
        BoneChain.__init__(self,baseName,side,type = self.type)
        
    def fromList(self,posList = [],orientList = [],autoOrient = 1):
        '''
        posList position
        orientList orient
        autoOrient bool whether use autoOrient List or not
        skipLast =whether add the last jj cc
        '''
        self.dynMainGrp = pm.group(em = 1,n = getUniqueName(self.side,self.baseName + 'Main','grp'))
        BoneChain.fromList(self, posList, orientList, autoOrient)
         
        #create ctrl:
        self.ikDymCtrl = pm.joint(p = (0,0,0),rad = self.size * 4,n = getUniqueName(self.side,self.baseName,'jc'))
        pm.xform(self.ikDymCtrl,ws = 1,matrix = self.chain[-1].worldMatrix.get()) 
        pm.pointConstraint(self.chain[-1],self.ikDymCtrl)
        lockAndHideAttr(self.ikDymCtrl,["sx","sy","sz",'tx','ty','tz','rx','ry','rz','v'])
        self.chain[-1].v.set(0)
        
        #open override
        self.ikDymCtrl.overrideEnabled.set(1)
        if self.side == 'm':
            self.ikDymCtrl.overrideColor.set(17) 
        elif self.side == 'l':
            self.ikDymCtrl.overrideColor.set(6) 
        elif self.side == 'r':        
            self.ikDymCtrl.overrideColor.set(13)     
        
        
         
        #create entire
        #perpare Name
        ikName = getUniqueName(self.side,self.baseName,'iks')
        baseCurName = getUniqueName(self.side,self.baseName + 'Base','cur')
        dynCurName = getUniqueName(self.side,self.baseName + 'Dyn','cur')
        hairSysName = getUniqueName(self.side,self.baseName + 'Hair','sys')
        self.hairFolName = getUniqueName(self.side,self.baseName,'fol')
        
        #create IK
        self.ikHandle,self.ikEffector,self.curve = pm.ikHandle(sj = self.chain[0],ee = self.chain[-1],solver = 'ikSplineSolver',n = ikName,ns = 3)
        pm.rename(self.curve,baseCurName)
        pm.select(self.curve)
        curveShape = self.curve.getShape()
        
        #make curve dynamic 
        mel.eval('makeCurvesDynamicHairs 1 0 1')
        
        #arrangement new items 
        self.hairFol = pm.listRelatives(self.curve,p = 1)
        self.hairFol[0].pointLock.set(1)
        trashFolGrp = self.hairFol[0].getParent()        
        self.hairFol[0].setParent(w = 1)
        hairSys = pm.listConnections(self.hairFol[0] + '.outHair')
        dynCur = pm.listConnections(self.hairFol[0] + '.outCurve')
        nucleus = pm.listConnections(hairSys[0] + '.stf')[0]
        
        pm.rename(hairSys,hairSysName)
        pm.rename(self.hairFol,self.hairFolName)
        pm.rename(dynCur,dynCurName)
        
        trashDynCurGrp = dynCur[0].getParent()
        self.hairFolGrp = pm.listRelatives(self.hairFol,p = 1)

        self.curve.setParent(self.hairFol[0])
        pm.disconnectAttr(curveShape.worldSpace[0], self.ikHandle.inCurve)
        dynCur[0].worldSpace[0].connect(self.ikHandle.inCurve)
        
        #add ctrl attr
        #stiffness
        pm.addAttr(self.ikDymCtrl,at = 'double',ln = 'stiff',dv = 0.001)
        pm.setAttr(self.ikDymCtrl + '.stiff',e = 0,keyable = 1)
        
        #damping
        pm.addAttr(self.ikDymCtrl,at = 'double',ln = 'damping',dv = 0.05)
        pm.setAttr(self.ikDymCtrl + '.damping',e = 0,keyable = 1)
        
        #drag
        pm.addAttr(self.ikDymCtrl,at = 'double',ln = 'drag',dv = 0)
        pm.setAttr(self.ikDymCtrl + '.drag',e = 0,keyable = 1)
        
        #friction
        pm.addAttr(self.ikDymCtrl,at = 'double',ln = 'friction',dv = 0.5)
        pm.setAttr(self.ikDymCtrl + '.friction',e = 0,keyable = 1)
        
        #mass
        pm.addAttr(self.ikDymCtrl,at = 'double',ln = 'mass',dv = 1)
        pm.setAttr(self.ikDymCtrl + '.mass',e = 0,keyable = 1)
           
        #gravity
        pm.addAttr(self.ikDymCtrl,at = 'double',ln = 'gravity',dv = 0.98)
        pm.setAttr(self.ikDymCtrl + '.gravity',e = 0,keyable = 1)
        
        #start_frame
        pm.addAttr(self.ikDymCtrl,at = 'double',ln = 'start_frame',dv = 1)
        pm.setAttr(self.ikDymCtrl + '.start_frame',e = 0,keyable = 1)        
        
        #startCurveAttraction
        pm.addAttr(self.ikDymCtrl,at = 'double',ln = 'start_curve_attract',dv = 0)
        pm.setAttr(self.ikDymCtrl + '.start_curve_attract',e = 0,keyable = 1)            
        
#         #template
#         pm.addAttr(self.ikDymCtrl,at = 'double',ln = 'tat',dv = 0.001)
#         pm.setAttr(self.ikDymCtrl + '.tat',e = 0,keyable = 1)        

        self.ikDymCtrl.stiff.connect(hairSys[0].getShape().stiffness)
        self.ikDymCtrl.damping.connect(hairSys[0].getShape().damp)
        self.ikDymCtrl.drag.connect(hairSys[0].getShape().drag)
        self.ikDymCtrl.friction.connect(hairSys[0].getShape().friction)
        self.ikDymCtrl.mass.connect(hairSys[0].getShape().mass)
        self.ikDymCtrl.gravity.connect(hairSys[0].getShape().gravity)
        self.ikDymCtrl.start_curve_attract.connect(hairSys[0].getShape().startCurveAttract)
        pm.disconnectAttr(nucleus.stf,hairSys[0].getShape().startFrame)
        self.ikDymCtrl.start_frame.connect(hairSys[0].getShape().startFrame)
        nucleus[0].v.set(0)
        
        #clean up
        #main cc
        self.ikHandle.v.set(0)
        self.ikHandle.setParent(self.dynMainGrp)
        dynCur[0].setParent(self.dynMainGrp)
        hairSys[0].setParent(self.dynMainGrp)
        self.ikDymCtrl.setParent(self.dynMainGrp)
        self.curve.v.set(0)
        hairSys[0].v.set(0)
        
        #delete trash grp
        pm.delete(trashFolGrp,trashDynCurGrp)
        
###main def
def rh_dynamicJoint():
    #Create a variable for the window name
    winName = 'DynamicJoint'
    winTitle = 'rh_DynamicJoint_prototype_v0.23'
    #Delete the window if it exists
    if pm.window(winName, exists = True):
        pm.deleteUI(winName, window = True)
    #Build the main window
    pm.window(winName, title = winTitle, sizeable = True)
    #name field
    pm.textFieldGrp('NameTFG',label = 'Set up name:', text = 'Ribbon45hp', ed = True)
    pm.columnLayout(adjustableColumn = True)
    #side
    pm.radioButtonGrp('ColSel',nrb = 3,label = 'Side:',la3 = ['l','m','r'],sl = 1)    
    pm.columnLayout(adjustableColumn = True)
    #axis
    pm.radioButtonGrp('AxisSel',nrb = 3,label = 'Axis:',la3 = ['x','y','z'],sl = 1)    
    pm.columnLayout(adjustableColumn = True)
    #ccSize
    pm.floatSliderGrp('Cc_Size',label = 'Control Size:',f = True,min = 1,max = 10,fmn = 1,fmx = 100,v = 1)
    pm.columnLayout(adjustableColumn = True)
    #joint number
    pm.intSliderGrp('Joint_Num',label = 'Number Of Joints:',f = True,min = 4,max = 49,fmn = 1,fmx = 100,v = 4)
    pm.columnLayout(adjustableColumn = True)
    
    #inbound
    pm.button(label = 'Ready For Tasking', command = 'inbound()')
    pm.columnLayout(adjustableColumn = True)
    #bringTheRain
    pm.button(label = 'Target Acquire', command = 'bringTheRain()')
    pm.columnLayout(adjustableColumn = True)    
    
    #Show the window
    pm.showWindow(winName)
    pm.window(winName, edit = True, width = 378, height = 210)
    
def inbound():
    
    global jointGuides,setUpName,jointGuidesGrp,side
    setUpName = pm.textFieldGrp('NameTFG', tx = True,q = True)
    colorSel = pm.radioButtonGrp('ColSel',q = True,sl = True) 
    
    if colorSel == 1:
        side = 'l'
    elif colorSel == 2:    
        side = 'm'
    elif colorSel == 3:    
        side = 'r'
        
    numOfJoints = pm.intSliderGrp('Joint_Num',q = True,v = True)   
    jointGuidesGrp = pm.group(em = 1,n = getUniqueName(side,setUpName + 'Gud', 'grp'))                
        
    for num in range(numOfJoints):
        loc = pm.spaceLocator(n = getUniqueName(side,setUpName,'loc'))
        pm.move(0,num * 2,0,loc)
        jointGuides.append(loc)
        loc.setParent(jointGuidesGrp)
    
    jointGuides.reverse()
    for num,loc in enumerate(jointGuides):
        if num < (len(jointGuides) - 1):
            jointGuides[num].setParent(jointGuides[num + 1])
    jointGuides.reverse()   
    
def bringTheRain():
    
    global jointGuides,setUpName,axis,size,side
    axisSel = pm.radioButtonGrp('AxisSel',q = True,sl = True)
    size = pm.floatSliderGrp('Cc_Size',q = True,v = True)  
    
    if axisSel == 1:
        axis = 'x'
    elif axisSel == 2:    
        axis = 'y'
    elif axisSel == 3:    
        axis = 'z'    
    
    jointGuidesGrp.v.set(0)    
    guidePos = [x.getTranslation(space = 'world') for x in jointGuides]
    guideRot = [x.getRotation(space = 'world') for x in jointGuides]   
     
    bc = BoneChain(baseName = setUpName,side = side,type = 'jj')
    bc.fromList(guidePos,guideRot,autoOrient = 1)  
      
    fk = FkChain(baseName = setUpName + 'Fk',side = side,size = size,type = 'fk',aimAxis = axis)
    fk.fromList(guidePos,guideRot,autoOrient = 1)
     
    ik = dynamicIkChain(baseName = setUpName + 'DynIk',side = side,type = 'ik')
    ik.fromList(guidePos,guideRot,autoOrient = 1)
    
    #create main Cc
    mainCtrl = Control(side,setUpName,size = size * 1.5,aimAxis = axis) 
    mainCtrl.circleCtrl()
    pm.xform(mainCtrl.controlGrp,ws = 1,matrix = ik.chain[0].worldMatrix.get()) 
#     jjPos = pm.xform(ik.chain[0],query=1,ws=1,rp=1)
#     pm.move(jjPos[0],jjPos[1],jjPos[2],mainCtrl.controlGrp)
    
    blendData = BoneChain.blendTwoChains(fk.chain,ik.chain,bc.chain,
                                         mainCtrl.control,'Dynamic',setUpName,side)
    
    lockAndHideAttr(mainCtrl.control , ['sx','sy','sz']) 
    jointGuidesGrp.setParent(ik.dynMainGrp) 
    ik.hairFol[0].setParent(mainCtrl.control)
    ik.chain[0].setParent(mainCtrl.control)
    fk.chain[0].setParent(mainCtrl.control)
    bc.chain[0].setParent(mainCtrl.control)
    
    
rh_dynamicJoint()    
