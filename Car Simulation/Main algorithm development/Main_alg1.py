#!/usr/bin/env pybricks-micropython

#This is the Second menu prototype, which will include running subroutines from the menu
#This version will include the OOP approach

# Imports
import time
import math
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                             InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

class Graph: # will hold all the vertices and operations of the graph
    def __init__(self):
        verticies = []

    def Dijkstras(self):
        pass

    def add_vertex(self):
        pass

    def sort_queue(self):
        pass

class vertex: # the base class of the vertex
    def __init__(self, label, dir0:list, dir1:list, dir2:list, dir3:list, type =1):
        self.label = label
        self.adjlabels = [dir0[0], dir1[0],dir2[0],dir3[0]]
        self.adjweights = [dir0[1], dir1[1],dir2[1],dir3[1]]
        if type ==0:
            self.currentcost = 0
            self.previouslabel = self.label

        elif type == 1:
            self.currentcost = math.inf
            self.previouslabel = None

        self.visited = False
        self.permacost = 0

class Menu: # used for the different submenus in the UI
    def __init__(self, name, titlesList:list, subroutines:list) -> None:
        self.name = name
        self.titles = titlesList 
        self.subroutines = subroutines

    def draw(self, screen, pointer): # draws onto the ev3 screen
        screen.draw_text(115, 5, self.name)
        screen.print("")
        for i in range(len(self.titles)):
            if pointer == i:
                screen.print(self.titles[i]+" <--")
            else:
                screen.print(self.titles[i])

class car:
    def __init__(self):
        self.ev3 = EV3Brick()
        self.screen = self.ev3.screen
        self.buttons = self.ev3.buttons

        self.motorA = Motor(Port.A)
        self.motorD = Motor(Port.D)

        self.driver = DriveBase(self.motorD,self.motorA,31,190) # wheels have diameter of 31mm and a drivebase width of 190mm    

        self.colsense = ColorSensor(Port.S4)
        self.driver.settings(straight_speed=200) # sets the cars speed to 200mm /s

        self.maze = Graph()

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
        self.screen.clear()
        self.screen.print("Finding Line")
        time.sleep(1)

    def search_algorithm(self):
        while True:
            self.driver.straight(10)

            if self.check_line(0,0):
                pass

            elif self.check_line(-45, 45):
                pass

            elif self.check_line(45,135):
                pass

            elif self.check_line(-135,-45):
                pass

            elif self.check_line(135, -135):
                pass
    
    def check_line(start_point:int, end_point:int):
        pass

class Main: # will hold the main section of the program. useful for dropping in different main loops
    def __init__(self) -> None:
        self.active = True

    def __call__(self): # the main section of the code is here vvv
        Car = car()
        MainMenu = Menu("Main", ["Run meter", "Left Right", "ID Line", "Find Line"], [Car.RunM, Car.LeftRight, Car.IDLine, Car.Findline])
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
        
    
#MyMain = Main() # creates the main object
#MyMain() # runs the main section of the code