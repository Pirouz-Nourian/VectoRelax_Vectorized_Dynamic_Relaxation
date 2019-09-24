#####################################################
#####################################################
#####################################################

### Dynamic Relaxation
###
### Written by Shervin Azadi and Pirouz Nouriana, Last Edited on 10/09/2018
###
### Thanks to Ir. Dirk Rinze Visser for introducing the following reference:
### Adriaenssens, S., P. Block, D. Veenendaal, and C. Williams (2014). Shell Structures for Architecture: Form Finding and Optimization. New York: Routledge.
### "Chapter 2: Review of Dynamic Relaxation with an extension to six degrees of freedom theory" by Adriaenssens

#####################################################
###
### OBJ Reader
###
#####################################################

import copy

# Input data:
# -----------
# filename : the path of the starting obj

filename = 'OBJ_Files/BasicRhinoOutput.obj'

# opening the file
with open(filename, 'r') as myfile:
    data = myfile.read().split('\n')

# initiating the lists
xyz = []  # xyz coordinates
vertices = []  # unique xyz coordinates
points = []  # references to vertices
lines = []  # pairs of references to vertices

# parsing the obj file, filling the data lists
for line in data:
    # spliting the string line by ' '
    parts = line.split()
    # checking if it contains data
    if not parts:
        continue
    # assigning the 1st element to head and the rest to tail (for obj file instructure check here: http://paulbourke.net/dataformats/obj/)
    head = parts[0]
    tail = parts[1:]
    # appending vertex cordinations in (xyz) and assigning an index to them in (points)
    if head == 'v':
        ftail = [float(x) for x in tail]
        xyz.append(ftail)
        points.append(len(xyz)-1)
    # iterating through the edges of the faces and appending them in (lines)
    elif head == 'f':
        ftail = [float(x) for x in tail]
        for i in range(len(ftail)):
            sp = ftail[i%len(ftail)]
            ep = ftail[(i+1)%len(ftail)]
            lines.append((int(sp)-1, int(ep)-1))

# points to verticies (welding similar vertices)
x2v = {}
tol = 0.001 ** 2
# initiating the bounding box max and min point
bbmax = [0,0,0]
bbmin = [0,0,0]
for i, x in enumerate(iter(xyz)):
    found = False
    for j, v in enumerate(iter(vertices)):
        if (x[0] - v[0]) ** 2 < tol \
                and (x[1] - v[1]) ** 2 < tol \
                and (x[2] - v[2]) ** 2 < tol:
                found = True
                x2v[i] = j
                break
    if not found:
        x2v[i] = len(vertices)
        vertices.append(x)
    
    #finding the bounding box
    for i in range(3):
        if x[i] > bbmax[i]: bbmax[i] = x[i]
        if x[i] < bbmin[i]: bbmin[i] = x[i]

# redefining the indexes
points[:] = [x2v[index] for index in points]
# redefining the edges by the refined indexes
edges = [(x2v[u[0]], x2v[u[1]]) for u in lines]
# reserving the Initial State of the system
xyzIS = copy.deepcopy(vertices)

# Output data:
# -----------
# points : List of points
# edges : List of edges
# vertices : List of vertices
# xyzIS : Initial state of the system
# bbmax, bbmin : Bounding Box

#####################################################
###
### Dynamic Relaxation
###
#####################################################

from numpy import array, zeros, float64, append, sqrt, sign

# Input data:
# -----------
# vertices: a list of unique xyz coordinates
# edges: a list of pairs of vertex indices
# points: index list of fixed vertices
# bbmax, bbmin : Bounding Box

m = len(edges)
n = len(vertices)


# fixed points here are set to be the boundary of the rectangle
fixed = []
for i, pnt in enumerate(iter(xyz)):
    if abs(pnt[0] - bbmin[0]) < 0.01 or abs(pnt[0] - bbmax[0]) < 0.01:
        fixed.append(i)
    elif abs(pnt[1] - bbmin[1]) < 0.01 or abs(pnt[1] - bbmax[1]) < 0.01:
        fixed.append(i)

