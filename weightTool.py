#===============================================================================================
# Author: SunDongDong
# WinProc: sdd_weightTools()
# E-mail: 136941679@qq.com
# Company: China-Najing-OF3D
# Version: 4.4.7
#===============================================================================================

from maya.cmds import *
import maya.mel as mm
import sys
import datetime
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import math
import os


def sdd_weightTools():

    if(window('sdd_weightToolsWin',q=1,ex=1)):
        deleteUI('sdd_weightToolsWin',window=1)
    windowPref('sdd_weightToolsWin',ra=1)
    window('sdd_weightToolsWin',rtf=1,menuBar=1,s=1,t='sdd_weightTools v4.4.7')
    #Menu

    menu(l='Weight',to=1)
    menuItem(l='Save',c='sdd_saveWeight()')
    menuItem(l='Load',c='sdd_loadWeight()')
    menuItem(divider=True)
    menuItem(l='Relax',c='sdd_relaxWeight()')
    menuItem(divider=True)
    menuItem(l='Copy',c='CopySkinWeightsOptions()')
    menuItem(l='Mirror',c='MirrorSkinWeightsOptions()')

    menu(l='Pose',to=1)
    menuItem(l='Create Pose Sets',c='sdd_createSelectionSets()')
    menuItem(divider=True)
    menuItem(l='Reset To Pose',c='sdd_resetToZero(".t")')
    

    menu(l='Help',to=1)
    menuItem(l='NanJing-OriginalForce')
    menuItem(divider=True)
    menuItem(l='Author:SunDongDong')
    menuItem(l='E-mail:136941679@qq.com')


    #FormLayout
    formLayout('wtMainFormFL')
    columnLayout('mwtMainCL')
    #Main Mode Icon
    newV=False
    if(int(about(v=1)[0:4])>2010):
        newV=True

    bstyle='etchedOut'
    MainFLW=208
    if(newV):
        bstyle='etchedIn'
        MainFLW=210

    iconWH=34
    font='tinyBoldLabelFont'

    rw=[55,54,55,50]
    if(newV):
        rw=[50,50,50,50]

    frameLayout('wtMainTypeFL',cll=0,cl=0,bs=bstyle,w=MainFLW,bv=1,lv=0,mh=3,mw=3)
    columnLayout('wtMainTypeCL')
    rowLayout(nc=4,cw4=rw,cal=[(1,'center'),(2,'center'),(3,'center'),(4,'center')])
    iconTextButton('wtMTNoneITB',iol='None',fn=font,st='iconAndTextVertical',ann='None',i='polySphere.xpm',w=iconWH,h=iconWH,c='sdd_noneModeProc()')
    iconTextButton('wtMTDeformITB',ann='Dform',fn=font,st='iconAndTextVertical',i='paintSetMembership.xpm',w=iconWH,h=iconWH,c='sdd_deformModeProc()')
    iconTextButton('wtMTPaintITB',ann='Paint',fn=font,i='paintSkinWeights.xpm',w=iconWH,h=iconWH,c='sdd_paintModeProc()')
    iconTextButton('wtMTVertexITB',ann='Vertex',fn=font,i='polyMergeVertex.xpm',w=iconWH,h=iconWH,c='sdd_vertexModeProc()')

    progressBar('wtMainPrograssPB',p='wtMainTypeCL',h=10,w=MainFLW-10,vis=0)
    checkBoxGrp('artisanRampUseRamp',p='wtMainTypeCL',vis=0)

####Paint Layout
    columnLayout('wtPaintTMainCL',p='wtMainFormFL')
    frameLayout('wtPaintTopFL',cll=0,cl=0,bs=bstyle,w=MainFLW,bv=1,lv=0,mh=3,mw=3)
    columnLayout('wtPaintTopCL',adj=1)

    #Deform Type
    columnLayout('wtPTDeformersCL',adj=1,vis=0)
    rowLayout(nc=3,cw3=[35,35,90])
    iconTextButton('wtDTClusterITB',w=iconWH,h=iconWH,iol='Clust',image='paintCluster.xpm',c='sdd_changeDeformType("Clust")')
    iconTextButton('wtDTBlendITB',w=iconWH,h=iconWH,en=1,image='paintBlendshape.xpm',c='sdd_changeDeformType("Blend")')
    iconTextButton('wtDTWireITB',w=iconWH,h=iconWH,en=1,image='paintWire.xpm',c='sdd_changeDeformType("Wire")')
    #iconTextButton(iol='PM',ann='Paint Membership',st='iconAndTextVertical',w=iconWH,h=iconWH,image='paintSetMembership.xpm',c='sdd_paintSetMembershipProc()')

    #Paint Top
    columnLayout('wtPTSkinCL',p='wtPaintTopCL',adj=1)
    #Filter

    rowLayout(p='wtPTSkinCL',nc=2,cw2=[20,175])
    iconTextButton('wtSkinMatchModeITB',i1='filtersOff.xpm',w=20,h=23,c='sdd_clearSkinMatchString()')
    popupMenu()
    menuItem('wtPaintMatchInverseMI',l='Inverse',cb=0,c='sdd_skinListMatchString()')

    menuItem('wtListM',l='List',sm=1)
    menuItem(l='Sort',sm=1,to=1)
    radioMenuItemCollection()
    menuItem('wtListSortHMI',l='Hierarchy',rb=1,c='sdd_sortList()')
    menuItem('wtListSortAMI',l='Alphabetically',rb=0,c='sdd_sortList()')
    menuItem('wtListSortLMI',l='Lock',rb=0,c='sdd_sortList()')
    menuItem(divider=True,p='wtListM')
    menuItem('wtListZeroMI',p='wtListM',l='Filter Zero',cb=0,c='sdd_filterZeroList()')
    menuItem(divider=True,p='wtListM')
    menuItem(p='wtListM',l='Smooth List',c='sdd_smoothPaintSkinList()')


    textField('wtPaintMatchTF',w=175,cc='sdd_skinListMatchString()')
    popupMenu('wtFilterPM')
    menuItem(d=1)
    menuItem(l='Add To Filter',c='sdd_sendToFilter()')


    #Paint Influence List
    textScrollList('wtPaintListTSL',p='wtMainFormFL',ams=1,pma=1,h=150,sc='sdd_paintScrollListSelectChange()',dcc='sdd_lockUnlockInfoScrollList()',vis=1)
    popupMenu('wtPaintInfluencePM')
    menuItem(l='Lock/Unlock',c='sdd_lockUnlockInfoScrollList()')
    menuItem(l='Lock All',c='sdd_lockUnlockAllInfoScrollList(1)')
    menuItem(l='Unlock All',c='sdd_lockUnlockAllInfoScrollList(0)')
    menuItem(d=1)
    menuItem(l='Vertex This',c='sdd_paintVertexThis()')
    menuItem(d=1)
    menuItem(l='Select All',c='sdd_selectPaintListObject()')

    #Bottom
    columnLayout('wtPaintBMainCL',p='wtMainFormFL')
    frameLayout('wtPaintBtmFL',cll=0,cl=0,bs=bstyle,w=MainFLW,bv=1,lv=0,mh=3,mw=3)
    columnLayout('wtPaintBtmCL')
    #1
    rowLayout(nc=3,cw3=[60,70,50])
    text(l='Opetation:')
    radioCollection()
    radioButton('wtPOabsoluteRB',l='Replace',sl=1,cc='sdd_changePaintOperationType("absolute")')
    radioButton('wtPOadditiveRB',l='Add',cc='sdd_changePaintOperationType("additive")')
    #2
    rowLayout(p='wtPaintBtmCL',nc=3,cw3=[60,70,50])
    text(l='')
    radioButton('wtPOscaleRB',l='Scale',cc='sdd_changePaintOperationType("scale")')
    radioButton('wtPOsmoothRB',l='Smooth',cc='sdd_changePaintOperationType("smooth")')
    separator(p='wtPaintBtmCL',style="none",h=5)
    #3
    PaintBtmCLRW=28
    bh=25
    if(newV):
        PaintBtmCLRW=27
    rowLayout(p='wtPaintBtmCL',nc=7,cw=[(1,PaintBtmCLRW),(2,PaintBtmCLRW),(3,PaintBtmCLRW),(4,PaintBtmCLRW),(5,PaintBtmCLRW),(6,PaintBtmCLRW),(7,PaintBtmCLRW)],cal=[(1,'center'),(2,'center'),(3,'center'),(4,'center'),(5,'center'),(6,'center'),(7,'center')])
    button('wtPValueB1',h=bh,w=PaintBtmCLRW-1,l='-',c='sdd_adjustPaintValue("-")')
    button('wtPValueB2',h=bh,w=PaintBtmCLRW-1,l='.02',c='sdd_setPaintValue(.02)')
    button('wtPValueB3',h=bh,w=PaintBtmCLRW-1,l='.1',c='sdd_setPaintValue(.1)')
    button('wtPValueB4',h=bh,w=PaintBtmCLRW-1,l='.25',c='sdd_setPaintValue(.25)')
    button('wtPValueB5',h=bh,w=PaintBtmCLRW-1,l='.5',c='sdd_setPaintValue(.5)')
    button('wtPValueB6',h=bh,w=PaintBtmCLRW-1,l='.75',c='sdd_setPaintValue(.75)')
    button('wtPValueB7',h=bh,w=PaintBtmCLRW-1,l='+',c='sdd_adjustPaintValue("+")')
    popupMenu()
    radioMenuItemCollection()
    menuItem('wtPVAdjustASMI',l='Add/Sub',rb=1)
    menuItem('wtPVAdjustMDMI',l='Mul/Div',rb=0)
    if(newV):
        button('wtPValueB7',e=1,w=PaintBtmCLRW-2)
        button('wtPValueB1',e=1,w=PaintBtmCLRW-2)

    separator(p='wtPaintBtmCL',style="none",h=5)
    #4
    rowLayout(p='wtPaintBtmCL',nc=3,cw3=[35,45,100])
    iconTextButton(l='Value:',w=35,h=20,st='textOnly',fn='smallPlainLabelFont',c='sdd_endsPaintValue()',dcc='sdd_endsPaintValue()')
    floatField('wtPaintValueFF',v=0,w=45,min=0, max=1,cc='sdd_changePaintValueFiled()')
    floatSlider('wtPaintValueFS',min=0, max=1,w=118,cc='sdd_changePaintValueSlider()')
    separator(p='wtPaintBtmCL',style="none",h=5)
    #5

    FloodBW=197
    if(newV):
        FloodBW=200
    button(p='wtPaintBtmCL',l='Flood',w=FloodBW,h=30,c='sdd_floodPaintCtx()')
    separator(p='wtPaintBtmCL',style="none",h=5)
    #6
    button('wtPaintCheckB',p='wtPaintBtmCL',l='Check flying',w=FloodBW,h=30,c='sdd_checkPaintCtxFlying()',bgc=(0,1,0))

