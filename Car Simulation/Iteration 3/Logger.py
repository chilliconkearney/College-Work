import time

class logger:
    loggingActive = True
    
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

    def dump(self, args): # dumps an object into a text file
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
        
        if self.loggingActive:
            with open(self.filename, "a") as writer:
                writer.write(lineStart + "[{}]".format(round(time.time() - self.init_time, 2)) + text + "\n")