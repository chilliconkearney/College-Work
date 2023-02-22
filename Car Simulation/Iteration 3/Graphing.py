class math: # allows me add math functions to a class, and easily replace math.inf
    inf = float("inf")

class Vertex():
    def __init__(self, label):
        self.label = str(label)
        # North, East, South, West
        self.adjacencyLabels = ["","","",""] # dictionary of the adjacent verticies
        self.adjacencyWeights = [math.inf, math.inf, math.inf, math.inf] # has all the connected arc weights set to infinity
        self.adjacencyPot = [False,False,False,False] # currently, no directions are possible
        self.totalweight = math.inf
        self.permanent = False
        self.previousVertex = ""
        self.previousDir = 0

    def update_adjacency(self, input = [[],[],[],[]]):
        for i in range(0,4):
            try:
                if len(input[i]) == 2:
                    self.adjacencyLabels[i] = str(input[i][0])
                    self.adjacencyWeights[i] = int(input[i][1])
            except:
                print("one of your values isn't the correct type")

    def __call__(self):
        properties = []

        properties.append(self.label)
        for i in range(len(self.adjacencyLabels)):
            properties.append("{},{}".format(self.adjacencyLabels[i], self.adjacencyWeights[i]))

        return properties
    
    def build():
        pass
            
class Graph():
    def __init__(self, end_label, screen):
        self.network = []
        self.label_index = 65 # 65 in unicode is A, works as an offset
        self.end = end_label
        self.nullVertex = Vertex("*")
        self.finalPath = ""
        self.finalLength = math.inf
        self.Permanent = []
        self.screen = screen
        

    def __call__(self):
        properties = []

        for item in self.network:
            properties.append(item())

        properties.append("{};{}".format(self.end, self.label_index))

        properties.append("{};{}".format(self.finalPath, self.finalLength))

        return properties

    def add_vertex(self, direction, distance, possibleDirs):
        
        if self.find_vertex(self.network, self.label_index).label == "*":
            Vert = Vertex(chr(self.label_index))
            
            if chr(self.label_index) == "A": # if the vertex is the initial vertex
                Vert.adjacencyPot[0] = True
        
            else: # if the vertex is any other vertex in the maze
                
                # updating the previous vertex
                previous_vertex = self.find_vertex(self.network, chr(self.label_index - 1))
                adjacency = [[],[],[],[]]
                adjacency[direction%4] = [chr(self.label_index),distance]
                previous_vertex.update_adjacency(adjacency)

                # updating the new vertex
                prev_label = chr(self.label_index - 1)
                adjacency = [[],[],[],[]]
                prev_dir = (direction+2)%4 # calculates the direction that the link should be made
                adjacency[prev_dir] = [prev_label,distance]
                Vert.update_adjacency(adjacency)
            
                Vert.adjacencyPot = possibleDirs

            self.network.append(Vert)
        self.label_index += 1 # increments the label by 1 e.g A -> B

    def Dijkstras(self):
        
        self.fixGraph()
        self.screen.print("Graph Fixed")

        Queue = []
        for item in self.network:
            Queue.append(item)
        
        
        Queue[0].totalweight = 0 # sets the initial vertex weight to 0
        end_vertex = self.find_vertex(Queue, self.end)

        while end_vertex in Queue: # the main loop which checks all the vertices
            
            self.screen.print("Doing Dijkstra's")
            
            self.bubble(Queue) # sorts the queue
            
            current_vertex = Queue.pop(0) # similar to the dequeue in static languages
            current_vertex.permanent = True

            self.Permanent.append(current_vertex)

            for i in range(0,4): # iterates from 0 to 3, stops when at 4
                dirVertex = self.find_vertex(Queue,current_vertex.adjacencyLabels[i]) # finds the vertex in the direction

                if dirVertex.totalweight > current_vertex.totalweight + current_vertex.adjacencyWeights[i]:
                        dirVertex.totalweight = current_vertex.totalweight + current_vertex.adjacencyWeights[i]
                        dirVertex.previousVertex = current_vertex.label
                        dirVertex.previousDir = i

        # Output the final path to follow
        self.finalPath = self.findPath(self.Permanent, self.end)
        return self.finalPath

    def findPath(self, final_list, curlabel, output = ""): # traces the path back to the start
        dirList = ["Left", "Right", "Rear", "Front"]
        curVertex = self.find_vertex(final_list, curlabel)
        output += "{},{},{}".format(curVertex.label, curVertex.totalweight, dirList[curVertex.previousDir])
        if curVertex.label == "A":
            return output
        else:
            return self.findPath(final_list, curVertex.previousVertex, output)

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
    
    def fixGraph(self): # fixes the graph so that vertices are not 'hopped' over
        for vert_i in self.network:
            for vert_j in self.network:
                for i in range(0,4):
                    if vert_i.label != vert_j.label and vert_i.adjacencyLabels[i] == vert_j.adjacencyLabels[i] and len(vert_j.adjacencyLabels[i])>0:
                        self.screen.print("Changing Layout")
                        
                        if vert_i.adjacencyWeights[i] > vert_j.adjacencyWeights[i]:
                            firstVert = vert_i
                            secondVert = vert_j
                            thirdVert = self.find_vertex(self.network, firstVert.adjacencyLabels[i])
                        
                        elif vert_i.adjacencyWeights[i] > vert_j.adjacencyWeights[i]:
                            firstVert = vert_j
                            secondVert = vert_i
                            thirdVert = self.find_vertex(self.network, firstVert.adjacencyLabels[i])

                        firstVert.adjacencyLabels[i] = secondVert.label
                        firstVert.adjacencyWeights[i] = firstVert.adjacencyWeights[i] - secondVert.adjacencyWeights[i]

                        secondVert.adjacencyLabels[(i+2)%4] = firstVert.label
                        secondVert.adjacencyLabels[(i+2)%4] = firstVert.adjacencyWeights[i]

                        thirdVert.adjacencyLabels[(i+2)%4] = secondVert.label
                        thirdVert.adjacencyWeights[(i+2)%4] = secondVert.adjacencyWeights[i]