####Vertex Layout
    columnLayout('wtVertexMainCL',p='wtMainFormFL',vis=0)

    frameLayout('wtVtxLayoutFL',cll=0,cl=0,bs=bstyle,w=MainFLW,bv=1,lv=0,mh=3,mw=3)
    columnLayout('wtVtxLayoutCL',adj=1)
    #
    bh=28#Botton Height
    #1
    Vtx1RW=39#RowLayout with
    if(newV):
        Vtx1RW=38
    rowLayout(nc=5,cw5=[Vtx1RW,Vtx1RW,Vtx1RW+2,Vtx1RW,Vtx1RW],cal=[(1,'center'),(2,'center'),(3,'center'),(4,'center'),(5,'center')])
    button(h=bh,w=Vtx1RW-2,l='Shri',c='ShrinkPolygonSelectionRegion()')
    button(h=bh,w=Vtx1RW-2,l='Grow',c='GrowPolygonSelectionRegion()')
    button(h=bh,w=Vtx1RW,l='Elem',c='sdd_selectElemVtx()')
    button(h=bh,w=Vtx1RW-2,l='Mirr',c='sdd_selectMirrorVtx()')
    button(h=bh,w=Vtx1RW-2,l='Last',c='sdd_selectLastVtx()')
    separator(p='wtVtxLayoutCL',style="none",h=5)
    #2
    Vtx2W=[28,27,27]#RowLayout Height
    if(newV):
        Vtx2W=[26,26,27]

    columnLayout('wtVertexValueCL',p='wtVtxLayoutCL')
    rowLayout(p='wtVertexValueCL',nc=7,cw=[(1,Vtx2W[0]),(2,Vtx2W[0]),(3,Vtx2W[0]),(4,Vtx2W[0]),(5,Vtx2W[0]),(6,Vtx2W[0]),(7,Vtx2W[0])],cal=[(1,'center'),(2,'center'),(3,'center'),(4,'center'),(5,'center'),(6,'center'),(7,'center')])
    button(h=bh,w=Vtx2W[1],l='0',c='sdd_vertexSetAbsWeight(0)')
    button(h=bh,w=Vtx2W[2],l='.1',c='sdd_vertexSetAbsWeight(.1)')
    button(h=bh,w=Vtx2W[2],l='.25',c='sdd_vertexSetAbsWeight(.25)')
    button(h=bh,w=Vtx2W[1],l='.5',c='sdd_vertexSetAbsWeight(.5)')
    button(h=bh,w=Vtx2W[2],l='.75',c='sdd_vertexSetAbsWeight(.75)')
    button(h=bh,w=Vtx2W[2],l='.9',c='sdd_vertexSetAbsWeight(.9)')
    button(h=bh,w=Vtx2W[1],l='1',c='sdd_vertexSetAbsWeight(1)')
    separator(p='wtVertexValueCL',style="none",h=5)
    #3
    Vtx3W=[35,35,60,35,35]
    if(newV):
        Vtx3W=[33,33,60,33,33]
    rowLayout(p='wtVertexValueCL',nc=5,cw5=Vtx3W,cal=[(1,'center'),(2,'center'),(4,'center'),(5,'center')])
    button(h=bh,w=30,l='*',c='sdd_vertexChangeWeight("*",0)')
    button(h=bh,w=30,l='/',c='sdd_vertexChangeWeight("/",0)')
    floatField('wtVtxAddValueFF',v=0.05,pre=4,min=0,max=1,w=55,h=bh)
    button(h=bh,w=30,l='+',c='sdd_vertexChangeWeight("+",0)')
    button(h=bh,w=30,l='-',c='sdd_vertexChangeWeight("-",0)')

    separator(p='wtVertexValueCL',style="none",h=5)


    #4
    Vtx5W=[41,41,47,65]
    if(newV):
        Vtx5W=[38,40,47,65]
    rowLayout('',p='wtVertexValueCL',nc=4,cw4=Vtx5W,cal=[(1,'center'),(2,'center'),(4,'center')])
    button(h=bh,w=38,l='Copy',c='sdd_vertexCopyWeight()')
    button(h=bh,w=38,l='Paste',c='sdd_vertexPasteWeight()')
    text(l='')
    button('wtVtxSmoothB',h=bh,w=65,l='Smooth',c='sdd_vertexChangeWeight("smooth",0)')

    separator(p='wtVertexValueCL',style="none",h=5)

    #5
    iconTextButton('wtSelJntNameT',p='wtVtxLayoutCL',h=15,st='iconAndTextCentered',al='left',l='Please Select Vertex !',w=195,bgc=[0,1,0])

    #iconTextButton(l='Color',w=40,st='textOnly',fn='smallPlainLabelFont')

    popupMenu()
    menuItem(l='Change To Closte Joint',c='sdd_vertexClosetJoint()')

    separator(p='wtVtxLayoutCL',style="none",h=5)

    rowLayout(p='wtVtxLayoutCL',nc=2,cw2=[30,165])
    iconTextButton('wtVtxShowMod',h=20,w=30,bgc=[0.5,0.5,0.5],l='All',st='textOnly',c='sdd_vertexInfoShowMode()')
    if(int(about(v=1)[0:4])!=2011):
        floatSliderGrp('wtVtxValue',f=1,cw2=(35,130),adj=2,min=0,max=1,fmn=0,fmx=1,pre=3,cc='sdd_vertexSliderChange()')
    else:
        floatSliderGrp('wtVtxValue',f=1,cw2=(35,100),adj=2,ad2=1,min=0,max=1,fmn=0,fmx=1,pre=3,cc='sdd_vertexSliderChange()')


    #Vertex List
    textScrollList('wtVertexListTSL',ams=1,pma=1,p='wtMainFormFL',w=195,sc='sdd_vertexScrollListSelectChange()',vis=0)
    popupMenu('wtInfoPM')
    menuItem(l='Lock/Unlock',c='sdd_lockUnlockInfoScrollList()')
    menuItem(l='Lock All',c='sdd_lockUnlockAllInfoScrollList(1)')
    menuItem(l='Unlock All',c='sdd_lockUnlockAllInfoScrollList(0)')
    menuItem(d=1)
    menuItem(l='Paint This',c='sdd_vertexPaintThis()')



    #Paint Layout
    listB=174
    bw=2#Border Width
    if(newV):
        listB=181
        bw=0

    formLayout('wtMainFormFL',e=1,af=[('wtPaintTMainCL','top',bw),('wtPaintTMainCL','left',bw),('wtPaintTMainCL','right',bw),('wtPaintListTSL','left',bw),('wtPaintListTSL','right',bw),('wtPaintListTSL','bottom',listB),('wtPaintBMainCL','left',bw),('wtPaintBMainCL','right',bw),('wtPaintBMainCL','bottom',bw)])
    formLayout('wtMainFormFL',e=1,ac=[('wtPaintListTSL','top',bw,'wtPaintTMainCL'),('wtPaintTMainCL','top',bw,'mwtMainCL'),('wtPaintBMainCL','top',bw,'wtPaintListTSL')])
    #Vertex Layout
    formLayout('wtMainFormFL',e=1,af=[('mwtMainCL','left',bw),('mwtMainCL','top',bw),('mwtMainCL','right',bw),('wtVertexMainCL','left',bw),('wtVertexMainCL','top',bw),('wtVertexMainCL','right',bw),('wtVertexListTSL','bottom',bw),('wtVertexListTSL','left',bw),('wtVertexListTSL','right',bw)])
    formLayout('wtMainFormFL',e=1,ac=[('wtVertexListTSL','top',bw,'wtVertexMainCL'),('wtVertexMainCL','top',bw,'mwtMainCL')])

    showWindow('sdd_weightToolsWin')
    sdd_showPaintLayout(1)
    sdd_showVertexLayout(0)
    sdd_enableVertexLayout(0)
    sdd_enablePaintLayout(0)
    sdd_enableVertexMenu(0)



