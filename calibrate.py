#!/usr/bin/python

import array
import time
import math

def get_corners(data):
    fiducials = data['FIDUCIALS'].split(',')
    fiducials = map(float, fiducials)
    fiducialMatrix = [[fiducials[j] for j in range( (i*17), (i*17) + 17 )]

                      for i in range(0, (len(fiducials) /17))]

    fiducialDict = {}
    for i in range(0, (len(fiducials) / 17)):
        fiducialDict['FID{0}'.format(i + 1)] = fiducialMatrix[i]

    centers = []
    for key in sorted( fiducialDict.iterkeys() ):
        xs = fiducialDict[key][1:8:2]
        ys = fiducialDict[key][2:9:2]
        centers.append([ sum(xs) / len(xs), sum(ys) / len(ys) ])

    if len(centers) != 4:
        raise SystemExit("can't see all corners")

    centers.sort(key=lambda x: x[0])

    leftpoints = centers[:2]
    rightpoints = centers[2:4]

    bottomleft = sorted(leftpoints, key=lambda x: x[1])[0]
    topleft = sorted(leftpoints, key=lambda x: x[1])[1]

    bottomright = sorted(rightpoints, key=lambda x: x[1])[0]
    topright = sorted(rightpoints, key=lambda x: x[1])[1]

    return (bottomleft, topleft, bottomright, topright)

def get_offset(bottomleft):
    offsetx = bottomleft[0] # x coordinate of bottomleft point
    offsety = bottomleft[1] # y coordinate of bottomleft point
    return(offsetx, offsety)

def get_sizes(bottomleft, topleft, bottomright, topright):
    width = bottomright[0] - bottomleft[0]
    height = topleft[1] - bottomleft[1]
    return(width, height)
