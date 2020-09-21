########################
#Dynamic Relaxation, a description
########################
# Dynamic relaxation
### Input data:
# vertices: a list of unique xyz coordinates
# edges: a list of pairs of vertex indices
# points: index list of fixed vertices
### Output data:
# xyzFS : Final state of the system
import numpy as np
verts=np.array(v)
edges=np.array(e)
faces=np.array(f)# unused for the moment, however in principle faces as 2D elements can ave elasticity as well. Right now, weare simiulating this mesh as a fishnet, as if it doesn't have faces!
#####################
#advanced setting parameters
#####################
c = damp# adamp : Acceleration damp controls the stability of the system
MaximumIterations = IterCount
k = Elasticity# K : Elasticity Constant in Hooke's law
dt = timeInterval# dt : Time intervals
m = vertexMass

vertexCount = len(verts)
edgeCount = len(edges)
freeIndices = list(set(range(vertexCount)) - set(fixed))#indices of free points
xyz = np.copy(verts)
p=np.zeros((vertexCount, 3), dtype=np.float64)
p=np.array(externalLoad)
if externalLoad==None and not justRelax:
    p=np.tile(np.multiply(m,np.array([0,0,9.81])),(vertexCount,1))
elif justRelax:
    p=np.zeros((vertexCount, 3), dtype=np.float64)
if((not p.shape[0]==vertexCount)):
    raise Exception('the length of the list of external loads is not the same as the list of vertices!')
#p = np.zeros((vertexCount, 3), dtype=np.float64)# p : Applied external/lateral Load Component which in our case is zero
# W : Gravity Force
#W = np.tile(np.array([0,0,9.81]),(vertexCount,1))#np.array([np.array([0,0,9.81]) for i in range(vertexCount)])
# v : Velosity
v = np.zeros((vertexCount, 3), dtype=np.float64)
# restlength : Rest Length of the springs
edgeVectors = xyz[edges[:,1]] - xyz[edges[:,0]]#np.array([(xyz[edges[i][1]] - xyz[edges[i][0]]) for i in range(edgeCount)])
restlength = np.linalg.norm(edgeVectors,axis=1,keepdims=True)#np.array([np.sqrt(diff[i,0]*diff[i,0] + diff[i,1]*diff[i,1] + diff[i,2]*diff[i,2]) for i in range(edgeCount)])
if(justRelax):
    restlength=np.multiply(contraction,restlength)
###################
#the main loop, must be changed to a while loop but for now this is ok
###################
#xyz0 = xyz.copy()# xyz0 : Initial Position
differance=1
tolerance=10E-3
t=0
while((differance>tolerance)and t<=MaximumIterations):#for t in range(MaximumIterations):
    S = np.zeros((vertexCount, 3), dtype=np.float64)# S : Sum of Stiffness Force on vertices
    R = np.zeros((vertexCount, 3), dtype=np.float64)# R : Final Forces
    vp = v.copy()# vp : Initial Velocity
    edgeVectors_t = xyz[edges[:,1]] - xyz[edges[:,0]]
    edgeLengths_t = (np.linalg.norm(edgeVectors_t,axis=1,keepdims=True))
    EdgeForce = ((edgeLengths_t - restlength) * k)#.reshape((edgeCount,1))# f_{i,j} at the iteration time t, note that this is only the magnitude of these forces, i.e. |f_{i,j}=k\Delta l|  
    EdgeForceVectors=np.multiply(EdgeForce,np.divide(edgeVectors_t,edgeLengths_t))#EdgeForce*(edgeVectors_t/edgeLengths_t)
    xyz0 = xyz.copy()#previous positions
    
    #S[edges[:,0]]-=EdgeForceVectors[:]
    #S[edges[:,1]]+=EdgeForceVectors[:]
    for e in range(edgeCount):# iterating throughout the edges, adding the force of each edge to the coresponding nodes 
        S[edges[e,0]] -= EdgeForceVectors[e]
        S[edges[e,1]] += EdgeForceVectors[e]
    R[freeIndices] = p[freeIndices] - S[freeIndices]
    A = 1/(1 + c * dt * 0.5)
    B = (1 - c * dt * 0.5 ) / (1 + c * dt * 0.5)
    v[freeIndices] = A * dt * R[freeIndices] / m + B * vp[freeIndices]# updating the velocity
    xyz[freeIndices] = xyz0[freeIndices] + dt * v[freeIndices]# updating the position
    differance=np.linalg.norm(xyz-xyz0,'fro')
    #print(differance)
    t+=1
print(t)
print(differance)
X=xyz[:,0].tolist()
Y=xyz[:,1].tolist()
Z=xyz[:,2].tolist()

