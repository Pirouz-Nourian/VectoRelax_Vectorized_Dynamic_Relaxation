"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "pnourian"
__version__ = "2020.08.21"

import Rhino.Geometry as rg
import System
m=rg.Mesh()
for faceTuple in f:
    if len(faceTuple)==4:
        m.Faces.AddFace(faceTuple[0],faceTuple[1],faceTuple[2],faceTuple[3])
    elif len(faceTuple)==3:
        m.Faces.AddFace(faceTuple[0],faceTuple[1],faceTuple[2])
IEV=System.Array[rg.Point3f](v)
m.Vertices.AddVertices(IEV)
a=m