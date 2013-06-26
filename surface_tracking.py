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

# ser = serial.Serial(PORT, BAUD_RATE)

while True:
    try:
        data = rr.GetAllVariables()
        offsetx, offsety = cb.get_offset(data)
        print "offsetx: {0} offsety: {1}".format(offsetx, offsety)
        cogx = data['COG_X'] - offsetx
        cogy = data['COG_Y'] - offsety
        print "ping pong ball"
        print "({0}, {1})".format(cogx, cogy)
        ser.write("-{0},{1},{2},{3}".format(200, 74, cogx, cogy))
        time.sleep(.1)
    except KeyboardInterrupt:
        print "all done"
        break
    except KeyError:
        os.system('cls')
        ser.write("-{0},{1},{2},{3}".format(1000, 1000, cogx, cogy))
        print "can't see ball :("
        time.sleep(1)
        os.system('cls')
        pass

ser.close()
print "all done"
