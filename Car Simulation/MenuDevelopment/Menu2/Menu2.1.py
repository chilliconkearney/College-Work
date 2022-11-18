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
    def __init__(self, name, titlesList:list, subroutines:list) -> None:
        self.name = name
        self.titles = titlesList 
        self.subroutines = subroutines

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
        Car = car()
        MainMenu = Menu("main", ["Run meter", "Left Right", "ID Line", "Find Line"], [Car.RunM, Car.LeftRight, Car.IDLine, Car.Findline])
        currentMenu = MainMenu
        pointer = 0

        while self.active:
            Car.screen.clear()
            currentMenu.draw(Car.screen, pointer)

            if Button.DOWN in Car.buttons.pressed():
                pointer += 1
                time.sleep(0.3)
            if Button.UP in Car.buttons.pressed():
                pointer -= 1
                time.sleep(0.3)
            if Button.CENTER in Car.buttons.pressed():
                try: # will try to run the subroutine in the current menu
                    currentMenu.subroutines[pointer]()
                except: 
                    pass

            time.sleep(0.1)
        
class car:
    def __init__(self):
        self.ev3 = EV3Brick()
        self.screen = self.ev3.screen
        self.buttons = self.ev3.buttons

        self.motorA = Motor(Port.A)
        self.motorD = Motor(Port.D)

        self.driver = DriveBase(self.motorD,self.motorA,31,190) # wheels have diameter of 31mm and a drivebase width of 190mm    

        self.colsense = ColorSensor(Port.S4)

    def RunM(self):
        self.screen.clear()
        self.screen.print("Run is running")

        self.driver.straight(1000) # forwards 1000 mm

        time.sleep(1)
    
    def LeftRight(self):
        dirs = ["Right", "left"]
        for i in (0,1):
            self.screen.clear()
            print (dirs[i] + " is running")
            self.driver.turn(90-180*i)

    def IDLine(self):
        self.screen.clear()
        self.screen.print("IDline is running")

        while self.colsense.color() != Color.BLACK:
            self.screen.print(self.colsense.color())
            time.sleep(0.001)

    def Findline(self):
        pass
    

MyMain = Main() # creates the main object
MyMain.runMain() # runs the main section of the code
