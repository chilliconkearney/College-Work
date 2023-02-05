#!/usr/bin/env pybricks-micropython

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

class car():
    def __init__(self):
        self.ev3 = EV3Brick()
        self.screen = self.ev3.screen
        self.buttons = self.ev3.buttons

        self.motorA = Motor(Port.A)
        self.motorD = Motor(Port.D)

        self.driver = DriveBase(self.motorD,self.motorA,31,190) # wheels have diameter of 31mm and a drivebase width of 190mm    
        
        self.colsense = ColorSensor(Port.S4) # Left out as wont work right now, FIX THIS!!!!!
        self.driver.settings(straight_speed=200) # sets the cars speed to 200mm /s
        self.maze = Graph("Z")

    def Search(self):
        
        self.maze.add_vertex() # creates the initial vertex

        while self.colsense.color() != Color.BLUE:
            time.sleep(0.1)
            
            dir_offset = 0

            self.driver.drive(200,0) # sets the motors to drive forward
            
            if self.colsense.color() == Color.RED: # go straight ahead
                print("running")
            
            elif self.check_line(-45,45): # within 90* ahead
                pass
            
            elif self.check_line(45,135): # within the 90* to the right
                self.maze.add_vertex(left=[chr(self.maze.label_index), self.driver.distance])
                self.driver.reset()

                dir_offset += 1 # increments the direction offset

            elif self.check_line(-135, -45):
                self.maze.add_vertex(right=[chr(self.maze.label_index), self.driver.distance])
                self.driver.reset()

                dir_offset -= 1

            elif self.check_line(135,-135):
                self.maze.add_vertex()
            

    def check_line(self, start_point, end_point):
        self.driver.drive(0,0) # stops the motors
        x = (end_point-start_point)/10
        self.driver.turn((self.driver.angle() - start_point))

        while self.driver.angle() < end_point:
            self.driver.turn(x)
            if self.colsense.color() == Color.RED:
                return True

        return False




Car = car()

Car.Search()