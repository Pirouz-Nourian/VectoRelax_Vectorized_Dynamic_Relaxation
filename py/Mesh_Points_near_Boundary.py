"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "pnourian"
__version__ = "2020.08.21"

import rhinoscriptsyntax as rs
#import clr
#import System
import Rhino.Geometry as rg
maxDistance=10E6
minDistance=10E-6
CloseVertices=[]
CloseIndices=[]
for i in range(v.Count):
    vertex=v[i]
    #t=clr.References[System.Double]()#https://developer.rhino3d.com/guides/rhinopython/python-reference/
    CP=guideCrv.ClosestPoint(vertex,maxDistance)
    #print(CP) how to deal with 'out' (output) parameters and 'ref'(by reference) parameters: IronPython will return the output of such methods as tuples including these parameters! Note that we skipped the argument t in the signature of the function altogether!
    closestPoint=guideCrv.PointAt(CP[1])
    distance=closestPoint.DistanceTo(vertex)
    if distance<minDistance:
        CloseIndices.append(i)
        CloseVertices.append(vertex)
Indices=CloseIndices
Vertices=CloseVertices