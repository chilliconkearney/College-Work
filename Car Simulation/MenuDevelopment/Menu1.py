#!/usr/bin/env pybricks-micropython


#This is the initial menu prototype


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

# Subroutines


# Create your objects here.
ev3 = EV3Brick()
screen = ev3.screen
buttons = ev3.buttons

# Write your program here.

MainMenu = ["Main Menu","Item 1", "Item 2", "Item 3"]



for i in range(len(MainMenu)):
    screen.print(MainMenu[i])

pointer = 0

while True:
    screen.clear()
    for i in range(len(MainMenu)):
        screen.print(MainMenu[i])
    
    if Button.DOWN in buttons.pressed():
        pointer+=1
        time.sleep(0.3)
    
    if Button.UP in buttons.pressed():
        pointer-=1
        time.sleep(0.3)
    
    screen.draw_text(100,22+22*pointer,"<--")

    time.sleep(0.1)



