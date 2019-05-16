import math

class Node:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

def dist(A, B):
    return math.sqrt((A.x_pos - B.x_pos)**2 + (A.y_pos - B.y_pos)**2)

def is_not_in(A, b):
    for i in range(len(A)):
        if(A[i].x_pos == b.x_pos and A[i].y_pos == b.y_pos):
            return False
    return True

def possibilites_generator(num):
    result = []
    for i in range(num):
        result.append(i)
    return result


def greedy(A, start):
    posibilities = possibilites_generator(len(A))
    path = []
    current = start
    while(len(path) < len(A)):
        shortest = 1000000
        shortest_i = 0
        for i in range(len(posibilities)):
            if(current != i and A[posibilities[i]] != -1 and dist(A[current],A[posibilities[i]]) < shortest):
                shortest = dist(A[current],A[i])
                shortest_i = i
        path.append(shortest_i)
        current = shortest_i
        posibilities[shortest_i] = -1
    for i in range(len(posibilities)):
        if(posibilities[i] != -1):
            path[len(path)-1] = posibilities[i]
    print(posibilities)
    return path

def dummy(A, b):
    for a in range(len(A)):
        print(A[a].x_pos)

p1 = Node(4,5)

p2 = Node(7,6)
p3 = Node(7,7)
p4 = Node(10,10)

p = [p1,p2,p3,p4]

print(greedy(p,0))