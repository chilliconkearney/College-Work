from random import randint

def bubble(queue):
            swaps = 1
            while swaps > 0:
                swaps = 0

                for i in range(0, len(queue)-1):
                    if queue[i].totalweight > queue[i+1].totalweight: 
                        queue[i], queue[i+1] = queue[i+1], queue[i] # swaps the two values round
                        swaps += 1

            return queue # returns the sorted version of queue


class tempObj():
    def __init__(self, weight) -> None:
        self.totalweight = weight

queue = []

for i in range(20):
    queue.append(tempObj(randint(0,20)))

print("unsorted list:")

for item in queue:
    print(item.totalweight)

queue = bubble(queue)

print("\n sorted list:")

for item in queue:
    print(item.totalweight)