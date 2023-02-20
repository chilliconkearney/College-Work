import math

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


myNetwork = Graph("E")
myNetwork.add_vertex(right=["B", 4])
myNetwork.add_vertex(left=["A", 4], front=["C", 4])
myNetwork.add_vertex(right=["E", 4], rear=["B", 4], front=["D", 4])
myNetwork.add_vertex(rear=["D", 4])
myNetwork.add_vertex(left=["C", 4])

myNetwork.Dijkstras()

print("reached the end")