#Windows Proc
def sdd_resetToZero(attr):
    global cntTList
    for i in cntTList:
        try:
            cnt=i[0]
            for a in i[1]:
                if(attr=='t' and (a[0]=='tx' or a[0]=='ty' or a[0]=='tz')):
                    setAttr(cnt+'.'+a[0],a[1])
                elif(attr=='r' and (a[0]=='rx' or a[0]=='ry' or a[0]=='rz')):
                    setAttr(cnt+'.'+a[0],a[1])
                else:
                    setAttr(cnt+'.'+a[0],a[1])
        except:
            pass


def sdd_paintListPopupMenuSwitch(typ):
    popupMenu('wtPaintInfluencePM',e=1,dai=1)
    if(typ=='Skin'):
        menuItem(p='wtPaintInfluencePM',l='Lock/Unlock',c='sdd_lockUnlockInfoScrollList()')
        menuItem(p='wtPaintInfluencePM',l='Lock All',c='sdd_lockUnlockAllInfoScrollList(1)')
        menuItem(p='wtPaintInfluencePM',l='Unlock All',c='sdd_lockUnlockAllInfoScrollList(0)')
        menuItem(p='wtPaintInfluencePM',d=1)
        menuItem(p='wtPaintInfluencePM',l='Vertex This',c='sdd_paintVertexThis()')
        menuItem(p='wtPaintInfluencePM',d=1)
        menuItem(p='wtPaintInfluencePM',l='Select Object',c='sdd_selectPaintListObject()')
    elif(typ=='Clust' or typ=='Wire'):
        menuItem(p='wtPaintInfluencePM',l='Add To This',c='sdd_addToScollListSets("Add")')
        menuItem(p='wtPaintInfluencePM',l='Remove From This',c='sdd_addToScollListSets("Remove")')
        menuItem(p='wtPaintInfluencePM',d=1)
        menuItem(p='wtPaintInfluencePM',l='Paint Membership',c='sdd_paintSetMembershipProc()')
        
def sdd_ToggleToolSettings():
    if not(checkBoxGrp('artisanRampUseRamp',q=1,ex=1)):
        checkBoxGrp('artisanRampUseRamp',q=1,ex=1)

    ToggleToolSettings()
    ToggleToolSettings()


def sdd_clearSkinMatchString():
    iconTextButton('wtSkinMatchModeITB',e=1,i1='filtersOff.xpm')
    textField('wtPaintMatchTF',e=1,tx='')
    sdd_loadPaintScrollList()

def sdd_changeWindowSize(typ):
    winH=window('sdd_weightToolsWin',q=1,h=1)
    if(typ=='-'):
        winH=winH-80
    else:
        winH=winH+80
    window('sdd_weightToolsWin',e=1,h=winH)
def sdd_refreshWindow():
    winW=window('sdd_weightToolsWin',q=1,w=1)
    window('sdd_weightToolsWin',e=1,w=winW)


def sdd_changeMainIconLable(typ):
    if(typ=='None'):
        iconTextButton('wtMTNoneITB',e=1,iol='None')
    else:
        iconTextButton('wtMTNoneITB',e=1,iol='')
    if(typ=='Dform'):
        iconTextButton('wtMTDeformITB',e=1,iol='Dform')
    else:
        iconTextButton('wtMTDeformITB',e=1,iol='')
    if(typ=='Paint'):
        iconTextButton('wtMTPaintITB',e=1,iol='Paint')
    else:
        iconTextButton('wtMTPaintITB',e=1,iol='')
    if(typ=='Vertex'):
        iconTextButton('wtMTVertexITB',e=1,iol='Vertx')
    else:
        iconTextButton('wtMTVertexITB',e=1,iol='')


def sdd_changeDeformType(typ):
    if(typ=='Clust'):
        iconTextButton('wtDTClusterITB',e=1,iol='Clust')
    else:
        iconTextButton('wtDTClusterITB',e=1,iol='')
    if(typ=='Blend'):
        iconTextButton('wtDTBlendITB',e=1,iol='Blend')
    else:
        iconTextButton('wtDTBlendITB',e=1,iol='')
    if(typ=='Wire'):
        iconTextButton('wtDTWireITB',e=1,iol='Wire')
    else:
        iconTextButton('wtDTWireITB',e=1,iol='')
    sdd_deformModeProc()


def sdd_paintSetMembership():
    PaintSetMembershipTool()
    sel=textScrollList('wtPaintListTSL',q=1,si=1)
    set=listConnections(sel[0]+'.message')[0]
    curCtx=currentCtx()
    artSetPaintCtx(curCtx,e=1,stm=set)

def sdd_changePaintValueSlider():
    value=floatSlider('wtPaintValueFS',q=1,v=1)
    floatField('wtPaintValueFF',e=1,v=value)
    sdd_changePaintCtxValue()
def sdd_changePaintValueFiled():
    value=floatField('wtPaintValueFF',q=1,v=1)
    floatSlider('wtPaintValueFS',e=1,v=value)
    sdd_changePaintCtxValue()

#Layout Visbility
def sdd_showVertexLayout(typ):
    columnLayout('wtVertexMainCL',e=1,vis=typ)
    textScrollList('wtVertexListTSL',e=1,vis=typ)

def sdd_showPaintLayout(typ):
    columnLayout('wtPaintTMainCL',e=1,vis=typ)
    textScrollList('wtPaintListTSL',e=1,vis=typ)
    columnLayout('wtPaintBMainCL',e=1,vis=typ)

def sdd_showFilterLayout(typ):
    columnLayout('wtPTSkinCL',e=1,vis=typ)

def sdd_showDeformLayout(typ):
    columnLayout('wtPTDeformersCL',e=1,vis=typ)


def sdd_enableVertexLayout(typ):
    columnLayout('wtVertexMainCL',e=1,en=typ)
    textScrollList('wtVertexListTSL',e=1,en=typ)

def sdd_enablePaintLayout(typ):
    columnLayout('wtPaintTMainCL',e=1,en=typ)
    textScrollList('wtPaintListTSL',e=1,en=typ)
    columnLayout('wtPaintBMainCL',e=1,en=typ)

def sdd_enableVertexMenu(typ):
    itemList=popupMenu('wtInfoPM',q=1,ia=1)
    for i in itemList:
        menuItem(i,e=1,en=typ)

#=========== Mode =====================
def sdd_noneModeProc():
    sdd_changeMainIconLable('None')
    sdd_enableVertexLayout(0)
    sdd_enablePaintLayout(0)
    setToolTo('moveSuperContext')
    sdd_objectMode()
    sdd_deletePaintScriptJob()
    sdd_deleteVertexScriptJob()

