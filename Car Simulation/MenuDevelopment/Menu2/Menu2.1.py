#!/usr/bin/env pybricks-micropython

#This is the Second menu prototype, which will include running subroutines from the menu
#This version will include the OOP approach

import time
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

ev3 = EV3Brick()

class Menu(): # used for the different submenus in the UI
    pass

class Main(): # will hold the main section of the program. useful for dropping in different main loops
    pass