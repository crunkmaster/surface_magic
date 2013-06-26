#!/usr/bin/python

import array
import time
import math

import os
from RR_API import RR_API

rr = RR_API()
rr.Connect("localhost")


try:
    # grab the data
    data = rr.GetAllVariables()
    fiducials = data['FIDUCIALS'].split(',')
    fiducials = map(float, fiducials)

    # generate matrix of fiducials
    fiducialMatrix = [[fiducials[j] for j in range( (i*17), (i*17) + 17 )]
                      for i in range(0, (len(fiducials) /17))]

    # put fiducials in a dictionary to make them easier to reference
    fiducialDict = {}
    for i in range(0, (len(fiducials) / 17)):
        fiducialDict['FID{0}'.format(i + 1)] = fiducialMatrix[i]

    centers = []

    for key in sorted( fiducialDict.iterkeys() ):

        # get all the x coordinates and all the y coordinates.
        xs = fiducialDict[key][1:8:2]
        ys = fiducialDict[key][2:9:2]
        # the center points are found by getting the avxerage of
        # all four points on the fiducial.
        centers.append([ sum(xs) / len(xs), sum(ys) / len(ys) ])

    # make sure we've got the right number of corners
    if len(centers) != 4:
        raise SystemExit("can't see all corners")

    # sort the centers by x coordinate
    centers.sort(key=lambda x: x[0])

    # split the list into the left points and rightpoints
    leftpoints = centers[:2]
    rightpoints = centers[2:4]

    # this part can definitely be refactored, but not right now
    # classify each of these points by their relative distance
    # from the origin.
    bottomleft = sorted(leftpoints, key=lambda x: x[1])[0]
    topleft = sorted(leftpoints, key=lambda x: x[1])[1]
    bottomright = sorted(rightpoints, key=lambda x: x[1])[0]
    topright = sorted(rightpoints, key=lambda x: x[1])[1]

    print "bottom left: {0}".format(bottomleft)
    print "bottom right: {0}".format(bottomright)
    print "topleft: {0}".format(topleft)
    print "topright: {0}".format(topright)

except KeyError:
    os.system('clear')
    print "no fiducial in vision"
    time.sleep(1)
    os.system('clear')
    pass
except KeyboardInterrupt:
    print "all done"
    print centers
