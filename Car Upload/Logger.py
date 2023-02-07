import pickle
import time

class Logger:
    def __init__(self) -> None:
        self.filename = "Log.txt"
        self.interval = 0.1
        self.init_time = time.time()
        self.log()

    def dump(self, objects): # dumps an object into a text file
        with open("Tomb.txt", "r") as Tomb:
            try:
                for line in Tomb: pass
                last = line # saves the last line as last

                prefix = int(list(last)[0])+1
            except:
                prefix = 1

        with open("Tomb.txt", "a") as Tomb:
            for item in objects:
                Tomb.write(str(prefix) + " " + str(pickle.dumps(item)) + "\n")

    def retrieve(self, searchName, index=1): # retrieves an object from a text file
        with open("Tomb.txt", "r") as Tomb:
            for line in Tomb:
                if searchName in line and index == line.split()[0]:
                    
                    return pickle.loads(line.split()[1])

    def log(self, text="", index = -1): # used to log things. 
        presets = ["Logger Initialised",
                   "",
                   "",
                   ""] # creates a list of presets that can be accessed using an index.
        if index == -1:
            with open(self.filename, "a") as writer:
                writer.write("[{}]".format(round(time.time() - self.init_time, 4)) + text + "\n")
        
        else:
            with open(self.filename, "a") as writer:
                writer.write("[{}]".format(round(time.time() - self.init_time, 4)) + presets[index] + "\n")


Lumberjack = Logger()
Lumberjack.dump([Lumberjack])
Lumberjack.interval = 0.2
Lumberjack2 = Lumberjack.retrieve("Logger")
print(Lumberjack2.interval)
