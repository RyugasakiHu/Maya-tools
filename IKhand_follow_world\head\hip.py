import maya.cmds as mc
#follow head
HeadT = mc.xform('charlie01_l_arm01_ikcc_off',q = 1,ws = 1,t = 1)
HeadRo = mc.xform('charlie01_l_arm01_ikcc_off',q = 1,ws = 1,ro = 1)

mc.setAttr('charlie01_l_arm01_ikcc.follow',0)
mc.setAttr('charlie01_l_arm01_ikcc_off_parentConstraint1.charlie01_c_pelvis_ccW0',0)
mc.setAttr('charlie01_l_arm01_ikcc_off_parentConstraint1.charlie01_c_headMaster01_ccW1',1)

mc.xform('charlie01_l_arm01_ikcc_off' , ws = 1,t = [HeadT[0],HeadT[1],HeadT[2]])
mc.xform('charlie01_l_arm01_ikcc_off' , ws = 1,ro = [HeadRo[0],HeadRo[1],HeadRo[2]])



import maya.cmds as mc
#follow World
WorldT = mc.xform('charlie01_l_arm01_ikcc_off',q = 1,ws = 1,t = 1)
WorldRo = mc.xform('charlie01_l_arm01_ikcc_off',q = 1,ws = 1,ro = 1)

mc.setAttr('charlie01_l_arm01_ikcc.follow',0)
mc.setAttr('charlie01_l_arm01_ikcc_off_parentConstraint1.charlie01_c_pelvis_ccW0',0)
mc.setAttr('charlie01_l_arm01_ikcc_off_parentConstraint1.charlie01_c_headMaster01_ccW1',0)

mc.xform('charlie01_l_arm01_ikcc_off' , ws = 1,t = [WorldT[0],WorldT[1],WorldT[2]])
mc.xform('charlie01_l_arm01_ikcc_off' , ws = 1,ro = [WorldRo[0],WorldRo[1],WorldRo[2]])



import maya.cmds as mc
#follow Hip
HipT = mc.xform('charlie01_l_arm01_ikcc_off',q = 1,ws = 1,t = 1)
HipRo = mc.xform('charlie01_l_arm01_ikcc_off',q = 1,ws = 1,ro = 1)

mc.setAttr('charlie01_l_arm01_ikcc.follow',0)
mc.setAttr('charlie01_l_arm01_ikcc_off_parentConstraint1.charlie01_c_pelvis_ccW0',1)
mc.setAttr('charlie01_l_arm01_ikcc_off_parentConstraint1.charlie01_c_headMaster01_ccW1',0)

mc.xform('charlie01_l_arm01_ikcc_off' , ws = 1,t = [HipT[0],HipT[1],HipT[2]])
mc.xform('charlie01_l_arm01_ikcc_off' , ws = 1,ro = [HipRo[0],HipRo[1],HipRo[2]])
