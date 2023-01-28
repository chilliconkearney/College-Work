import math

class Vertex():
    def __init__(self, label):
        self.label = str(label)
        # left, right, rear, front
        self.adjacencyLabels = ["","","",""] # dictionary of the adjacent verticies
        self.adjacencyWeights = [math.inf, math.inf, math.inf, math.inf] # has all the connected arc weights set to infinity
        self.totalweight = math.inf
        self.permanent = False

    def update_adjacency(self, input = [[],[],[],[]]):
        for i in range(0,4):
            try:
                if type(input[0][0]),type(input[0][1]) == str,float:
                    pass
        
        
        
        
        if type(left[0]) == str and type(left[1]) == float: # Left
            self.adjacencyLabels[0] = left[0]
            self.adjacencyWeights[0] = left[1]
        
        if type(left[0]) == str and type(left[1]) == float: # Right
            self.adjacencyLabels[1] = right[0]
            self.adjacencyWeights[1] = right[1]
        
        if type(left[0]) == str and type(left[1]) == float: # Rear
            self.adjacencyLabels[1] = rear[0]
            self.adjacencyWeights[1] = rear[1]
        
        if type(left[0]) == str and type(left[1]) == float: # Front
            self.adjacencyLabels[1] = front[0]
            self.adjacencyWeights[1] = front[1]
            
        


class Graph():
    def __init__(self, end_label):
        self.network = []
        self.label_index = 65 # 65 in unicode is A
        self.end = end_label

    def add_vertex(self, left = [], right = [], rear = [], front = []):
        Vert = Vertex(chr(self.label_index))
        try:
            self.network.append(Vert)
        self.label_index += 1


    def Dijkstras(self):
        
        Queue = self.network
        Permanent = []
        dirList = ["Left", "Right", "Rear", "Front"]
        
        Queue[0].totalweight = 0 # sets the initial vertex weight to 0
        
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

                if self.find_vertex(Queue, dirVertexLabel).totalweight > current_vertex.totalweight + current_vertex.adjacencyDict[dirList[i]][1]:
                        self.find_vertex(Queue, dirVertexLabel).totalweight = current_vertex.totalweight + current_vertex.adjacencyDict[dirList[i]][1]

   
        
        # Output the final path to follow
        # For now, this will just output all the vertices with the links

        print("WOOOOOO, YOU GOT THIS FAR!!!!")

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
            input()

    def bubble(self, queue): # sorts the vertices by weight from start
            swaps = 1
            while swaps > 0:
                swaps = 0

                for i in range(0, len(queue)-1):
                    if queue[i].totalweight > queue[i+1].totalweight: 
                        queue[i], queue[i+1] = queue[i+1], queue[i] # swaps the two values round
                        swaps += 1

            return queue # returns the sorted version of queue


Test = Vertex("T")
Test.update_adjacency(left=["A", 8.0])

input()