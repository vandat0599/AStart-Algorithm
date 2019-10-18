# from graphics import*

# winWidth = 700
# winHeight = 700
# win = GraphWin("DDDPRO", winWidth, winHeight)


# def drawFirstWin(matrix):
#     # draw grid
#     win.setCoords(0, 0, matrix.w, matrix.h)
#     rectangle = Rectangle(Point(0, 0), Point(matrix.w, matrix.h))
#     rectangle.setFill("white")
#     rectangle.draw(win)
#     for i in range(0, matrix.w):
#         Line(Point(0, i), Point(matrix.w, i)).draw(win)
#     for x in range(0, matrix.h):
#         Line(Point(x, 0), Point(x, matrix.h)).draw(win)


# def drawPoint(x, y, color):
#     square = Rectangle(Point(x, y), Point(x+1, y+1))
#     square.draw(win)
#     square.setFill(color)


# class MyPoint():
#     def __init__(self, x=0, y=0):
#         self.x = x
#         self.y = y

#     def __eq__(self, other):
#         return self.x == other.x and self.y == other.y

#     def getAllNeighborPoint(self, w, h):
#         res = []
#         if self.y-1 > 0:
#             res.append(MyPoint(self.x, self.y-1))
#         if self.y+1 < h:
#             res.append(MyPoint(self.x, self.y+1))
#         if self.x-1 > 0:
#             res.append(MyPoint(self.x-1, self.y))
#         if self.x+1 < w:
#             res.append(MyPoint(self.x+1, self.y))
#         if self.x-1 > 0 and self.y-1 > 0:
#             res.append(MyPoint(self.x-1, self.y-1))
#         if self.x+1 < w and self.y+1 < h:
#             res.append(MyPoint(self.x+1, self.y+1))
#         if self.x-1 > 0 and self.y+1 < h:
#             res.append(MyPoint(self.x-1, self.y+1))
#         if self.x+1 < w and self.y-1 > 0:
#             res.append(MyPoint(self.x+1, self.y-1))
#         return res


# class Node():
#     def __init__(self, parent=None, position=None):
#         self.parent = parent
#         self.position = position

#     def __eq__(self, other):
#         return self.position == other.position

#     def getAllNodeNeighbor(self, w, h, end):
#         res = []
#         neightborPoint = self.position.getAllNeighborPoint(w, h)
#         for point in neightborPoint:
#             node = Node(self.position, point)
#             res.append(node)
#         return res


# class Matrix():
#     def __init__(self, w, h):
#         self.w = w
#         self.h = h
#         self.polyInside = []

#     def addPolyInside(self, poly):
#         self.polyInside.append(poly)

#     def getAllPolyInside(self):
#         return self.polyInside


# def bfs(matrix, start, end):
#     node_start = Node(None, start)
#     node_end = Node(None, end)
#     queue = [node_start]
#     visited = list()
#     while queue:
#         # Gets the first path in the queue
#         path = queue.pop(0)
#         if type(path) == Node:
#             # Gets the last node in the path
#             vertex = path
#         else:
#             vertex = path[-1]
#         # Checks if we got to the end
#         #vertex = Node()
#         if node_end == vertex:
#             return path
#         # We check if the current node is already in the visited nodes set in order not to recheck it
#         elif vertex not in visited:
#             # enumerate all adjacent nodes, construct a new path and push it into the queue
#             for current_neighbour in vertex.getAllNodeNeighbor(matrix.w, matrix.h, None):
#                 if type(path) == Node:
#                     new_path = list()
#                     new_path.append(path)
#                     new_path.append(current_neighbour)
#                     queue.append(new_path)
#                 else:
#                     new_path = list(path)
#                     new_path.append(current_neighbour)
#                     queue.append(new_path)

#             # Mark the vertex as visited
#             visited.append(vertex)


# def main():
#     matrix = Matrix(22, 22)
#     start = MyPoint(0, 0)
#     end = MyPoint(10, 20)
#     drawFirstWin(matrix)
#     Bfs = bfs(matrix, start, end)
#     for i in Bfs:
#         drawPoint(i.position.x, i.position.y, 'blue')
#     win.getMouse()
#     win.close()


# main()
import queue
from graphics import *
import math

winWidth = 700
winHeight = 700
win = GraphWin("DDDPRO",winWidth,winHeight)

def drawFirstWin(matrix):
    #draw grid
    win.setCoords(0, 0, matrix.w, matrix.h)
    rectangle = Rectangle(Point(0, 0), Point(matrix.w, matrix.h))
    rectangle.setFill("white")
    rectangle.draw(win)
    for i in range(0, matrix.w):
        Line(Point(0, i), Point(matrix.w, i)).draw(win)
    for x in range(0, matrix.h):
        Line(Point(x, 0), Point(x, matrix.h)).draw(win)

