import pymel.core as pm
from see import see

def clusLoc():
    '''create a clus base on edges'''
    #sl edges
    edges = pm.selected(flatten = True)
    #convert to edges
    verts = list(set(sum([list(e.connectedVertices()) for e in edges],[])))
    #create clus
    clusShp,clusTras = pm.cluster(verts)
    
    loc = pm.spaceLocator()
    pcn = pm.pointConstraint(clusTras,loc, mo = False)
    pm.delete(pcn)
    pm.delete(clusTras)    
    
clusLoc()    
    
    


    
