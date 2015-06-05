
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
    mc.button(label='Achtung', command='Achtung()')
    mc.columnLayout(adjustableColumn=True)
    mc.showWindow(winName)
    
def Achtung():
    #get info
    num_jnt=mc.intFieldGrp('RH_R_NameTFG',q=True,v=True)
    a1=mc.ls(sl=1)
    a2=mc.listRelatives(a1,c=1)
    b1=mc.xform(a1,q=1,ws=1,t=1)
    b2=mc.xform(a2,q=1,ws=1,t=1)
    #unparent
    mc.parent(a2,w=1)
    
    for i in range(0,num_jnt[0]):
       mc.select(a1,r=1) 
       b3=[(b1[0] - b2[0])*(i + 1)/(num_jnt[0] + 1) + b2[0],
       (b1[1] - b2[1])*(i + 1)/(num_jnt[0] + 1) + b2[1],
       (b1[2] - b2[2])*(i + 1)/(num_jnt[0] + 1) + b2[2]]
       radius = mc.getAttr(a1[0] + '.radius')
       mc.joint(rad = radius,p=(b3[0],b3[1],b3[2]),n=a1[0]+"_insert_"+str(num_jnt[0]-i))
       if i == 0:
           mc.parent(a2[0],a1[0]+"_insert_"+str(num_jnt[0]-i))
       else :    
           mc.parent(a1[0]+"_insert_"+str(num_jnt[0]-i+1),a1[0]+"_insert_"+str(num_jnt[0]-i))
           
RH_Split()    
