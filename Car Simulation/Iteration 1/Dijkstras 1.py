import math
import time

class Vertex():
    def __init__(self, label, left = [None,None], right = [None,None], rear = [None, None], front = [None, None]): # lists stored as [label, weight]
        self.label = str(label)
        self.adjacencyDict = {"Left":left, "Right":right, "Rear":rear, "Front":front} # dictionary of the adjacent verticies
        self.totalweight = 0
        self.permanent = False

class Graph():
    def __init__(self, end_label):
        self.network = []
        self.label_index = 65 # 65 in unicode is A
        self.end = end_label

    def add_vertex(self, left = [None,None], right = [None,None], rear = [None, None], front = [None, None]):
        Vert = Vertex(chr(self.label_index), left, right, rear, front)
        self.network.append(Vert)
        self.label_index += 1

    def Dijkstras(self):
        
        Queue = self.network
        Permanent = []
        dirList = ["Left", "Right", "Rear", "Front"]
        
        for i in range(1, len(self.network)): # setting up the initial values of the distance from the start node. 
            Queue[i].totalweight = math.inf   
        
        while len(Queue) > 0: # the main loop which checks  all the vertices
            
            self.bubble(Queue)
            
            current_vertex = Queue.pop(0) # similar to the dequeue in static languages
            current_vertex.permanent = True

            print("\n\n {}".format(current_vertex.label))
            for direction in dirList:
                print("{}: {}".format(direction, current_vertex.adjacencyDict[direction]))
            print(current_vertex.totalweight) 

            Permanent.append(current_vertex)

            for i in range(0,4): # iterates from 0 to 3, stops when at 4
                dirVertexLabel = current_vertex.adjacencyDict[dirList[i]][0] # finds the vertex in the direction

                try:
                    if self.find_vertex(Queue, dirVertexLabel).totalweight > current_vertex.totalweight + current_vertex.adjacencyDict[dirList[i]][1]:
                        self.find_vertex(Queue, dirVertexLabel).totalweight = current_vertex.totalweight + current_vertex.adjacencyDict[dirList[i]][1]
                except Exception as e:
                    print(e)
   
        
        # Output the final path to follow
        # For now, this will just output all the vertices with the links

        for item in Permanent:
            print("\n\n {}".format(item.label))
            for direction in dirList:
                print("{}: {}".format(direction, item.adjacencyDict[direction]))
            print(item.totalweight)             
        
    def find_vertex(self, Queue, label):
        for item in Queue:
            if item.label == label:
                return item # returns the vertex

        try:
            return Queue[len(Queue)-2]  #  returns the final value of the queue   
        except:
            print(len(Queue))
            print(label)
            for thing in Queue:
                print(thing.label)


    def bubble(self, queue):
            swaps = 1
            while swaps > 0:
                swaps = 0

                for i in range(0, len(queue)-1):
                    if queue[i].totalweight > queue[i+1].totalweight: 
                        queue[i], queue[i+1] = queue[i+1], queue[i] # swaps the two values round
                        swaps += 1

            return queue # returns the sorted version of queue

print("Start Time: {}".format(time.time()))
start = time.time()

myNetwork = Graph("D")

myNetwork.add_vertex(right=["B", 4]) # A
myNetwork.add_vertex(left=["A", 4], rear=["C", 4]) # B
myNetwork.add_vertex(front=["B", 4], right=["E", 4], rear=["D", 4]) # C
myNetwork.add_vertex(front=["C", 4]) # D
myNetwork.add_vertex(left=["C", 4]) # E

myNetwork.Dijkstras()

print("End Time: {}".format(time.time()))
print("This took {} seconds".format(time.time()-start))