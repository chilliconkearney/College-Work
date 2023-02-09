#!/usr/bin/env pybricks-micropython

#This is the Second menu prototype, which will include running subroutines from the menu
#This version will include the OOP approach

# importing the seperate sections of the solution. 
import Logger 

# Imports
import sys
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

class math: # allows me add math functions to class, and easily replace math.inf
    inf = float("inf")

class Vertex():
    def __init__(self, label):
        self.label = str(label)
        # left, right, rear, front
        self.adjacencyLabels = ["","","",""] # dictionary of the adjacent verticies
        self.adjacencyWeights = [math.inf, math.inf, math.inf, math.inf] # has all the connected arc weights set to infinity
        self.totalweight = math.inf
        self.permanent = False
        self.previousVertex = ""
        self.previousDir = 0

    def update_adjacency(self, input = [[],[],[],[]]):
        for i in range(0,4):
            try:
                if len(input[i]) > 0:
                    self.adjacencyLabels[i] = str(input[i][0])
                    self.adjacencyWeights[i] = int(input[i][1])
            except:
                print("one of your values isn't the correct type")
            
class Graph():
    def __init__(self, end_label):
        self.network = []
        self.label_index = 65 # 65 in unicode is A, works as an offset
        self.end = end_label
        self.nullVertex = Vertex("*")

    def add_vertex(self, left = [], right = [], rear = [], front = []):
        Vert = Vertex(chr(self.label_index))
        Vert.update_adjacency([left,right,rear,front])
        self.network.append(Vert)
        self.label_index += 1 # increments the label by 1 e.g A -> B

class Menu: # used for the different submenus in the UI
    def __init__(self, name, titlesList:list, subroutines=[]) -> None:
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

        self.colsense = ColorSensor(Port.S4) # Left out as wont work right now, FIX THIS!!!!!
        self.driver.settings(straight_speed=200) # sets the cars speed to 200mm /s
    
    def CalTurning(self):
        dirs = ["Right", "left"]
        for i in (0,1):
            self.screen.clear()
            print (dirs[i] + " is running")
            self.driver.turn(90-180*i)

        self.screen.clear()
        self.screen.print("Finding Line")
        time.sleep(1)

    def CalTrackLine(self):
        print("Tracking Line")

    def SetMotorSpeed(self):
        print("settings motor speed")

    def SetLogType(self):
        print("setting log type")

    def SetLogInterval(self):
        print("setting log interval")

    def RunAll(self):
        print("running all")

    def RunSearch(self):
        
        self.maze.add_vertex() # creates the initial vertex

        while self.colsense.color() != Color.BLUE:
            time.sleep(0.1)
            
            dir_offset = 0

            self.driver.drive(200,0) # sets the motors to drive forward
            
            if self.colsense.color() == Color.RED: # go straight ahead
                print("running")
            
            if self.colsense.color() != Color.RED:
                
                self.driver.drive(0,0)
                self.driver.turn(-30)
                rel_angle = -30
                while rel_angle<30:
                    self.driver.turn(10)
                    if self.colsense.color() == Color.RED:
                        break
                    rel_angle += 10
                self.driver.turn(-30) 

            if self.colsense.color() != Color.RED:
                directions = self.check_line()
                print(directions)
                time.sleep(30)

    def check_line(self):
        self.maze.add_vertex(chr(self.maze.label_index))
        self.driver.drive(0,0) # stops the motors
        rel_angle = 0
        possible_dirs = []
        
        print("Checking Line")

        while rel_angle<360:
            
            self.driver.turn(10)

            if rel_angle > 45 and rel_angle < 135 and "Right" not in possible_dirs and self.colsense.color() == Color.RED:
                possible_dirs.append("Right") 
            if rel_angle > 135 and rel_angle < 225 and "Back" not in possible_dirs and self.colsense.color() == Color.RED:
                possible_dirs.append("Back")
            if rel_angle > 225 and rel_angle < 360 and "Left" not in possible_dirs and self.colsense.color() == Color.RED:
                possible_dirs.append("Left")
            rel_angle+= 10

        return possible_dirs

    def RunSolved(self):
        print("running solved")

class Main: # will hold the main section of the program. useful for dropping in different main loops
    def __init__(self) -> None:
        self.active = True

    def runMain(self): # the main section of the code is here vvv
        LumberJack = Logger.Logger()
        Car = car()
        MainMenu = Menu("Main", ["Run Menu", "Calibration Menu", "Settings Menu", "Quit"])
        RunMenu = Menu("Run", ["Run All", "Run Search", "Run Solve", "Main Menu"])
        CalMenu = Menu("Calibration", ["Track Line", "Turning", "Main Menu"])
        SetMenu = Menu("Settings", ["Motor Speed", "Logging Type", "Logging Intervals", "Main Menu"])
        
        MainMenu.subroutines = [RunMenu, CalMenu, SetMenu, self.Exit]
        RunMenu.subroutines = [Car.RunAll, Car.RunSearch, Car.RunSolved, MainMenu]
        CalMenu.subroutines = [Car.CalTrackLine, Car.CalTurning, MainMenu]
        SetMenu.subroutines = [Car.SetMotorSpeed, Car.SetLogType, Car.SetLogInterval, MainMenu]
        
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
                    if isinstance(currentMenu.subroutines[pointer],Menu):
                        currentMenu = currentMenu.subroutines[pointer]
                        pointer = 0

                    else:
                        currentMenu.subroutines[pointer]()
                    
                except Exception as e: 
                    print("hmmm, this didnt work")
                    print("here is why:", e)

            time.sleep(0.1)

        # close the log file here
        Car.screen.clear()
        Car.screen.print("Shutting Down...")

    def Exit(self):
        self.active = False

MyMain = Main() # creates the main object
MyMain.runMain() # runs the main section of the code