def sdd_paintModeProc():
    sdd_changeMainIconLable('Paint')
    sdd_enableVertexLayout(0)
    sdd_enablePaintLayout(1)
    sdd_showPaintLayout(1)
    sdd_showVertexLayout(0)
    sdd_showFilterLayout(1)
    sdd_showDeformLayout(0)
    sdd_objectMode()

    if(modelEditor('modelPanel4',q=1,ex=1)):
        modelEditor('modelPanel4',e=1,da='smoothShaded')
    selectPriority(jp=2)

    typ=sdd_returnPaintType()
    if  (typ=='Skin'):
        ArtPaintSkinWeightsTool()
        sdd_paintListPopupMenuSwitch('Skin')
        if(skinList==[]):
            sdd_ToggleToolSettings()
        print 'SkinCluster'

    sdd_initPaintLayout()
    sdd_deleteVertexScriptJob()
    sdd_loadPaintScrollList()
    sdd_createPaintScriptJob()

def sdd_deformModeProc():
    sdd_changeMainIconLable('Dform')
    sdd_enableVertexLayout(0)
    sdd_enablePaintLayout(1)
    sdd_showPaintLayout(1)
    sdd_showVertexLayout(0)
    sdd_showFilterLayout(0)
    sdd_showDeformLayout(1)
    sdd_objectMode()
    typ=sdd_returnPaintType()
    if(typ=='Blend'):
        mm.eval('ArtPaintBlendShapeWeightsTool;')
        sdd_paintListPopupMenuSwitch('Blend')
        print 'BlendShape'
    if(typ=='Clust'):
        mm.eval('artAttrToolScript 4 "cluster";')
        sdd_paintListPopupMenuSwitch('Clust')
        print 'Cluster'
    if(typ=='Wire'):
        mm.eval('artAttrToolScript 4 "wire";')
        sdd_paintListPopupMenuSwitch('Wire')
        print 'Wire'

    sdd_initPaintLayout()
    sdd_deleteVertexScriptJob()
    sdd_loadPaintScrollList()


def sdd_vertexModeProc():
    sdd_changeMainIconLable('Vertex')
    sdd_enableVertexLayout(1)
    sdd_enablePaintLayout(0)
    sdd_showPaintLayout(0)
    sdd_showVertexLayout(1)
    if(currentCtx()!='selectSuperContext'):
        setToolTo('selectSuperContext')
    sdd_vertexMode()
    sdd_deletePaintScriptJob()
    sdd_createVertexScriptJob()
    undoInfo(swf=0)
    sdd_loadVertexInfo()
    undoInfo(swf=1)





def sdd_objectMode():
    selectMode(o=1)

    undoInfo(swf=0)
    sel=ls(sl=1,typ='joint')
    if(sel!=[]):
        select(sel,d=1)
    undoInfo(swf=1)



def sdd_vertexMode():
    selectMode(co=1)
    selectPriority(jp=1)
    selectType(jp=1,sp=0,rp=0,cv=1,pv=1,smp=1,lp=1,pr=1)
    #modelEditor(getPanel(wf=1),e=1,jointXray=1,da='wireframe')

#SetS
def sdd_paintSetMembershipProc():
    selI=textScrollList('wtPaintListTSL',q=1,si=1)
    if(selI==None):
        return
    mTyp=sdd_returnPaintType()
    if(mTyp=='Blend'):
        mm.eval('warning "Support only Cluster and Wire!"')
        return
    PaintSetMembershipTool()
    cluSet=listConnections(selI[0]+'.message')
    if(cluSet==None):
        return
    artSetPaintCtx(currentCtx(),e=1,stm=cluSet[0])

def sdd_addToScollListSets(typ):
    sel=ls(sl=1)
    selI=textScrollList('wtPaintListTSL',q=1,si=1)
    if(selI==None):
        return
    cluSet=listConnections(selI[0]+'.message')
    if(cluSet==None):
        return
    allVtx=sdd_getSelectObjVertex(sel)
    if(typ=='Add'):
        sets(allVtx,add=cluSet[0])
    if(typ=='Remove'):
        sets(allVtx,add=cluSet[0])
        for i in allVtx:
            if(sets(i,im=cluSet[0])):
                sets(i,rm=cluSet[0])
def sdd_getSelectObjVertex(sel):
    selVtx=filterExpand(sel,sm=[28,31,36,40,46])
    allVtx=[]
    if(selVtx!=None):
        allVtx=selVtx
    for i in sel:
        if (i.find('.')!=-1):
            continue
        objName=i.split('.')[0]
        shape=listRelatives(objName,s=1,f=1)
        if(shape==None):
            return
        supportList=['mesh','lattice','nurbsCurve','nurbsSurface','subdiv']
        sTyp=objectType(shape[0])
        if not(sTyp in supportList):
            return

        suf='.vtx[*]'
        if(sTyp in ['nurbsCurve','nurbsSurface']):
            suf='.smp[*]'
        if(sTyp=='subdiv'):
            suf='.smp[*]'
        if(sTyp=='lattice'):
            suf='.pt[*]'
        allVtx=allVtx+ls(objName+suf,fl=1)
    return allVtx


def sdd_addToSelectionSets():
    sel=ls(sl=1)
    sets(sel[:-1],add=sel[-1])

def sdd_createSelectionSets():
    global cntTList
    sel=ls(sl=1)
    cntTList=[]
    for i in sel:
        attrList=['tx','ty','tz','rx','ry','rz','sx','sy','sz']
        udList=listAttr(i,ud=1)
        if(udList!=None):
            attrList=attrList+udList

        aList=[]
        for a in attrList:
            if not(getAttr(i+'.'+a,l=1)):
                v=getAttr(i+'.'+a)
                aList.append([a,v])
        cntTList.append([i,aList])

#sort and filler
def sdd_sortList():
    sdd_loadPaintScrollList()
def sdd_filterZeroList():
    sdd_loadPaintScrollList()


#====Function====#
#Paint
def sdd_initPaintLayout():
    curCtx=currentCtx()
    paintCtx=sdd_returnPaintCtxfunction()
    paintCtx(curCtx,e=1,stP='solid')

    po=paintCtx(curCtx,q=1,sao=1)
    radioButton('wtPO%sRB'%po,e=1,sl=1)
    sdd_changePaintOperationType(po)

    val=paintCtx(curCtx,q=1,val=1)
    floatField('wtPaintValueFF',e=1,v=val)
    floatSlider('wtPaintValueFS',e=1,v=val)

    sdd_updatePaintCheckButton()

def sdd_returnPaintCtxfunction():
    typ=sdd_returnPaintType()
    if(typ=='skin'):
        paintCtx=artAttrSkinPaintCtx
    else:
        paintCtx=artAttrCtx
    return paintCtx

def sdd_returnPaintType():
    if(iconTextButton('wtMTPaintITB',q=1,iol=1)!=''):
        return 'Skin'
    elif(iconTextButton('wtDTClusterITB',q=1,iol=1)!=''):
        return 'Clust'
    elif(iconTextButton('wtDTBlendITB',q=1,iol=1)!=''):
        return 'Blend'
    elif(iconTextButton('wtDTWireITB',q=1,iol=1)!=''):
        return 'Wire'

#Change Paint Operation
def sdd_changePaintOperationType(typ):
    curCtx=currentCtx()
    paintCtx=sdd_returnPaintCtxfunction()
    paintCtx(curCtx,e=1,sao=typ)

    if(typ=='smooth'):
        return

    lList=['.02','.1','.25','.5','.75']
    if(typ=='additive'):
        lList=['.01','.02','.05','.1','.25']
    if(typ=='scale'):
        lList=['.5','.75','.95','.98','.99']

    rw=28
    bh=25
    button('wtPValueB2',e=1,h=bh,w=rw-1,l=lList[0],c='sdd_setPaintValue(%s)'%lList[0])
    button('wtPValueB3',e=1,h=bh,w=rw-1,l=lList[1],c='sdd_setPaintValue(%s)'%lList[1])
    button('wtPValueB4',e=1,h=bh,w=rw-1,l=lList[2],c='sdd_setPaintValue(%s)'%lList[2])
    button('wtPValueB5',e=1,h=bh,w=rw-1,l=lList[3],c='sdd_setPaintValue(%s)'%lList[3])
    button('wtPValueB6',e=1,h=bh,w=rw-1,l=lList[4],c='sdd_setPaintValue(%s)'%lList[4])
#Parint Value
def sdd_setPaintValue(value):
    floatSlider('wtPaintValueFS',e=1,v=value)
    floatField('wtPaintValueFF',e=1,v=value)
    sdd_changePaintCtxValue()

