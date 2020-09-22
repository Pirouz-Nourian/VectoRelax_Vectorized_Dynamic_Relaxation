########################
# Dynamic Relaxation, by Pirouz Nourian & Shervin Azadi, last edited on 22-08-2020
# Licence and citation information on https://zenodo.org/record/3459223#.X0FG58gzZPY
########################
# Dynamic relaxation
# Input data:
# vertices: a list of unique xyz coordinates
# edges: a list of pairs of vertex indices
# points: index list of fixed vertices
# Output data:
# xyzFS : Final state of the system
import numpy as np
verts = np.array(v)
edges = np.array(e)
faces = np.array(f)  # unused for the moment, however in principle faces as 2D elements can ave elasticity as well. Right now, weare simiulating this mesh as a fishnet, as if it doesn't have faces!
#####################
# advanced setting parameters
#####################
c = damp  # adamp : Acceleration damp controls the stability of the system
MaximumIterations = IterCount
k = Elasticity  # K : Elasticity Constant in Hooke's law
dt = timeInterval  # dt : Time intervals
m = vertexMass

vertexCount = len(verts)
edgeCount = len(edges)
freeIndices = list(set(range(vertexCount)) - set(fixed)
                   )  # indices of free points
xyz = np.copy(verts)
p = np.zeros((vertexCount, 3), dtype=np.float64)
p = np.array(externalLoad)

if externalLoad == None and not justRelax:
    p = np.tile(np.multiply(m, np.array([0, 0, 9.81])), (vertexCount, 1))
elif justRelax:
    p = np.zeros((vertexCount, 3), dtype=np.float64)
if((not p.shape[0] == vertexCount)):
    raise Exception(
        'the length of the list of external loads is not the same as the list of vertices!')

# v : Velosity
v = np.zeros((vertexCount, 3), dtype=np.float64)
# restlength : Rest Length of the springs
# np.array([(xyz[edges[i][1]] - xyz[edges[i][0]]) for i in range(edgeCount)])
edgeVectors = xyz[edges[:, 1]] - xyz[edges[:, 0]]
# np.array([np.sqrt(diff[i,0]*diff[i,0] + diff[i,1]*diff[i,1] + diff[i,2]*diff[i,2]) for i in range(edgeCount)])
restlength = np.linalg.norm(edgeVectors, axis=1, keepdims=True)
if(justRelax):
    restlength = np.multiply(contraction, restlength)
###################
# the main loop, must be changed to a while loop but for now this is ok
###################
# xyz0 = xyz.copy()# xyz0 : Initial Position
differance = 1
tolerance = 10E-3
t = 0
# for t in range(MaximumIterations):
while((differance > tolerance) and t <= MaximumIterations):

    R = np.zeros((vertexCount, 3), dtype=np.float64)  # R : Final Forces
    vp = v.copy()  # vp : Initial Velocity
    xyz0 = xyz.copy()  # previous positions

    edgeVectors_t = xyz[edges[:, 1]] - xyz[edges[:, 0]]
    edgeLengths_t = (np.linalg.norm(edgeVectors_t, axis=1, keepdims=True))
    # .reshape((edgeCount,1))# f_{i,j} at the iteration time t, note that this is only the magnitude of these forces, i.e. |f_{i,j}=k\Delta l|
    EdgeForce = ((edgeLengths_t - restlength) * k)
    EdgeForceVectors = np.multiply(EdgeForce, np.divide(
        edgeVectors_t, edgeLengths_t))  # EdgeForce*(edgeVectors_t/edgeLengths_t)

    graph_force = np.zeros((vertexCount, vertexCount, 3))
    graph_force[edges[:, 0], edges[:, 1]] += EdgeForceVectors

    # S : Sum of Stiffness Force on vertices
    S = np.sum(graph_force, axis=0) - np.sum(graph_force, axis=1)
    R[freeIndices] = p[freeIndices] - S[freeIndices]

    A = 1/(1 + c * dt * 0.5)
    B = (1 - c * dt * 0.5) / (1 + c * dt * 0.5)
    v[freeIndices] = A * dt * R[freeIndices] / m + \
        B * vp[freeIndices]  # updating the velocity
    xyz[freeIndices] = xyz0[freeIndices] + dt * \
        v[freeIndices]  # updating the position
    differance = np.linalg.norm(xyz-xyz0, 'fro')

    t += 1

print(t)
print(differance)

X = xyz[:, 0].tolist()
Y = xyz[:, 1].tolist()
Z = xyz[:, 2].tolist()
