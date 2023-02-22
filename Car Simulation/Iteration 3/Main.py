#!/usr/bin/env pybricks-micropython

#This is the Second menu prototype, which will include running subroutines from the menu
#This version will include the OOP approach

import Logger
import Graphing

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

class Menu: # used for the different submenus in the UI
    def __init__(self, name, titlesList:list, subroutines=[]) -> None:
        self.name = name
        self.titles = titlesList 
        self.subroutines = subroutines
        self.ObjectID = "menu"

    def draw(self, screen, pointer): # draws onto the ev3 screen
        screen.draw_text(170-(len(self.name)*10), 5, self.name)
        screen.print("")
        for i in range(len(self.titles)):
            if pointer == i:
                screen.print(self.titles[i]+" <--")
            else:
                screen.print(self.titles[i])

class car:
    maze = Graphing.Graph("D") # creates a graph with final vertex Z
    
    def __init__(self):
        self.ev3 = EV3Brick()
        self.screen = self.ev3.screen
        self.buttons = self.ev3.buttons

        self.motorA = Motor(Port.A)
        self.motorD = Motor(Port.D)

        self.driver = DriveBase(self.motorD,self.motorA,31,190) # wheels have diameter of 31mm and a drivebase width of 190mm    

        self.colsense = ColorSensor(Port.S4) # Left out as wont work right now, FIX THIS!!!!!
        self.speed = 200
        self.driver.settings(straight_speed=self.speed) # sets the cars speed to 200mm /s

        self.ObjectID = "car"
    
    def CalTurning(self): # turns about a point and prints the list of directions possible
        self.screen.clear()
        directions = self.check_line()
        self.screen.print(directions)
        evLogger.log(directions)
        time.sleep(10)

    def CalTrackLine(self): # will carry on going down a red line until the line stops
        self.screen.clear()

        runLoop = True

        while runLoop == True:
            time.sleep(0.1)

            lineFound = True

            self.driver.drive(self.speed,0)

            if self.colsense.color() == Color.RED:
                pass

            if self.colsense.color() != Color.RED: # re-adjust to find the line
                evLogger.log("Lost Line")
                lineFound = False
                self.driver.drive(0,0)
                self.driver.turn(-30)
                rel_angle = -30
                while rel_angle<30:
                    self.driver.turn(8)
                    if self.colsense.color() == Color.RED:
                        lineFound = True
                        evLogger.log("Found Line")
                        break
                    
                    if self.colsense.color() == Color.GREEN:
                        runLoop = False
                        lineFound = True
                        evLogger.log("Found End")
                        runLoop = False
                        break
                    rel_angle += 8

                if lineFound == False:
                    runLoop = False
                    evLogger.log("End of Line Found")


    def SetMotorSpeed(self): # increases or decreases the speed of the motor
        while Button.CENTER not in self.buttons.pressed(): # if the center button is pressed, take this as enter and exit the subroutine
            time.sleep(0.05)
            self.screen.clear()
            self.screen.print(self.speed) # print the current speed.
            if Button.UP in self.buttons.pressed() and self.speed <= 290: # increase the speed if the up button is pressed
                self.speed += 10
            elif Button.DOWN in self.buttons.pressed() and self.screen >= 110: # decrease the speed if the down button is pressed
                self.speed -= 10
        self.driver.settings(straight_speed=self.speed)
        evLogger.log("driver speed set to {}".format(self.speed))
        time.sleep(5)

    def SetLogType(self): # toggles logging on/off
        self.screen.clear()
        evLogger.loggingActive = not evLogger.loggingActive
        self.screen.print("Logging toggled {}".format(evLogger.loggingActive))
        time.sleep(5)

    def SetLogInterval(self):
        while Button.CENTER not in self.buttons.pressed(): # if the center button is pressed, take this as enter and exit the subroutine
            time.sleep(0.05)
            self.screen.clear()
            self.screen.print(evLogger.interval) # print the current speed.
            if Button.UP in self.buttons.pressed(): # increase the speed if the up button is pressed
                evLogger.interval += 0.1
            elif Button.DOWN in self.buttons.pressed(): # decrease the speed if the down button is pressed
                evLogger.interval -= 0.1
        evLogger.log("Logger interval set to {}".format(evLogger.interval))
        time.sleep(5)

    def RunAll(self): # runs both of the subroutines: hence will search the maze, then will traverse the maze back and run the complete solved maze
        self.RunSearch()
        self.RunSolved() # needs to run the maze that has just been solved. 

    def RunSearch(self):
        
        self.screen.clear()

        time.sleep(2) # waits 2 secs before starting the search

        evLogger.log("Starting Search")

        self.maze.add_vertex(0, 0, [True,False,False,False]) # creates the initial vertex: A

        dirfacing = 0 # facing north relative to start

        runLoop = True

        while runLoop == True:
            time.sleep(0.1)
            
            lineFound = True

            self.driver.drive(self.speed,0) # sets the motors to drive forward
            
            if self.colsense.color() == Color.RED: # go straight ahead
                pass
            
            if self.colsense.color() != Color.RED: # re-adjust to find the line
                evLogger.log("Lost Line")
                lineFound = False
                self.driver.drive(0,0)
                self.driver.turn(-30)
                rel_angle = -30
                while rel_angle<30:
                    self.driver.turn(8)
                    if self.colsense.color() == Color.RED:
                        lineFound = True
                        evLogger.log("Found Line")
                        break
                    
                    if self.colsense.color() == Color.GREEN:
                        runLoop = False
                        lineFound = True
                        evLogger.log("Found End")
                        
                        break
                    rel_angle += 8
                 

            if lineFound == False: # find out which directions are possible to turn. 

                self.driver.turn(-30)
                directions = self.check_line()
                self.screen.print(directions)

                abs_directions = [False,False,False,False] # a list of the directions in NESW
                if "Left" in directions:
                    abs_directions[(dirfacing-1)%4] = True
                if "Right" in directions:
                    abs_directions[(dirfacing+1)%4] = True
                if "Back" in directions:
                    abs_directions[(dirfacing+2)%4] = True

                self.driver.straight(50)

                self.maze.add_vertex(dirfacing, self.driver.distance(), abs_directions)
                self.driver.reset()
                self.driver.drive(0,0)
                
                if "Left" in directions:
                    self.driver.turn(-90)
                    evLogger.log("Found Corner")
                    
                elif "Right" in directions:
                    self.driver.turn(90)
                    evLogger.log("Found Corner")
                    
                elif "Back" in directions: 
                    # problem here, as it doesnt know that the vertex
                    # before this vertex is going to be the next vertex.
                    # Hence, needs some condition to know it needs to 
                    # navigate to another vertex that isnt complete.
                    self.driver.turn(180)
                    evLogger.log("Found Dead End")
                    
        abs_directions = [False,False,False,False]
        abs_directions[(dirfacing+2)%4] = True
        self.maze.end = chr(self.maze.label_index)
        self.maze.add_vertex(dirfacing, self.driver.distance(), abs_directions)
        try:
            evLogger.log(self.maze.Dijkstras())
        except Exception as e:
            evLogger.log(e)
        evLogger.log("Search Complete") # logs that the search algorithm is done. 

    def check_line(self): # finds which directions are possible to turn. 
        evLogger.log("Check Line algorithm")
        
        self.driver.drive(0,0) # stops the motors
        rel_angle = 0
        possible_dirs = []

        while rel_angle<330:
            
            self.driver.turn(10)

            if rel_angle > 0 and rel_angle < 135 and "Right" not in possible_dirs and self.colsense.color() == Color.RED:
                possible_dirs.append("Right") 
            if rel_angle > 135 and rel_angle < 225 and "Back" not in possible_dirs and self.colsense.color() == Color.RED:
                possible_dirs.append("Back")
            if rel_angle > 225 and rel_angle < 360 and "Left" not in possible_dirs and self.colsense.color() == Color.RED:
                possible_dirs.append("Left")
            rel_angle+= 10

        return possible_dirs

    def RunSolved(self, maze_index): # will take any of the previously solved mazes, and execute the path. 
        pass

class main: # will hold the main section of the program. useful for dropping in different main loops
    def __init__(self) -> None:
        self.active = True
        self.ObjectID = "main"

    def runMain(self): # the main section of the code is here vvv
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
                time.sleep(0.05)
            if Button.UP in Car.buttons.pressed():
                pointer -= 1
                time.sleep(0.05)
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

            time.sleep(0.2)

        # close the log file here
        Car.screen.clear()
        Car.screen.print("Shutting Down...")

    def Exit(self):
        self.active = False

evLogger = Logger.logger()

MyMain = main() # creates the main object
MyMain.runMain() # runs the main section of the code