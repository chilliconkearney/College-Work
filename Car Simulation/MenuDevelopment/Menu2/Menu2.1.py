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

# Subroutines

def Run():
    screen.clear()
    screen.print("Run is running")

    car.straight(1000) # forwards 1000 mm

    time.sleep(1)

def LeftRight():
    screen.clear()
    
    screen.print("Right is running")
    car.turn(90)
    time.sleep(1)
    
    screen.clear()
    
    screen.print("Left is running")
    car.turn(-90)
    time.sleep(1)

def IDLine():
    screen.clear()
    screen.print("IDLine is running")

    while colsense.color()!=Color.BLACK:
        screen.print(colsense.color())
        time.sleep(0.001)
    

def FindLine():
    screen.clear()
    screen.print("FindLine is running")

    

    time.sleep(1)


# Create your objects here.
ev3 = EV3Brick()
screen = ev3.screen
buttons = ev3.buttons

motorA = Motor(Port.A)
motorD = Motor(Port.D)

car = DriveBase(motorD,motorA,31,190) # wheels have diameter of 31mm and a drivebase width of 190mm

colsense = ColorSensor(Port.S4)

sensorList = [colsense]

# Write your program here.

MainMenu = ["Main Menu","Run", "Left RIght", "ID Line", "Find Line"]
MainMenuLookUp = [Run, LeftRight, IDLine, FindLine]

current_menu = MainMenu # allows for the main loop to update which menu it uses
current_menuLookUp = MainMenuLookUp

pointer = 0

car.settings(straight_speed=200)

while True:
    
    # Output to screen
    screen.clear()
    for i in range(len(current_menu)):
        if i != 0:
            if pointer+1==i:
                screen.print(current_menu[i]+" <--") # adds the cursor to the end of the text line
            else:
                screen.print(current_menu[i]) # prints all the other lines in the menu
        if i == 0:
            screen.print("")

    screen.draw_text(75, 0, current_menu[0])
    
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
        
        except Exception as e:
            print(e)
            time.sleep(1)

    time.sleep(0.1)