def sdd_changePaintCtxValue():
    value=floatField('wtPaintValueFF',q=1,v=1)
    curCtx=currentCtx()
    paintCtx=sdd_returnPaintCtxfunction()
    paintCtx(curCtx,e=1,val=value)


def sdd_adjustPaintValue(typ):
    value=floatField('wtPaintValueFF',q=1,v=1)
    if(typ=='+'):
        if(menuItem('wtPVAdjustASMI',q=1,rb=1)):
            value=max(min(1,value+0.05),0)
        else:
            value=max(min(1,value*1.5),0)
    if(typ=='-'):
        if menuItem('wtPVAdjustASMI',q=1,rb=1):
            value=min(max(0,value-0.05),1)
        else:
            value=min(max(0,value*0.5),1)

    floatSlider('wtPaintValueFS',e=1,v=value)
    floatField('wtPaintValueFF',e=1,v=value)
    sdd_setPaintValue(value)

def sdd_endsPaintValue():
    value=floatField('wtPaintValueFF',q=1,v=1)
    if(value>0):
        value=0
    else:
        value=1
    floatSlider('wtPaintValueFS',e=1,v=value)
    floatField('wtPaintValueFF',e=1,v=value)
    sdd_setPaintValue(value)

#Paint ScrollList
def sdd_loadPaintScrollList():
    sel=ls(sl=1)
    if(sel==[]):
        mm.eval('warning "Please select mesh!"')
        textScrollList('wtPaintListTSL',e=1,ra=1)
        return
    textScrollList('wtPaintListTSL',e=1,ra=1)
    typ=sdd_returnPaintType()
    if(typ=='Skin'):
        sdd_loadSkinInfoToList(sel)
    else:
        sdd_loadDeformersInfoToList(typ)

#Change Paint Select
def sdd_paintScrollListSelectChange():
    global paintOldSelClust
    global paintOldSelBlend
    global paintOldSelWire
    sel=textScrollList('wtPaintListTSL',q=1,si=1)
    if(sel==None):
        return

    ctxList=['artAttrSkinContext','artAttrBlendShapeContext','artAttrContext']
    curCtx=currentCtx()
    if not(curCtx in ctxList):
        sdd_selectPaintObject(sel)
        return

    typ=sdd_returnPaintType()
    if  (typ=='Skin'):
        mm.eval('setSmoothSkinInfluence %s'%sel[0].split(' (')[0])
    elif(typ=='Clust'):
        mm.eval('artSetToolAndSelectAttr( "artAttrCtx","cluster.%s.weights");'%sel[0])
        sdd_hiliteObjectByShape(sel[0])
        paintOldSelClust=sel[0]
    elif(typ=='Blend'):
        spList=sel[0].split('.')
        if(len(spList)>1):
            mm.eval('artSetToolAndSelectAttr( "artAttrCtx","blendShape.%s");'%sel[0])
            mm.eval('artAttrInitPaintableAttr;')
            textScrollList('wtPaintListTSL',e=1,ra=1)
            sdd_loadBlendShapeTargetsToList(spList[0])
            sdd_deformersListAutoSelectCurrent(typ)
        else:
            sdd_changeBlendShapeTargetIndex(sel[0])
            paintOldSelBlend=sel[0]
    elif(typ=='Wire'):
        artAttrCtx(curCtx,e=1,pas='cluster.%s.weights'%sel[0])
        paintOldSelWire=sel[0]


def sdd_changeBlendShapeTargetIndex(bsTatget):
    if not(textScrollList('blendShapeTargetList',q=1,ex=1)):
        return
    allI=textScrollList('blendShapeTargetList',q=1,ai=1)
    for i in allI:
        if(i==bsTatget):
            textScrollList('blendShapeTargetList',e=1,si=i)
    mm.eval('global string $artBlendShapeCurrentTarget;$artBlendShapeCurrentTarget="%s"'%bsTatget)
    curCtx=currentCtx()
    blendShapeAttr=artAttrCtx(curCtx,q=1,asl=1)
    artAttrCtx(curCtx,e=1,pas=blendShapeAttr)
def sdd_hiliteObjectByShape(Node):
    tranform=listConnections(Node+'.matrix')[0]
    hilite(tranform,r=1)


#Load Info To Scroll List
def sdd_loadSkinInfoToList(sel):
    global skinList

    skinNode=sdd_findRelatedSkinCluster(sel[0])
    if(skinNode==''):
        return

    skinList=[]
    jntList=skinCluster(sel[0],q=1,inf=1)
    if(menuItem('wtListZeroMI',q=1,cb=1)):
        jntList=skinCluster(sel[0],q=1,wi=1)
    if(menuItem('wtListSortAMI',q=1,rb=1)):
        jntList.sort()
    if(menuItem('wtListSortLMI',q=1,rb=1)):
        jntList=sdd_sortPaintListByLock(jntList)

    for i in jntList:
        if(getAttr(i+'.liw')):
            i=i+' (Hold)'
        textScrollList('wtPaintListTSL',e=1,a=i)
        skinList.append(i)

    sdd_skinListAutoSelectCurrent()
    matchTx=sdd_returnMatchStr()
    if(matchTx!=''):
        sdd_skinListMatchString()

def sdd_skinListAutoSelectCurrent():
    allI=textScrollList('wtPaintListTSL',q=1,ai=1)
    selI=textScrollList('wtPaintListTSL',q=1,si=1)
    if(allI==None):
        return
    curCtx=currentCtx()
    if(curCtx!='artAttrSkinContext'):
        return
    curJnt=artAttrSkinPaintCtx(curCtx,q=1,inf=1)
    if(curJnt==''):
        textScrollList('wtPaintListTSL',e=1,sii=1)
        mm.eval('setSmoothSkinInfluence %s'%allI[0].split(' (')[0])
        return
    lock=getAttr(curJnt+'.liw')
    if(lock):
        curJnt=curJnt+' (Hold)'
    if(selI==curJnt):
        return
    textScrollList('wtPaintListTSL',e=1,da=1)
    if(curJnt in allI):
        sdd_changeWindowSize('-')
        textScrollList('wtPaintListTSL',e=1,si=curJnt)
        sdd_changeWindowSize('+')

def sdd_sortPaintListByLock(jntList):
    holdList=[]
    noHoldList=[]
    for i in jntList:
        if(getAttr(i+'.liw')):
            holdList.append(i)
            continue
        noHoldList.append(i)
    return noHoldList+holdList

def sdd_loadDeformersInfoToList(typ):
    curCtx=currentCtx()
    attrStr=artAttrCtx(curCtx,q=1,oaa=1)
    attrList=attrStr.split(' ')
    attrList.sort()
    for i in attrList:
        tmp=i.split('.')
        if(tmp[0]=='cluster' and typ=='Clust'):
            textScrollList('wtPaintListTSL',e=1,a=tmp[1])
        if(tmp[0]=='wire' and typ=='Wire'):
            textScrollList('wtPaintListTSL',e=1,a=tmp[1])

        if(tmp[0]=='blendShape' and typ=='Blend'):
            if(tmp[2]!='baseWeights'):
                textScrollList('wtPaintListTSL',e=1,a=tmp[1]+'.'+tmp[2])
    sdd_deformersListAutoSelectCurrent(typ)

def sdd_deformersListAutoSelectCurrent(typ):
    global paintOldSelClust
    global paintOldSelBlend
    global paintOldSelWire
    allI=textScrollList('wtPaintListTSL',q=1,ai=1)
    if(allI!=None):
        for i in [paintOldSelClust,paintOldSelBlend,paintOldSelWire]:
            if(i in allI):
                textScrollList('wtPaintListTSL',e=1,sii=allI.index(i)+1)
                sdd_paintScrollListSelectChange()
                break
        if(textScrollList('wtPaintListTSL',q=1,si=1)==None and typ!='Blend'):
            textScrollList('wtPaintListTSL',e=1,sii=1)
            sdd_paintScrollListSelectChange()
    else:
        setToolTo('selectSuperContext')

def sdd_loadBlendShapeTargetsToList(bsNode):
    aliasList=listConnections(bsNode+'.it')
    if(aliasList==[]):
        return
    aliasList.sort()
    for i in aliasList:
        textScrollList('wtPaintListTSL',e=1,a=i)


