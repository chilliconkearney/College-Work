import math

class Vertex():
    def __init__(self, label, left = [None,None], right = [None,None], rear = [None, None], front = [None, None]): # lists stored as [label, weight]
        self.label = str(label)
        self.adjacencyDict = {"Left":left, "Right":right, "Rear":rear, "Front":front} # dictionary of the adjacent verticies
        self.totalweight = 0


class Graph():
    def __init__(self, end_label):
        self.network = []
        self.label_index = 0
        self.end = end_label

    def add_vertex(self, left, right, rear, front):
        Vert = Vertex(chr(self.label_index), left, right, rear, front)
        self.network.append(Vert)


    def Dijkstras(self):
        
        Queue = self.network
        Visited = []
        
        for i in range(1, len(self.network)): # setting up the initial values of the distance from the start node. 
            Queue[i].totalweight = math.inf   
        
        def bubble(queue):
            swaps = 1
            while swaps > 0:
                swaps = 0

                for i in range(0, len(queue)-1):
                    if queue[i].totalweight > queue[i+1].totalweight: 
                        queue[i], queue[i+1] = queue[i+1], queue[i] # swaps the two values round
                        swaps += 1

            return queue # returns the sorted version of queue