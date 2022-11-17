#!/usr/bin/env pybricks-micropython

#This is the Second menu prototype, which will include running subroutines from the menu
#This version will include the OOP approach

# Imports
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



class Menu: # used for the different submenus in the UI
    def __init__(self, name, titlesList:list) -> None:
        self.name = name
        self.titles = titlesList 

    def draw(self, screen, pointer): # draws onto the ev3 screen
        screen.draw_text(75, 0, self.name)
        screen.print("")
        for i in range(len(self.titles)):
            if pointer+1 == i:
                screen.print(self.titles[i]+" <--")
            else:
                screen.print(self.titles[i])


class Main: # will hold the main section of the program. useful for dropping in different main loops
    def __init__(self) -> None:
        self.active = True

    def runMain(self): # the main section of the code is here vvv
        MainMenu = Menu()
        currentMenu = MainMenu
        screen = ev3.screen

        while self.active:
            screen.clear()
            currentMenu.draw(ev3.screen)

            time.sleep(0.1)
        

        

ev3 = EV3Brick()
MyMain = Main() # creates the main object
MyMain.runMain() # runs the main section of the code