#Lock Unlock Paint ScrollList
def sdd_lockUnlockInfoScrollList():
    global skinList
    idx=sdd_returnCurrentScrollListId()
    selI=textScrollList(idx,q=1,sii=1)
    sel=textScrollList(idx,q=1,si=1)
    for i in range(len(sel)):
        tmp=sel[i].split(' (')[0]
        jnt=tmp.split('|')[-1]
        setAttr(jnt+'.liw',l=0)
        if(getAttr(jnt+'.liw')):
            setAttr(jnt+'.liw',0)
        else:
            setAttr(jnt+'.liw',1)
            tmp=tmp+' (Hold)'
        if(iconTextButton('wtMTVertexITB',q=1,iol=1)==''):
            skinList[skinList.index(sel[i])]=tmp
        textScrollList(idx,e=1,ap=[selI[i],tmp])
        textScrollList(idx,e=1,sii=selI[i])
        textScrollList(idx,e=1,rii=selI[i]+1)
    textScrollList(idx,e=1,sii=selI)
    sdd_vertexInitSlider()

def sdd_lockUnlockAllInfoScrollList(typ):
    global skinList
    sel=ls(sl=1)
    if(sel==[]):
        return
    if(skinList==[]):
        sdd_loadSkinInfoToList([sel[0].split('.')[0]])
    clusterName=sdd_findRelatedSkinCluster(sel[0].split('.')[0])
    if(clusterName==''):
        return
    idx=sdd_returnCurrentScrollListId()
    selI=textScrollList(idx,q=1,sii=1)
    allI=textScrollList(idx,q=1,ai=1)
    textScrollList(idx,e=1,da=1)

    for i in range(len(allI)):
        tmp=allI[i].split(' (')[0]
        jnt=tmp.split('|')[-1]
        if(typ):
            tmp=tmp+' (Hold)'
        textScrollList(idx,e=1,ap=[i+1,tmp])
        textScrollList(idx,e=1,sii=selI[0])
        if(i+2==selI[0]):
            textScrollList(idx,e=1,sii=selI[0]+1)
        textScrollList(idx,e=1,rii=i+2)
        skinList[i]=tmp

    allJnt=skinCluster(clusterName,q=1,inf=1)
    for i in allJnt:
        setAttr(i+'.liw',l=0)
        if not(typ):
            setAttr(i+'.liw',0)
        else:
            setAttr(i+'.liw',1)
    if(selI!=None):
        selI=textScrollList(idx,e=1,sii=selI)
    if(idx=='wtVertexListTSL'):
        sdd_vertexInitSlider()

def sdd_returnCurrentScrollListId():
    if(iconTextButton('wtMTVertexITB',q=1,iol=1)==''):
        return 'wtPaintListTSL'
    return 'wtVertexListTSL'

#List Select Object
def sdd_selectPaintListObject():
    sel=textScrollList('wtPaintListTSL',q=1,si=1)
    setToolTo('selectSuperContext')
    sdd_selectPaintObject(sel)

#Match String
def sdd_skinListMatchString():
    global skinList
    matchTx=sdd_returnMatchStr()
    if(matchTx==''):
        sdd_loadPaintScrollList()
        return
    matchList=[]
    textScrollList('wtPaintListTSL',e=1,ra=1)
    for i in skinList:
        ret=sdd_matchStrListOr(matchTx,i)
        if not(menuItem('wtPaintMatchInverseMI',q=1,cb=1)):
            if(ret):
                matchList.append(i)
        else:
            if not(ret):
                matchList.append(i)
    for i in matchList:
        textScrollList('wtPaintListTSL',e=1,a=i)
    iconTextButton('wtSkinMatchModeITB',e=1,i1='filtersOn.xpm')
    sdd_skinListAutoSelectCurrent()
def sdd_returnMatchStr():
    matchTx=textField('wtPaintMatchTF',q=1,tx=1)
    matchTx=matchTx.strip(' ')
    matchTx=matchTx.strip('|')
    matchTx=matchTx.strip('*')
    return matchTx
def sdd_matchStrListOr(matchTx,Str):
    mlist=matchTx.split('|')
    for i in mlist:
        if(i==''):
            continue
        if(sdd_matchStrListAnd(i,Str)):
            return 1
    return 0
def sdd_matchStrListAnd(matchTx,Str):
    mlist=matchTx.split('*')
    for i in mlist:
        i=i.strip(' ')
        if(i==''):
            continue
        if(Str.find(i)==-1):
            return 0
    return 1
def sdd_sendToFilter():
    sItem=textScrollList('wtPaintListTSL',q=1,si=1)
    if(sItem==None):
        return
    matchTx=''
    for i in sItem:
        matchTx=matchTx+i.split('(')[0]+'|'
    matchTx=matchTx.strip('|')
    textField('wtPaintMatchTF',e=1,tx=matchTx)
    iconTextButton('wtSkinMatchModeITB',e=1,i1='filtersOn.xpm')
    sdd_skinListMatchString()



def sdd_checkPaintCtxFlying():
    curCtx=currentCtx()
    paintCtx=sdd_returnPaintCtxfunction()
    cp=paintCtx(curCtx,q=1,colorrangeupper=1)
    if(cp<1):
        paintCtx(curCtx,e=1,colorrangeupper=1)
    else:
        paintCtx(curCtx,e=1,colorrangeupper=0.001)
    sdd_updatePaintCheckButton()

def sdd_updatePaintCheckButton():
    curCtx=currentCtx()
    paintCtx=sdd_returnPaintCtxfunction()
    cp=paintCtx(curCtx,q=1,colorrangeupper=1)
    bw=197
    if(int(about(v=1)[0:4])>2009):
        bw=200
    if(cp<1):
        button('wtPaintCheckB',e=1,w=bw,l='Exit',bgc=(1,0,0))
    else:
        button('wtPaintCheckB',e=1,w=bw,l='Check flying',bgc=(0,1,0))
    button('wtPaintCheckB',e=1,en=0)
    button('wtPaintCheckB',e=1,en=1)

def sdd_floodPaintCtx():
    curCtx=currentCtx()
    paintCtx=sdd_returnPaintCtxfunction()
    paintCtx(curCtx,e=1,clear=1)

def sdd_selectPaintObject(sel):
    select(cl=1)
    for i in sel:
        select(i.split(' (')[0],add=1)


def sdd_smoothPaintSkinList():
    selI=textScrollList('wtPaintListTSL',q=1,sii=1)
    allList=textScrollList('wtPaintListTSL',q=1,ai=1)
    sdd_changePaintOperationType("smooth")
    radioButton('wtPOsmoothRB',e=1,sl=1)
    for i in allList:
        item=i.split('(')[0]
        mm.eval('setSmoothSkinInfluence %s'%item)
        sdd_floodPaintCtx()
        refresh(cv=1)
    textScrollList('wtPaintListTSL',e=1,sii=selI)

#Vertex
def sdd_vertexEnable(enb):
    columnLayout('wtVertexValueCL',e=1,en=enb) 
    floatSliderGrp('wtVtxValue',e=1,en=enb)
    # floatSlider('wtVtxRelaxFS',e=1,en=enb)
    button('wtVtxSmoothB',e=1,en=0)
    # floatSlider('wtVtxRelaxSizeFS',e=1,en=enb)
#Load Info To list
def sdd_loadVertexInfo():
    undoInfo(swf=0)

    global curVtxJnt
    global allJntList
    global oldSelVtx
    global skinName
    textScrollList('wtVertexListTSL',e=1,ra=1)
    sdd_enableVertexMenu(0)

    sel=ls(sl=1,fl=1)
    if(sel==[]):
        iconTextButton('wtSelJntNameT',e=1,l='Please Select Vertex !')
        sdd_vertexEnable(0)
        return
    selJnt=filterExpand(sel,sm=[50])
    if(selJnt!=None):
        select(selJnt,d=1)
        curVtxJnt=selJnt[0].split('.')[0]

    #selJnt=filterExpand(sel,sm=[50])

    selVtx=sel

    meshName=selVtx[0].split('.')[0]
    skinName=sdd_findRelatedSkinCluster(meshName)


    if(skinName==''):
        sdd_vertexEnable(0)
        return


    allJntList=skinCluster(skinName,q=1,inf=1)
    infJnt=sdd_skinPercentQueryTransform(skinName,selVtx[0])
    if(iconTextButton('wtVtxShowMod',q=1,l=1)=='All'):
        jntList=infJnt
    else:
        jntList=allJntList

    if(curVtxJnt=='') or not(curVtxJnt in allJntList):
        curVtxJnt=infJnt[0]


    sItem=''
    for i in jntList:
        val=skinPercent(skinName,selVtx[0],q=1,t=i)
        tmpStr='%s | %s'%('%.3f'%val,i)
        if(getAttr(i+'.liw')):
            tmpStr=tmpStr+' (Hold)'
        textScrollList('wtVertexListTSL',e=1,a=tmpStr)
        if(curVtxJnt==i):
            sItem=tmpStr

    if(sItem!=''):
        textScrollList('wtVertexListTSL',e=1,si=sItem)

    meshShape=listRelatives(meshName,s=1)[0]
    isMesh=objectType(meshShape)=='mesh'
    typ=iconTextButton('wtSelJntNameT',q=1,ann=1)

        

    sdd_vertexInitSlider()
    sdd_vertexEnable(1)
    button('wtVtxSmoothB',e=1,en=0)
    oldSelVtx=selVtx


    info='%s - %s'%(len(selVtx),curVtxJnt)
    iconTextButton('wtSelJntNameT',e=1,l=info)
    sdd_enableVertexMenu(1)
    sdd_vertexHilite()
    undoInfo(swf=1)

