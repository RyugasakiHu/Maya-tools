#Title: rh_dynamicJoint.py
#Author:Ryugasaji Hu
#Created: Nov,03,2015
#Last Update: Nov,05,2015
#Type: Prototype 
#Version: 0.22
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

###function def
###name
def getUniqueName(side,baseName,suf):
    
    security = 1000
    
    sides = ['l','m','r']
    suffix = ['grp','loc','jj','fk','cc','iks','ik','cur','sys','fol','jc']
    
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
           
        print reversedList   
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
        self.ikDymCtrl = pm.joint(p = (0,0,0),n = getUniqueName(self.side,self.baseName,'jc'))
        pm.xform(self.ikDymCtrl,ws = 1,matrix = self.chain[-1].worldMatrix.get()) 
        pm.pointConstraint(self.chain[-1],self.ikDymCtrl)
        lockAndHideAttr(self.ikDymCtrl,["sx","sy","sz",'tx','ty','tz','rx','ry','rz'])
        self.chain[-1].v.set(0) 
         
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
        
        self.hairFol = pm.listRelatives(self.curve,p = 1)
        self.hairFol[0].pointLock.set(1)
        trashFolGrp = self.hairFol[0].getParent()        
        self.hairFol[0].setParent(w = 1)
        hairSys = pm.listConnections(self.hairFol[0] + '.outHair')
        dynCur = pm.listConnections(self.hairFol[0] + '.outCurve')
        
        pm.rename(hairSys,hairSysName)
        pm.rename(self.hairFol,self.hairFolName)
        pm.rename(dynCur,dynCurName)
        
        trashDynCurGrp = dynCur[0].getParent()
        self.hairFolGrp = pm.listRelatives(self.hairFol,p = 1)

        self.curve.setParent(self.hairFol[0])
#         pm.disconnectAttr(self.curve + 'Shape' + '.worldSpace[0]', self.ikHandle.inCurve)
        pm.disconnectAttr(curveShape.worldSpace[0], self.ikHandle.inCurve)
        dynCur[0].worldSpace[0].connect(self.ikHandle.inCurve)
        
        #clean up
        #main cc
        self.ikHandle.v.set(0)
        self.ikHandle.setParent(self.dynMainGrp)
        dynCur[0].setParent(self.dynMainGrp)
        hairSys[0].setParent(self.dynMainGrp)
        self.ikDymCtrl.setParent(self.dynMainGrp)
        
        #delete trash grp
        pm.delete(trashFolGrp,trashDynCurGrp)
        

###main def
def RH_dynamicJoint():
    #Create a variable for the window name
    winName = 'DynamicJoint'
    winTitle = 'RH_DynamicJoint_prototype_v0.1'
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
    #side
    pm.radioButtonGrp('AxisSel',nrb = 3,label = 'Axis:',la3 = ['x','y','z'],sl = 1)    
    pm.columnLayout(adjustableColumn = True)        
    #joint number
    pm.intSliderGrp('Joint_Num',label = 'Number Of Joints:',f = True,min = 4,max = 49,fmn = 1,fmx = 100,v = 4)
    pm.columnLayout(adjustableColumn = True)
    #stiffness
    pm.floatSliderGrp('Stiffness_Para',label = 'Stiffness:',f = True,min = 0.1,max = 50,fmn = 0.1,fmx = 100,v = 0.1)
    pm.columnLayout(adjustableColumn = True)
    #Damp
    pm.floatSliderGrp('Damp_Para',label = 'Damp:',f = True,min = 0.1,max = 50,fmn = 0.1,fmx = 100,v = 0.1)
    pm.columnLayout(adjustableColumn = True)        
    #Friction
    pm.floatSliderGrp('Friction_Para',label = 'Friction:',f = True,min = 1,max = 10,fmn = 0.1,fmx = 100,v = 0.1)
    pm.columnLayout(adjustableColumn = True)
    
    #button1
    pm.button(label = 'Ready For Tasking', command = 'inbound()')
    pm.columnLayout(adjustableColumn = True)
    #button2
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
    
    global jointGuides,setUpName,axis

    axisSel = pm.radioButtonGrp('AxisSel',q = True,sl = True)
    
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
      
    fk = FkChain(baseName = setUpName + 'Fk',side = side,type = 'fk',aimAxis = axis)
    fk.fromList(guidePos,guideRot,autoOrient = 1)
     
    ik = dynamicIkChain(baseName = setUpName + 'DynIk',side = side,type = 'ik')
    ik.fromList(guidePos,guideRot,autoOrient = 1)
    
    #create main Cc
    mainCtrl = Control(side,setUpName,size = 2,aimAxis = 'y') 
    mainCtrl.circleCtrl()
    
    jjPos = pm.xform(ik.chain[0],query=1,ws=1,rp=1)
    pm.move(jjPos[0],jjPos[1],jjPos[2],mainCtrl.controlGrp)
     
    jointGuidesGrp.setParent(mainCtrl.control) 
    ik.hairFol[0].setParent(mainCtrl.control)
    ik.chain[0].setParent(mainCtrl.control)
    fk.chain[0].setParent(mainCtrl.control)
    bc.chain[0].setParent(mainCtrl.control)
    
    
RH_dynamicJoint()    
