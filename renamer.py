import pymel.core as pm

def reNamerUI():
    winName = 'reName_Tool'
    if(pm.window(winName,q=1,ex=1)):
        pm.deleteUI(winName)
    
    pm.window(winName,ret=1,mb=1)
    
    pm.columnLayout('reNameLayout',adj = 1)
    pm.textFieldGrp('pre',l = 'Prefix Name : ',tx = '',adj = 1,cl2 = ('left','left'))
    pm.radioButtonGrp('side',nrb = 3,la3 = ['left','center','right'],adj = 1,ad3 = 1)
    pm.textFieldGrp('obj',l = 'Object Name : ',tx = '',adj = 1,cl2 = ('left','left'))
    pm.textFieldGrp('starNum',l = 'Start Number : ',tx = 1,adj = 1,cl2 = ('left','left'))
    pm.textFieldGrp('paddingNum',l = 'Padding Number : ',tx = 0,adj = 1,cl2 = ('left','left'))
    pm.textFieldGrp('suffix',l = 'Suffix Name : ',tx = 'jj',adj = 1,cl2 = ('left','left'))
    pm.checkBox('je',l = 'make Last joint je',v = 1)
    
    pm.button('Select hierachy',c = 'selHierachy()')
    pm.button('Achtung!',c = 'renaming()')
    pm.showWindow(winName)

def selHierachy():
    pm.ls(sl = 1)
    pm.select(hi = 1)

def renaming():
    preName = pm.textFieldGrp('pre',q = 1,tx = 1)
    
    sideB = pm.radioButtonGrp('side',q = 1,sl = 1)
    sideList = ['l','r','m']
    
    objName = pm.textFieldGrp('obj',q = 1,tx = 1)
    startNum = pm.textFieldGrp('starNum',q = 1,tx = 1)
    paddingNum = pm.textFieldGrp('paddingNum',q = 1,tx = 1)
    suffixName = pm.textFieldGrp('suffix',q = 1,tx = 1)
    jointEnd = pm.checkBox('je',q = 1,v = 1)
    
    sels = pm.ls(sl = 1)
    
    for num,sel in enumerate(sels):
    
        if len(str(startNum)) < paddingNum:
            number = str(0) + str(startNum)
        
        preNames = ''
        
        if preName != '':
            preNames = preName + '_'
            
        name = preNames + objName + '_' + sideList[sideB] + '_' + number + '_' + suffixName
         
        pm.rename(sel,name)
    
        if jointEnd == 1:
            name = preNames + objName + '_' + sideList[sideB] + '_' + number + '_' + 'je'
            pm.rename(sels[-1],name)
            print name
        startNum = int(startNum) + 1
        
reNamerUI()
