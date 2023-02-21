#!/usr/bin/env pybricks-micropython

#This is the Second menu prototype, which will include running subroutines from the menu
#This version will include the OOP approach

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
        self.ObjectID = "vertex"

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
        self.route = ""
        self.ObjectID = "graph"

    def __call__(self):
        properties = []
        properties.append(self.end)
        return properties
        
    def build(properties):
        print(len(properties))
        this = Graph(properties[0])
        return this
        
    def add_vertex(self, left = [], right = [], rear = [], front = []):
        Vert = Vertex(chr(self.label_index))
        Vert.update_adjacency([left,right,rear,front])
        self.network.append(Vert)
        self.label_index += 1 # increments the label by 1 e.g A -> B

    def Dijkstras(self):
        Queue = self.network
        Permanent = []
        
        Queue[0].totalweight = 0 # sets the initial vertex weight to 0
        end_vertex = self.find_vertex(Queue, self.end)

        while end_vertex in Queue: # the main loop which checks all the vertices
            self.bubble(Queue) # sorts the queue
            
            current_vertex = Queue.pop(0) # similar to the dequeue in static languages
            current_vertex.permanent = True

            Permanent.append(current_vertex)

            for i in range(0,4): # iterates from 0 to 3, stops when at 4
                dirVertex = self.find_vertex(Queue,current_vertex.adjacencyLabels[i]) # finds the vertex in the direction

                if dirVertex.totalweight > current_vertex.totalweight + current_vertex.adjacencyWeights[i]:
                        dirVertex.totalweight = current_vertex.totalweight + current_vertex.adjacencyWeights[i]
                        dirVertex.previousVertex = current_vertex.label
                        dirVertex.previousDir = i

        # Output the final path to follow
        print(self.findPath(Permanent, self.end))

    def findPath(self, final_list, curlabel, output = ""): # traces the path back to the start
        dirList = ["Left", "Right", "Rear", "Front"]
        curVertex = self.find_vertex(final_list, curlabel)
        output += "\n\nlabel: {},\nweight: {},\ndir: {}".format(curVertex.label, curVertex.totalweight, dirList[curVertex.previousDir])
        if curVertex.label == "A":
            return output
        else:
            return self.findPath(final_list,curVertex.previousVertex, output)
 
    def find_vertex(self, Queue, label):
        if len(Queue)>0:
            for item in Queue:
                if item.label == label:
                    return item # returns the vertex 
        return self.nullVertex
            
    def bubble(self, queue): # sorts the vertices by weight from start
            swaps = 1
            while swaps > 0:
                swaps = 0

                for i in range(0, len(queue)-1):
                    if queue[i].totalweight > queue[i+1].totalweight: 
                        queue[i], queue[i+1] = queue[i+1], queue[i] # swaps the two values round
                        swaps += 1

            return queue # returns the sorted version of queue

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
    def __init__(self):
        self.ev3 = EV3Brick()
        self.screen = self.ev3.screen
        self.buttons = self.ev3.buttons

        self.motorA = Motor(Port.A)
        self.motorD = Motor(Port.D)

        self.driver = DriveBase(self.motorD,self.motorA,31,190) # wheels have diameter of 31mm and a drivebase width of 190mm    

        self.colsense = ColorSensor(Port.S4) # Left out as wont work right now, FIX THIS!!!!!
        self.driver.settings(straight_speed=200) # sets the cars speed to 200mm /s

        self.ObjectID = "car"
    
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
        print("running search")

    def RunSolved(self):
        print("running solved")

class logger:
    def __init__(self, filename="Log.txt") -> None:
        self.filename = filename
        self.interval = 0.1
        self.init_time = time.time()
        self.log(index=0, lineStart="\n") # logs that it has initialised itself. 
        self.ObjectID = "logger"

    def __call__(self):
        properties = []
        properties.append(self.filename)
        properties.append(str(self.interval))
        properties.append(str(self.init_time))
        properties.append(self.ObjectID)

        return properties

    def dump(self, *args): # dumps an object into a text file
        #finding what increment is next and updating the file to store this increment. 
        with open("increment.txt", "r") as openFile:
            for line in openFile: pass
            this_increment = int(line) + 1
        with open("increment.txt", "w") as openFile:
            openFile.write(str(this_increment))
        
        self.object_increment = this_increment
        
        for item in args:
            with open(str(this_increment) + " " + item.ObjectID, "w") as Tomb:
                
                
                for i in range(len(item())):
                    if i == 0:
                        Tomb.write("{}".format(item()[0]))
                    else:
                        Tomb.write("\n{}".format(item()[i]))
                    i+=1

                self.log("{} dumped".format(item.ObjectID))



    def retrieve(self, searchName, object, index=1): # retrieves an object from a text file
        with open(str(index) + " " + searchName, "r") as Tomb:
            
            properties = []

            for line in Tomb.readlines():
                properties.append(line.strip())
            

            return object.build(properties)



    def log(self, text="", index = -1, lineStart = ""): # used to log things. 
        presets = ["Logger Initialised",
                   "Graph Initialised",
                   "",
                   ""] # creates a list of presets that can be accessed using an index.

        if index == -1:
            pass
        elif index < -1:
            text = "Log Index Does Not Exist"            
        else:
            text = presets[index]
        
        with open(self.filename, "a") as writer:
            writer.write(lineStart + "[{}]".format(round(time.time() - self.init_time, 2)) + text + "\n")

class Main: # will hold the main section of the program. useful for dropping in different main loops
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


L1 = logger()
G1 = Graph("Z")

L1.dump(G1)
print(L1.retrieve("graph", Graph, index=5).end)

MyMain = Main() # creates the main object
#MyMain.runMain() # runs the main section of the code