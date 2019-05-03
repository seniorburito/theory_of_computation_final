import math

class Node:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

def dist(A, B):
    return math.sqrt((A.x_pos - B.x_pos)**2 + (A.y_pos - B.y_pos)**2)

def greedy(A, start):
    current = A[start]
    path = []
    while(len(A)>1):
        #find the closest node
        shortest = dist(current,A[0])
        shortest_index = 0
        for i in range(len(A)):
            if(dist(current,A[i]) < shortest and dist(current,A[i]) > 0):
                shortest = dist(current,A[i])
                shortest_index = i
        #move to the closest node
        path.append(current)
        print(current.x_pos)
        previous = current
        current = A[shortest_index]
        A.remove(previous)
        #remove the previous node from the list 
        #repeat
    path.append(A[0])
    return path

def dummy(A, b):
    for a in range(len(A)):
        print(A[a].x_pos)

p1 = Node(4,5)

p2 = Node(7,6)
p3 = Node(7,7)

p = [p1,p2,p3]
print(greedy(p,0))