def drawPoint( x, y, color):
    square = Rectangle(Point(int(x),y), Point(int(x)+1,int(y)+1))
    square.draw(win)
    square.setFill(color)

class MyPoint():
    def __init__(self, x=0, y=0):
        self.x = int(x)
        self.y = int(y)

    def __eq__(self,other):
        return self.x == other.x and self.y == other.y

    def getAllNeighborPoint(self, w, h):
        res = []
        if self.y-1>=0:
            res.append(MyPoint(self.x,self.y-1))
        if self.y+1<h:
            res.append(MyPoint(self.x,self.y+1))
        if self.x-1>=0:
            res.append(MyPoint(self.x-1,self.y))
        if self.x+1<w:
            res.append(MyPoint(self.x+1,self.y))
        if self.x-1>=0 and self.y-1>0:
            res.append(MyPoint(self.x-1,self.y-1))
        if self.x+1<w and self.y+1<h:
            res.append(MyPoint(self.x+1,self.y+1))
        if self.x-1>=0 and self.y+1<h:
            res.append(MyPoint(self.x-1,self.y+1))
        if self.x+1<w and self.y-1>0:
            res.append(MyPoint(self.x+1,self.y-1))
        return res


class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0

    def __eq__(self, other):
        return self.position == other.position

    def getAllNodeNeighbor(self, w, h):
        res = []
        neightborPoint = self.position.getAllNeighborPoint(w,h)
        for point in neightborPoint:
            node = Node(self,point)
            if abs(node.position.x - point.x) == 1 and abs(node.position.y-point.y)==1:
                node.g = self.g + 1.5
            node.g = self.g + 1
            res.append(node)
        return res

class MyPoly():
    def __init__(self,points):
        self.points = list(points)
    
    def getDrawPoints(self):
        res = self.points.copy()
        res.append(res[0])
        return res

def is_point_in_path(x, y, poly):
    """
    x, y -- x and y coordinates of point
    poly -- a list of tuples [(x, y), (x, y), ...]
    """
    num = len(poly)
    i = 0
    j = num - 1
    c = False
    for i in range(num):
        if ((poly[i][1] > y) != (poly[j][1] > y)) and \
                (x < poly[i][0] + (poly[j][0] - poly[i][0]) * (y - poly[i][1]) /
                                  (poly[j][1] - poly[i][1])):
            c = not c
        j = i
    return c

def isPointInPolyInMatrix(matrix, point):
    for m in matrix.getAllPolyInside():
        if(is_point_in_path(point.x,point.y,m.getDrawPoints())):
            return True
    return False

class Matrix():
    def __init__(self, w, h):
        self.w = int(w)
        self.h = int(h)
        self.polyDrawedPositions = set()
        self.polyInside = []

    def addPolyInside(self,poly):
        self.polyInside.append(poly)

    def addAllPolyEdgePositions(self,p):
        self.polyDrawedPositions = p
    
    def getAllPolyInside(self):
        return self.polyInside

def reconstructPath(current):
    resultPath = [current]
    while current.parent:
        current = current.parent
        resultPath.insert(0,current)
    return resultPath

def pathWithPickupPoint(matrix,start,end,pickupPoint):
    points = []
    points.append(start)
    for pickup in pickupPoint:
        points.append(MyPoint(pickup[0],pickup[1]))
    points.append(end)
    result = []
    for index in range(0,len(points)-1):
        result += bfs(matrix,points[index],points[index+1])
    return result

def getYInLine(p1,p2,x):
    if p2.x-p1.x==0:
        return -1
    return int(((p2.y-p1.y)*x-(p2.y-p1.y)*p1.x+(p2.x-p1.x)*p1.y)/(p2.x-p1.x))

def getXInLine(p1,p2,y):
    if p2.y-p1.y==0:
        return -1
    return int(((p2.y-p1.y)*p1.x+(p2.x-p1.x)*y-(p2.x-p1.x)*p1.y)/(p2.y-p1.y))

def group2List(l):
    res = []
    for i in range(0,len(l)-1,2):
        res.append((l[i],l[i+1]))
    return res

def drawPoly(poly):
    pSets = set()
    pointPoly = poly.getDrawPoints()
    for index in range(0,len(pointPoly)-1):
        minX = pointPoly[index][0] if pointPoly[index][0] < pointPoly[index+1][0] else pointPoly[index+1][0]
        maxX = pointPoly[index][0] if pointPoly[index][0] > pointPoly[index+1][0] else pointPoly[index+1][0]
        for i in range(minX,maxX+1):
            y = getYInLine(MyPoint(pointPoly[index][0],pointPoly[index][1]),MyPoint(pointPoly[index+1][0],pointPoly[index+1][1]),i)
            if y!=-1:
                drawPoint(i,y,'khaki1')
                pSets.add((i,y))

    for index in range(0,len(pointPoly)-1):
        minY = pointPoly[index][1] if pointPoly[index][1] < pointPoly[index+1][1] else pointPoly[index+1][1]
        maxY = pointPoly[index][1] if pointPoly[index][1] > pointPoly[index+1][1] else pointPoly[index+1][1]
        for i in range(minY,maxY+1):
            x = getXInLine(MyPoint(pointPoly[index][0],pointPoly[index][1]),MyPoint(pointPoly[index+1][0],pointPoly[index+1][1]),i)
            if x!=-1:
                drawPoint(x,i,'khaki1')
                pSets.add((x,i))
    for point in pointPoly:
        drawPoint(point[0],point[1],'khaki4')
    return pSets

 
