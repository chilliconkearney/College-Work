#!/usr/bin/env pybricks-micropython


#This is the Second menu prototype, which will include running subroutines from the menu


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

def Run():
    screen.clear()
    screen.print("Run is running")
    time.sleep(1)

def Right():
    screen.clear()
    screen.print("Right is running")
    time.sleep(1)

def Left():
    screen.clear()
    screen.print("Left is running")
    time.sleep(1)

def IDLine():
    screen.clear()
    screen.print("IDLine is running")
    time.sleep(1)

def FindLine():
    screen.clear()
    screen.print("FindLine is running")
    time.sleep(1)


# Create your objects here.
ev3 = EV3Brick()
screen = ev3.screen
buttons = ev3.buttons

# Write your program here.

MainMenu = ["Run", "Right 90", "Left 90", "ID Line", "Find Line"]
MainMenuLookUp = [Run]




current_menu = MainMenu
current_menuLookUp = MainMenuLookUp


pointer = 0

while True:
    
    # Output to screen
    screen.clear()
    for i in range(len(current_menu)):
        screen.print(current_menu[i])
    
    # navigation
    
    if Button.DOWN in buttons.pressed():
        pointer+=1
        time.sleep(0.3)
    
    if Button.UP in buttons.pressed():
        pointer-=1
        time.sleep(0.3)


    if Button.CENTER in buttons.pressed():
        try:
            current_menuLookUp[pointer]()   
        
        
        except:
            pass



    screen.draw_text(100,22+22*pointer,"<--")

    time.sleep(0.1)



