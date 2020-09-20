"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "pnourian"
__version__ = "2020.08.21"

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
tolerance=10E-3
chosenVertices=[]
chosenIndices=[]
for i in range(v.Count):#vertex in v:
    vertex=v[i]
    insideInside=(inside.Contains(vertex, rg.Plane.WorldXY,tolerance)==rg.PointContainment.Inside)
    outsideOutside=(outside.Contains(vertex, rg.Plane.WorldXY,tolerance)==rg.PointContainment.Outside)
    chosen=insideInside and outsideOutside
    if chosen:
        chosenVertices.append(vertex)
        chosenIndices.append(i)
inBandVertices=chosenVertices
inBandIndices=chosenIndices
