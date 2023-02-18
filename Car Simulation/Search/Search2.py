#!/usr/bin/env pybricks-micropython

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

        evLogger.log("Vertex Successfully Instantiated") # logs that a vertex is successfully made

    def update_adjacency(self, input = [[],[],[],[]]):
        for i in range(0,4):
            try:
                if len(input[i]) > 0:
                    self.adjacencyLabels[i] = str(input[i][0])
                    self.adjacencyWeights[i] = int(input[i][1])
            except:
                evLogger.log("Incorrect Vertex Values Passed")
            
class Graph():
    def __init__(self, end_label):
        self.network = []
        self.label_index = 65 # 65 in unicode is A, works as an offset
        self.end = end_label
        self.nullVertex = Vertex("*")

        evLogger.log("Graph Successfully Instantiated") # logs that the graph is successfully made

    def add_vertex(self, left = [], right = [], rear = [], front = []):
        Vert = Vertex(chr(self.label_index))
        Vert.update_adjacency([left,right,rear,front])
        self.network.append(Vert)
        self.label_index += 1 # increments the label by 1 e.g A -> B

class car():
    def __init__(self):
        self.ev3 = EV3Brick()
        self.screen = self.ev3.screen
        self.buttons = self.ev3.buttons
        self.speaker = self.ev3.speaker

        self.motorA = Motor(Port.A)
        self.motorD = Motor(Port.D)

        self.driver = DriveBase(self.motorD,self.motorA,31,190) # wheels have diameter of 31mm and a drivebase width of 190mm    
        
        self.colsense = ColorSensor(Port.S4) # Left out as wont work right now, FIX THIS!!!!!
        self.driver.settings(straight_speed=200) # sets the cars speed to 200mm /s
        self.maze = Graph("Z")
        evLogger.log("Car Successfully Instantiated") # logs that the car object is successfully made

    def Search(self):
        
        evLogger.log("Starting Search")

        self.maze.add_vertex() # creates the initial vertex

        while self.colsense.color() != Color.GREEN:
            time.sleep(0.1)
            
            dir_offset = 0

            self.driver.drive(200,0) # sets the motors to drive forward
            
            if self.colsense.color() == Color.RED: # go straight ahead
                pass
            
            if self.colsense.color() != Color.RED: # re-adjust to find the line
                evLogger.log("Lost Line")

                self.driver.drive(0,0)
                self.driver.turn(-30)
                rel_angle = -30
                while rel_angle<30:
                    self.driver.turn(10)
                    if self.colsense.color() == Color.RED:
                        evLogger.log("Found Line")
                        break

                    rel_angle += 10
                 

            if self.colsense.color() != Color.RED: # find out which directions are possible to turn. 
                
                self.driver.turn(-30)
                directions = self.check_line()
                self.screen.print(directions)

                self.driver.straight(50)

                self.driver.drive(0,0)
                if "Left" in directions:
                    self.driver.turn(-90)
                    evLogger.log("Found Corner")
                    
                elif "Right" in directions:
                    self.driver.turn(90)
                    evLogger.log("Found Corner")
                    
                elif "Back" in directions:
                    self.driver.turn(180)
                    evLogger.log("Found Dead End")
                    

        evLogger.log("Search Complete") # logs that the search algorithm is done. 

    def check_line(self): # finds which directions are possible to turn. 
        evLogger.log("Check Line algorithm")
        
        self.maze.add_vertex(chr(self.maze.label_index))
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
            
evLogger = Logger.logger("Search2Logs.txt")

Car = car()

Car.Search()