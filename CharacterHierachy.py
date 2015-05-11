#Title: CharacterHierachy.py
#Author: Ryugasaki Hu
#Created: May 11, 2015
#Last Update: May 11, 2015 
#Version: 1
#Description:This is a character group set,the setting hierachy 
            #come from Puppeteer Lounge rig workshop2
            #I decide to use this hierachy to my own character plugin script
            #this will be quiet a long ride when it start now

import maya.cmds as cmds

def GTA():
    #Create a variable for the window name
    winName = 'blend'
    winTitle = 'Group Them All!!!'
    #Delete the window if it exists
    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName, window=True)
    #Build the main window
    cmds.window(winName, title=winTitle, sizeable=True)
    cmds.textFieldButtonGrp('character',label='Character Name:', text='',buttonLabel='GTA',bc = 'Create_Character_Main_Group()')
    cmds.columnLayout(adjustableColumn=True)    
    #Show the window
    cmds.showWindow(winName)
    cmds.window(winName, edit=True, width=378, height=210)
    
def Create_Character_Main_Group():
    #get value
    CName = cmds.textFieldButtonGrp('character',q=True,tx=True)
    All = cmds.group(em=True, name = CName + '01_All')
    TRS = cmds.group(em= True,parent = All,name=CName + '01_TRS')
    GEO = cmds.group(em=True, parent = TRS,name=CName + '01_GEO')
    PP = cmds.group(em=True, parent = TRS,name=CName + '01_PP')
    XTR = cmds.group(em=True, parent = TRS,name=CName + '01_XTR')
    SKL = cmds.group(em=True, parent = PP,name=CName + '01_SKL')
    CC = cmds.group(em=True, parent = PP,name=CName + '01_CC')
    IK = cmds.group(em=True, parent = PP,name=CName + '01_IK')
    LOC = cmds.group(em=True, parent = PP,name=CName + '01_LOC')

GTA()    
