import Rhino.Geometry as rg
from math import sqrt

centroids = []
areas = []
spheres = []
names = []
# parsing space related attributes
for i in xrange(len(SpaceCentroid)):
    centroid = SpaceCentroid[i].replace(" ",'')
    centroid = centroid[1:-1].split('%')
    centroid = [float(j) for j in centroid]

    npt = rg.Point3d(centroid[0],centroid[1],centroid[2])
    centroids.append(npt)

    area = SpaceAreas[i].replace(" ",'')
    area = float(area)
    areas.append(area)

    ball = rg.Sphere(centroids[i],sqrt(area))
    spheres.append(ball)

    name = SpaceNames[i].replace(" ",'').replace("'",'')
    names.append(name)

relS = []
relE = []
lines = []
# parsing  relation related attributes
for i in xrange(len(Relations_A)):
    rA = Relations_A[i].replace(" ",'')
    relS.append(int(rA))

    rB = Relations_B[i].replace(" ",'')
    relE.append(int(rB))

    line = rg.Line(centroids[int(rA)], centroids[int(rB)])
    lines.append(line)

SpaceCentroids = centroids
SpaceAreas = areas
RelationsStart = relS
RelationsEnd = relE
SpaceNames = names
Spheres = spheres
Lines = lines