def sdd_vertexInitSlider():
    global curVtxJnt

    sel=textScrollList('wtVertexListTSL',q=1,si=1)
    allI=textScrollList('wtVertexListTSL',q=1,ai=1)
    if(allI==None):
        return
    if(sel==None):
        floatSliderGrp('wtVtxValue',e=1,v=0)
    else:
        floatSliderGrp('wtVtxValue',e=1,v=float(sel[0].split('|')[0]))
    if(getAttr(curVtxJnt+'.liw')):
        floatSliderGrp('wtVtxValue',e=1,en=0)
    else:
        floatSliderGrp('wtVtxValue',e=1,en=1)

def sdd_vertexHilite():
    global curVtxJnt
    jntHL=ls(hl=1,typ='joint')
    if(jntHL!=[]):
        hilite(jntHL,u=1)
    if(curVtxJnt!=''):
        if(objExists(curVtxJnt)):
            hilite(curVtxJnt)

def sdd_vertexScrollListSelectChange():
    global curVtxJnt
    sel=textScrollList('wtVertexListTSL',q=1,si=1)[0]
    curVtxJnt=sel.split('|')[1].split('(Hold)')[0]
    curVtxJnt=curVtxJnt.strip(' ')
    info=iconTextButton('wtSelJntNameT',q=1,l=1)
    newInfo=info.split(' - ')[0]+' - '+curVtxJnt
    iconTextButton('wtSelJntNameT',e=1,l=newInfo)
    sdd_vertexInitSlider()
    sdd_vertexHilite()



def sdd_vertexInfoShowMode():
    if(iconTextButton('wtVtxShowMod',q=1,l=1)=='All'):
        iconTextButton('wtVtxShowMod',e=1,w=30,l='<<')
    else:
        iconTextButton('wtVtxShowMod',e=1,w=30,l='All')
    undoInfo(swf=0)
    sdd_loadVertexInfo()
    undoInfo(swf=1)


def sdd_vertexSliderChange():
    value=floatSliderGrp('wtVtxValue',q=1,v=1)
    sdd_vertexSetAbsWeight(value)



#Change Weight

def sdd_vertexChangeWeight(typ,value):
    global curVtxJnt
    global skinName
    if(curVtxJnt==''):
        return

    sel=ls(sl=1)
    selVtx=filterExpand(sel,sm=[28,31,36,40,46])

    stepValue=floatField('wtVtxAddValueFF',q=1,v=1)
    nw=getAttr('skinCluster1.nw')
    if(len(selVtx)>200):
        progressBar('wtMainPrograssPB',e=1,vis=1)

    progressBar('wtMainPrograssPB',e=1,bp=1,ii=1,max=len(selVtx))
    sdd_refreshWindow()
    try:
        for i in selVtx:
            value=skinPercent(skinName,i,q=1,t=curVtxJnt)
            if typ=='+':
                value=value+stepValue
            if typ=='-':
                value=value-stepValue
            if typ=='*':
                value=value*(1+stepValue)
            if typ=='/':
                value=value*(1-stepValue)
            value=max(0,value)
            if(nw<=1):
                value=min(1,value)
            skinPercent(skinName,i,tv=[curVtxJnt,value])

            progressBar('wtMainPrograssPB',e=1,s=1)
    except:
        mm.eval('warning "Save Weight Error!"')
    finally:
        progressBar('wtMainPrograssPB',e=1,ep=1)
        progressBar('wtMainPrograssPB',e=1,vis=0)

    undoInfo(swf=0)
    sdd_loadVertexInfo()
    undoInfo(swf=1)

def sdd_vertexSetAbsWeight(value):
    global curVtxJnt
    global skinName
    skinPercent(skinName,ls(sl=1),tv=[curVtxJnt,value])
    undoInfo(swf=0)
    sdd_loadVertexInfo()
    undoInfo(swf=1)

#Copy And Paste
def sdd_vertexCopyWeight():
    global copyVtx
    global curVtxJnt
    global skinName

    sel=ls(sl=1)
    selVtx=filterExpand(sel,sm=[28,31,36,40,46])

    copyValueList=skinPercent(skinName,selVtx[0],ib=0.0000001,q=1,v=1)
    copyTransList=sdd_skinPercentQueryTransform(skinName,selVtx[0])

    iconTextButton('wtSelJntNameT',e=1,l='Copy %s'%(selVtx[0].split('.')[-1]))

    tvList=[]
    for i in range(len(copyValueList)):
        tvList.append([copyTransList[i],copyValueList[i]])

    copyVtx=tvList

        
        
def sdd_vertexPasteWeight():
    global copyVtx
    if(copyVtx==[]):
        return

    sel=ls(sl=1)
    selVtx=filterExpand(sel,sm=[28,31,36,40,46])
    skinPercent(skinName,selVtx,tv=copyVtx)
    iconTextButton('wtSelJntNameT',e=1,l='Paste Success.')

    undoInfo(swf=0)
    sdd_loadVertexInfo()
    undoInfo(swf=1)

#Paint <> Vertex
def sdd_paintVertexThis():
    global curVtxJnt
    curCtx=currentCtx()
    curVtxJnt=artAttrSkinPaintCtx(curCtx,q=1,inf=1)
    sdd_vertexModeProc()

def sdd_vertexPaintThis():
    global curVtxJnt
    sdd_noneModeProc()
    ArtPaintSkinWeightsTool()
    mm.eval('setSmoothSkinInfluence %s'%curVtxJnt)
    sdd_paintModeProc()

def sdd_vertexClosetJoint():
    global allJntList
    global curVtxJnt
    sel=ls(sl=1)
    if(sel==[]):
        return
    selVtx=filterExpand(sel,sm=[31])
    if(selVtx==None):
        return

    curP=OpenMaya.MPoint()
    jntP=OpenMaya.MPoint()

    curPos=xform(selVtx[0],q=1,ws=1,t=1)
    curP.x=curPos[0]
    curP.y=curPos[1]
    curP.z=curPos[2]

    closteJnt=''
    tmpdis=0
    for i in allJntList:
        pos=xform(i,q=1,ws=1,t=1)
        jntP.x=pos[0]
        jntP.y=pos[1]
        jntP.z=pos[2]
        dis=jntP.distanceTo(curP)
        if(tmpdis==0 or tmpdis>dis):
            tmpdis=dis
            closteJnt=i
    closteJnt
    curVtxJnt=closteJnt
    sdd_vertexModeProc()     


#Vertex Select
def sdd_selectElemVtx():
    mm.eval('polyConvertToShell;')

def sdd_selectLastVtx():
    global oldSelVtx
    select(cl=1)
    for i in oldSelVtx:
        if(objExists(i)):
            select(i,add=1)

def sdd_selectMirrorVtx():
    sel=ls(sl=1)
    if(sel==[]):
        return
    selVtx=filterExpand(sel,sm=[31])
    if(selVtx==None):
        print "Olny spourt mesh vertex!"
        return 
    sdd_getMehsMirrorVertex()


#Save Or Load Weight
def sdd_saveLoadDialog(mod):
    path=fileDialog(m=mod,dm='*.sdd')
    if(path==''):
        return path
    fieldName=(path.split('/'))[-1]
    if(fieldName.find('.')==-1):
        path=path+'.sdd'
    return path



