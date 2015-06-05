#for i in range(0,10):
#    print "a"
import maya.cmds as mc

def RH_Split():
    #Create a variable for the window name
    winName='Split'
    winTitle='Split_Joint!'
    #Delete the window if it exists
    if mc.window(winName, exists=True):
        mc.deleteUI(winName, window=True)
    #Build the main window
    mc.window(winName, title=winTitle, sizeable=True)
    #text field
    mc.intFieldGrp('RH_R_NameTFG',numberOfFields=1,label='Split_Joint_Num:', value1=0)
    #mc.intField('RH_R_NameTFG',label='Split_Joint_Num:',value=0 )
    mc.columnLayout(adjustableColumn=True)
    mc.button(label='Jawoll', command='Jawoll()')
    mc.columnLayout(adjustableColumn=True)
    mc.showWindow(winName)
    
def Jawoll():
    #get info
    num_jnt=mc.intFieldGrp('RH_R_NameTFG',q=True,v=True)
    a1=mc.ls(sl=1)
    a2=mc.listRelatives(a1,c=1)
    b1=mc.xform(a1,q=1,ws=1,t=1)
    b2=mc.xform(a2,q=1,ws=1,t=1)
    
    #mc.parent(a2,w=1)
    
    for i in range(num_jnt):
        print 'a'
    print type(num_jnt),a1,a2,b1,b2
 
RH_Split()    
