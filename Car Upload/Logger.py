import pickle
import time
import os

class Logger:
    def __init__(self) -> None:
        self.filename = "Log.txt"
        self.interval = 0.1
        self.init_time = time.time()
        self.log(index=0)
        self.name = "Logger"

    def dump(self, objects): # dumps an object into a text file
        #finding what increment is next and updating the file to store this increment. 
        with open("increment.txt", "r") as openFile:
            for line in openFile: pass
            this_increment = int(line) + 1
        with open("increment.txt", "w") as openFile:
            openFile.write(str(this_increment))
        
        self.object_increment = this_increment
        
        for item in objects:
            with open(str(this_increment) + " " + item.name, "wb") as Tomb:
                pickle.dump(item, Tomb)
                self.log("{} dumped".format(item.name))

    def retrieve(self, searchName, index=1): # retrieves an object from a text file
        with open(str(index) + " " + searchName, "rb") as Tomb:
            return pickle.load(Tomb)
                
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
            writer.write(lineStart + "[{}]".format(round(time.time() - self.init_time, 4)) + text + "\n")