#Save weight
def sdd_saveWeight():
    sel=ls(sl=1,fl=1)
    if(sel==[]):
        return

    selVtx=filterExpand(sel,sm=[28,31,36,40,46])
    if(selVtx==None):
        selVtx=sdd_getMeshAllVertex(sel[0],[])
        if(selVtx==[]):
            return
    objName=selVtx[0].split('.')[0]
    clusterName=sdd_findRelatedSkinCluster(objName)
    if(clusterName==''):
        return

    #save path
    path=sdd_saveLoadDialog(1)
    if(path==''):
        progressBar('wtMainPrograssPB',e=1,vis=0)
        return

    #time
    t1=datetime.datetime.now()
    progressBar('wtMainPrograssPB',e=1,bp=1,vis=1,ii=1,max=len(selVtx))
    sdd_refreshWindow()
    try:
        f=open(path,'w')
        for i in selVtx:
            progressBar('wtMainPrograssPB',e=1,s=1)
            ValueList=skinPercent(clusterName,i,ib=0.0000001,q=1,v=1)
            TransList=sdd_skinPercentQueryTransform(clusterName,i)
            tvList=[]
            for a in range(len(ValueList)):
                tvList.append([TransList[a],ValueList[a]])

            wtStr='%s--%s\r\n'%(i.split('.')[-1],tvList)
            f.write(wtStr)
    except:
        mm.eval('warning "Save Weight Error!"')  
    finally:
        progressBar('wtMainPrograssPB',e=1,ep=1)
        progressBar('wtMainPrograssPB',e=1,vis=0)
        f.close()
    t2=datetime.datetime.now()
    sys.stderr.write('Used time is : %s'%(t2-t1))




def sdd_getMeshAllVertex(mesh,idxList):
    selVtx=[]
    selShape=listRelatives(mesh,s=1,f=1)
    if(selShape==None):
        return
    typ=objectType(selShape[0])
    if(typ=='mesh'):
        suf='.vtx'
    elif(typ=='nurbsCurve' or typ=='nurbsSurface' ):
        suf='.cv'
    elif(typ=='subdiv'):
        suf='.smp'
    elif(typ=='lattice'):
        suf='.pt'
    else:
        return selVtx

    if(idxList==[]):
        selVtx=ls(mesh+suf+'[*]',fl=1)
    else:
        for i in idxList:
            vtx=mesh+suf+'[%s]'%i
            if(objExists(vtx)):
                selVtx.append(vtx)

    return selVtx

#load weight
def sdd_loadWeight():
    sel=ls(sl=1,fl=1)
    if(len(sel)==[]):
        mm.eval('warning "Please selcte mesh!"')
        return

    objName=sel[0].split('.')[0]
    clusterName=sdd_findRelatedSkinCluster(objName)
    if(clusterName==''):
        return

    path=sdd_saveLoadDialog(0)
    if(path==''):
        progressBar('wtMainPrograssPB',e=1,vis=0)
        return

    #time
    allLine=[]
    try:
        f=open(path,'r')
        line=f.readline()
        while(line!=''):
            allLine.append(line)
            line=f.readline()
    finally:
        f.close()

    t1=datetime.datetime.now()
    progressBar('wtMainPrograssPB',e=1,bp=1,vis=1,ii=1,max=len(allLine))
    sdd_refreshWindow()

    try:
        for i in allLine:
            vtx=i.split('--')[0]
            vtx=vtx.strip()
            tvList=i.split('--')[-1]
            tvList=tvList.strip()
            exec('skinPercent("%s","%s",tv=%s)'%(clusterName,objName+'.'+vtx,tvList))
            progressBar('wtMainPrograssPB',e=1,s=1)
    except:
        mm.eval('warning "Load Weight Error!"')  
    finally:
        progressBar('wtMainPrograssPB',e=1,ep=1)
        progressBar('wtMainPrograssPB',e=1,vis=0)
    t2=datetime.datetime.now()
    sys.stderr.write('Used time is : %s'%(t2-t1))


def sdd_vertexModeQuit():
    sdd_noneModeProc()


############
def sdd_getMehsMirrorVertex():
    global skinName
    #get argument
    sList=OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(sList)
    sItList=OpenMaya.MItSelectionList(sList)
    dagPath=OpenMaya.MDagPath()
    mObj = OpenMaya.MObject()
    sItList.getDagPath(dagPath,mObj)
    mItVtx=OpenMaya.MItGeometry(dagPath,mObj)
    dpObj = OpenMaya.MObject()
    sList.getDependNode(0,dpObj)
    mfnMesh=OpenMaya.MFnMesh(dpObj)
    mfnMeshPlug=mfnMesh.findPlug("inMesh")
    #MFnSkincluster

    skinList=OpenMaya.MSelectionList()
    skinList.add(skinName)
    skinNode=OpenMaya.MObject()
    skinList.getDependNode(0,skinNode)


    mFnSkinCluster=OpenMayaAnim.MFnSkinCluster(skinNode)
    origList=OpenMaya.MObjectArray()
    mFnSkinCluster.getInputGeometry(origList)
    mfnMesh=OpenMaya.MFnMesh(origList[0])

    basePList=OpenMaya.MPointArray()
    mfnMesh.getPoints(basePList)
    clostP=OpenMaya.MPoint()
    mirP=OpenMaya.MPoint()
    space = OpenMaya.MSpace.kObject
    util = OpenMaya.MScriptUtil()
    util.createFromInt(0)
    idPointer = util.asIntPtr()
    mirX=-1
    mirY=1
    mirZ=1

    retList=[]
    for i in range(mItVtx.count()):
        curPos=mItVtx.position()
        mirP.x=curPos.x*mirX
        mirP.y=curPos.y*mirY
        mirP.z=curPos.z*mirZ
        mfnMesh.getClosestPoint(mirP,clostP,space,idPointer)
        idx = OpenMaya.MScriptUtil(idPointer).asInt()
        nearestList=OpenMaya.MIntArray()
        mfnMesh.getPolygonVertices(idx,nearestList)
        tmpdis=None
        retIdx=None
        for d in nearestList:
            dis=basePList[d].distanceTo(mirP)
            if(tmpdis==None or dis<tmpdis):
                tmpdis=dis
                retIdx=d
        retList.append(retIdx)
        mItVtx.next()

    mItAllVtx=OpenMaya.MItMeshVertex(dagPath) 
    for i in retList:
        mItAllVtx.setIndex(i,idPointer)
        sList.add(dagPath,mItAllVtx.currentItem())
    OpenMaya.MGlobal.setActiveSelectionList(sList)


#Call Mel
def sdd_findRelatedSkinCluster(obj):
    return mm.eval('findRelatedSkinCluster("%s")'%obj)

def sdd_skinPercentQueryTransform(skinName,selVtx):
    return mm.eval('skinPercent -ib 0.0000001 -q -t %s %s'%(skinName,selVtx))


#Global

if not('skinList' in dir()):
    skinName=''
    skinList=[]
    cntTList=[]
    curVtxJnt=''
    copyVtx=[]
    paintOldSelClust=''
    paintOldSelBlend=''
    paintOldSelWire=''
    allJntList=[]
    oldSelVtx=[]




def sdd_deletePaintScriptJob():
    if(text('wtPaintScriptJobS',q=1,ex=1)):
        deleteUI('wtPaintScriptJobS',ctl=1)

def sdd_createPaintScriptJob():
    if(text('wtPaintScriptJobS',q=1,ex=1)):
        return
    text('wtPaintScriptJobS',p='wtMainTypeCL',w=1,vis=0)
    scriptJob(e=['RecentCommandChanged','sdd_skinListAutoSelectCurrent()'],p='wtPaintScriptJobS')


def sdd_deleteVertexScriptJob():
    if(text('wtVertexScriptJobS',q=1,ex=1)):
        deleteUI('wtVertexScriptJobS',ctl=1)

def sdd_createVertexScriptJob():
    if(text('wtVertexScriptJobS',q=1,ex=1)):
        return
    text('wtVertexScriptJobS',p='wtMainTypeCL',w=1,vis=0)
    scriptJob(e=['Undo','undoInfo(swf=0);sdd_loadVertexInfo();undoInfo(swf=1);'],p='wtVertexScriptJobS')
    scriptJob(e=['SelectionChanged','undoInfo(swf=0);sdd_loadVertexInfo();undoInfo(swf=1);'],p='wtVertexScriptJobS')
    scriptJob(e=['ToolChanged','sdd_vertexModeQuit()'],p='wtVertexScriptJobS')
    scriptJob(e=['SelectModeChanged','sdd_vertexModeQuit()'],p='wtVertexScriptJobS')


if __name__=='__main__':
    sdd_weightTools()
