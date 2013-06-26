#!/usr/bin/python

import array
import time
import math
import serial

import os
from RR_API import RR_API
import calibrate as cb

rr = RR_API()
rr.Connect("localhost")

PORT = '/dev/tty.usbmodem1421'
BAUD_RATE = 9600

ser = serial.Serial(PORT, BAUD_RATE)

data = rr.GetAllVariables()
bottomleft, topleft, bottomright, topright = cb.get_corners(data)
offsetx, offsety = cb.get_offset(bottomleft)
width, height = cb.get_sizes(bottomleft, topleft, bottomright, topright)
width = int(round(width))
height = int(round(height))

ser.write("*{0},{1}".format(width, height))

while True:
    try:
        data = rr.GetAllVariables()
        cogx = float(data['COG_X']) - offsetx
        cogy = float(data['COG_Y']) - offsety
        print "ping pong ball"
        cogx = int(round(cogx))
        cogy = int(round(cogy))
        print "({0}, {1})".format(cogx, cogy)
        print "width: {0}, height: {1}".format(width, height)
        ser.write("-{0},{1},{2},{3}".format(200, 74, cogx, cogy))
        time.sleep(.1)
    except KeyboardInterrupt:
        print "all done"
g        break
    except KeyError:
        os.system('clear')
        ser.write("-{0},{1},{2},{3}".format(1000, 1000, cogx, cogy))
        print "can't see ball :("
        os.system('clear')
        time.sleep(1)
        pass

ser.close()
print "all done"