free = list(set(range(n)) - set(fixed))

xyz = array(vertices)
# p : Applied Load Component which in our case is zero
p = zeros((n, 3), dtype=float64)
# W : Gravity Force
W = array([array([0,0,9.8]) for i in range(n)])

# v : Velosity
v = zeros((n, 3), dtype=float64)
# restlength : Rest Length of the springs
diff = array([(xyz[edges[i][1]] - xyz[edges[i][0]]) for i in range(m)])
restlength = array([sqrt(diff[i,0]*diff[i,0] + diff[i,1]*diff[i,1] + diff[i,2]*diff[i,2]) for i in range(m)])

# adamp : Acceleration damp controls the stability of the system
adamp = 10
IterationMax = 100
# K : Elasticity Constant in Hooke's law
K = 20
# dt : Time intervals
dt = 0.1
mass = 1

for k in range(IterationMax):
    # S : Stiffness Force
    S = zeros((n, 3), dtype=float64)
    # R : Final Forces
    R = zeros((n, 3), dtype=float64)
    
    if k%100 == 0 : print (k)
    # xyz0 : Initial Position
    xyz0 = xyz.copy()
    # vp : Initial Velocity
    vp = v.copy()
    
    # calculating the length of the edges
    di = array([(xyz[edges[i][1]] - xyz[edges[i][0]]) for i in range(m)])
    dist = array([sqrt(di[i,0]*di[i,0] + di[i,1]*di[i,1] + di[i,2]*di[i,2]) for i in range(m)])

    # Hooke's law : Force = length difference * Elasticity Constant (K)
    EdgeForce = (dist - restlength) * K
    # Edge Force : Decomposing the existing force in each edge into the 3 dimensions 
    EdgeForceS = zeros((m, 3), dtype=float64)

    # iterating throughout the edges
    for i in range(m):
        for j in range(3):
            # Separating the forces into X, Y, Z dimensions
            EdgeForceS[i,j] = (di[i,j] / dist[i]) * EdgeForce[i]

        # Adding the force of each edge to the coresponding nodes
        S[edges[i][0]] -= EdgeForceS[i]
        S[edges[i][1]] += EdgeForceS[i]
    
    R[free] = p[free] + W[free] - S[free]

    A = 1/(1 + adamp * dt * 0.5)
    B = (1 - adamp * dt * 0.5 ) / (1 + adamp * dt * 0.5)
    
    # updating the velocity
    v[free] = A * dt * R[free] / mass + B * vp[free]
    # updating the position
    xyz[free] = xyz0[free] + dt * v[free]

# Output data:
# -----------
# xyzFS : Final state of the system

xyzFS = xyz

#####################################################
###
### Plotter
###
#####################################################

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Input data:
# -----------
# xyzIS : initial state of the system
# xyzFS : final state of the system
# bbmax, bbmin : Bounding Box

coordinates = xyzFS

# initiating the plotter
fig = plt.figure()
ax = fig.gca(projection='3d')

# plotting edges
for u, v in edges:
    ax.plot([coordinates[u][0], coordinates[v][0]],
            [coordinates[u][1], coordinates[v][1]],
            [coordinates[u][2], coordinates[v][2]], color='k')

# plotting points
for i in points:
    ax.scatter(coordinates[i][0], coordinates[i][1], coordinates[i][2],
               color='r', s=4)

ax.scatter([bbmin[0], bbmax[0]], [bbmin[1], bbmax[1]], [bbmin[2], bbmax[2]+10], color='w', s=1)
ax.set_xlim([bbmin[0], bbmax[0]])
ax.set_ylim([bbmin[1], bbmax[1]])
ax.set_zlim([bbmin[2], bbmax[2]+10])
ax.set_aspect('equal')

plt.show()

#####################################################
###
###
###
#####################################################