# def dfs_paths(matrix, start, end):
#     startNode = Node(None, start)
#     endNode = Node(None, end)
#     stack = [startNode]
#     visited = []
#     path = []
#     while stack:
#         n = len(stack)-1
#         vertex = stack[n]
#         path.append(stack[n])
#         stack.remove(stack[n])
#         if vertex not in visited:
#             if vertex == endNode:
#                 return reconstructPath(vertex)
#             visited.append(vertex)
#             for neighbor in vertex.getAllNodeNeighbor(matrix.w,matrix.h):
#                 if neighbor not in stack:
#                      if not(isPointInPolyInMatrix(matrix,neighbor.position)) and \
#                     (neighbor.position.x,neighbor.position.y) not in matrix.polyDrawedPositions:
#                         print("-- ({},{})".format(neighbor.position.x,neighbor.position.y))
#                         stack.append(neighbor)
#                         # drawPoint(neighbor.position.x,neighbor.position.y,'royalblue')

def bfs(matrix, start, end):
    node_start = Node(None, start)
    node_end = Node(None, end)
    queue = [node_start]
    visited = list()
    while queue:
        # Gets the first path in the queue
        path = queue.pop(0)
        if type(path) == Node:
            # Gets the last node in the path
            vertex = path
        else:
            vertex = path[-1]
        # Checks if we got to the end
        #vertex = Node()
        if node_end == vertex:
            return reconstructPath(vertex)
        # We check if the current node is already in the visited nodes set in order not to recheck it
        elif vertex not in visited:

            if not(isPointInPolyInMatrix(matrix,vertex.position)) and \
                    (vertex.position.x,vertex.position.y) not in matrix.polyDrawedPositions:
                        print("-- ({},{})".format(vertex.position.x,vertex.position.y))
                        # drawPoint(neighbor.position.x,neighbor.position.y,'royalblue')
                        # enumerate all adjacent nodes, construct a new path and push it into the queue
                        for current_neighbour in vertex.getAllNodeNeighbor(matrix.w, matrix.h):
                            if type(path) == Node:
                                new_path = list()
                                new_path.append(path)
                                new_path.append(current_neighbour)
                                queue.append(new_path)
                            else:
                                new_path = list(path)
                                new_path.append(current_neighbour)
                                queue.append(new_path)

                        # Mark the vertex as visited
                        visited.append(vertex)
                        drawPoint(vertex.position.x,vertex.position.y,'royalblue')

            

def main():

    #read file
    with open("input.txt") as f:
        lineList = f.readlines()
    for i in range(0,len(lineList)):
        lineList[i] = lineList[i].rstrip()
    
    matrixWidth = lineList[0].split(',')[0]
    matrixHeight = lineList[0].split(',')[1]
    points = group2List(lineList[1].split(','))
    polyCount = int(lineList[2])
    polyArr = []
    for i in range(0,polyCount):
        polyArr.append(MyPoly(group2List([int(num) for num in lineList[3+i].split(',')])))
    #prepare data
    pointStart = MyPoint(points[0][0],points[0][1])
    pointEnd = MyPoint(points[1][0],points[1][1])
    pickupPoint = points[2:]
    matrix = Matrix(matrixWidth,matrixHeight)
    drawFirstWin(matrix)
    positionEdgeDrawed = set()
    for poly in polyArr:
        matrix.addPolyInside(poly)
        positionEdgeDrawed = positionEdgeDrawed.union(drawPoly(poly))
    matrix.addAllPolyEdgePositions(positionEdgeDrawed)

    for point in pickupPoint:
        drawPoint(point[0],point[1],'magenta2')
    drawPoint(pointStart.x,pointStart.y,'red')
    drawPoint(pointEnd.x,pointEnd.y,'red')

    resultPath = pathWithPickupPoint(matrix,pointStart, pointEnd,pickupPoint)
    for node in resultPath:
            drawPoint(node.position.x,node.position.y,'lime')
    for point in pickupPoint:
        drawPoint(point[0],point[1],'red')
    drawPoint(pointStart.x,pointStart.y,'red')
    drawPoint(pointEnd.x,pointEnd.y,'red')
    win.getMouse()
    win.close()
main()
            


