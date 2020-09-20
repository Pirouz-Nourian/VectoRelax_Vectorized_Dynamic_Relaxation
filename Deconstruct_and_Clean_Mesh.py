__author__ = "pnourian"
__version__ = "2020.08.21"

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math
#####################################
#input validation: weldedness, manifoldness, cleanness
#####################################
if not M.IsManifold(True):
    raise Exception("the input mesh is non-mannifold and this method is not designed to work with non-manifold meshes!")
M.Weld(math.pi)
M.Vertices.CombineIdentical(True,True)
M.Vertices.CullUnused()
if not M.Vertices.Count==M.TopologyVertices.Count:
    raise Exception("the input mesh must be completely welded; although we tried our best, the given mesh seems to have a problem not allowing it to be fully welded!")
#####################################
#exporting vertices as a list of rg.Point3f
#####################################
v=M.Vertices.ToPoint3fArray()
#####################################
#exporting edges as a list of tuples
#####################################
edges=[]
for edgeIndex in range(M.TopologyEdges.Count):
    IJ=M.TopologyEdges.GetTopologyVertices(edgeIndex)
    edges.append((IJ.I,IJ.J))
e=edges
#####################################
#exporting faces as a list of tuples
#####################################
faces=[]
if M.Faces.QuadCount==M.Faces.Count:
    print("a fully quadrilateral mesh")
    for face in M.Faces:
        faces.append((face.A,face.B,face.C,face.D))
elif M.Faces.TriangleCount==M.Faces.Count:
    print("a fully triangular mesh")
    for face in M.Faces:
        faces.append((face.A,face.B,face.C))
else:
    raise Exception("this method only works for meshes that are either fully quadrilateral or fully triangular!")

f=faces
