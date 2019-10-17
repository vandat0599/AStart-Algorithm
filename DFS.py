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
    square = Rectangle(Point(x,y), Point(x+1,y+1))
    square.draw(win)
    square.setFill(color)

class MyPoint():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self,other):
        return self.x == other.x and self.y == other.y

    def manhattanDistance(self,other):
        return abs(self.x - other.x) + abs(self.y - other.y)

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
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def getAllNodeNeighbor(self, w, h):
        res = []
        neightborPoint = self.position.getAllNeighborPoint(w,h)
        for point in neightborPoint:
            node = Node(self.position,point)
            
            res.append(node)
        return res

class MyPoly():
    def __init__(self,points):
        self.points = points
    
    def getDrawPoints(self):
        res = self.points.copy()
        res.append(res[0])
        return res
    
    def checkPointInSide(self,point):
        isInside = False
        minX = minY = math.inf
        maxX = maxY = -math.inf
        for p in self.points:
            if minX > p[0]:
                minX = p[0]
            if maxX < p[0]:
                maxX = p[0]
            if minY > p[1]:
                minY = p[1]
            if maxY < p[1]:
                maxY = p[1]
        if point.x>=minX and point.x<=maxX and point.y>=minY and point.y<=maxY:
            intersectCount = 0
            if True:
                return True
        # print("minx: {} maxx: {}".format(minY,maxY))
        return False

class Matrix():
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.polyInside = []

    def addPolyInside(self,poly):
        self.polyInside.append(poly)
    
    def getAllPolyInside(self):
        return self.polyInside


def pathWithPickupPoint(matrix,start,end,pickupPoint):
    points = []
    points.append(start)
    for pickup in pickupPoint:
        points.append(MyPoint(pickup[0],pickup[1]))
    points.append(end)
    result = []
    for index in range(0,len(points)-1):
        result += aStar(matrix,points[index],points[index+1])
    return result

def getYInLine(p1,p2,x):
    if p2.x-p1.x==0:
        return -1
    return int(((p2.y-p1.y)*x-(p2.y-p1.y)*p1.x+(p2.x-p1.x)*p1.y)/(p2.x-p1.x))

def getXInLine(p1,p2,y):
    if p2.y-p1.y==0:
        return -1
    return int(((p2.y-p1.y)*p1.x+(p2.x-p1.x)*y-(p2.x-p1.x)*p1.y)/(p2.y-p1.y))

def drawPoly(poly):
    pointPoly = poly.getDrawPoints()
    for index in range(0,len(pointPoly)-1):
        minX = pointPoly[index][0] if pointPoly[index][0] < pointPoly[index+1][0] else pointPoly[index+1][0]
        maxX = pointPoly[index][0] if pointPoly[index][0] > pointPoly[index+1][0] else pointPoly[index+1][0]
        for i in range(minX,maxX+1):
            y = getYInLine(MyPoint(pointPoly[index][0],pointPoly[index][1]),MyPoint(pointPoly[index+1][0],pointPoly[index+1][1]),i)
            if y!=-1:
                drawPoint(i,y,'khaki')

    for index in range(0,len(pointPoly)-1):
        minY = pointPoly[index][1] if pointPoly[index][1] < pointPoly[index+1][1] else pointPoly[index+1][1]
        maxY = pointPoly[index][1] if pointPoly[index][1] > pointPoly[index+1][1] else pointPoly[index+1][1]
        for i in range(minY,maxY+1):
            x = getXInLine(MyPoint(pointPoly[index][0],pointPoly[index][1]),MyPoint(pointPoly[index+1][0],pointPoly[index+1][1]),i)
            if x!=-1:
                drawPoint(x,i,'khaki')
    for point in pointPoly:
        drawPoint(point[0],point[1],'darkkhaki')


#đây này nhé bạn yêu <3 
def dfs_paths(matrix, start, end):
    stack = [start]
    visited = []
    path = []
    while stack:
        n = len(stack)-1
        vertex = stack[n]
        path.append(stack[n])
        stack.remove(stack[n])
        if vertex not in visited:
            if vertex == end:
                return path
            visited.append(vertex)
            for neighbor in vertex.getAllNodeNeighbor(matrix.w,matrix.h):
                if neighbor not in stack:
                    stack.append(neighbor)


def main():
    pointStart = MyPoint(3,3)
    pointEnd = MyPoint(18,18)
    startNode = Node(None, pointStart)
    endNode = Node(None, pointEnd)
    matrix = Matrix(22,22)
    drawFirstWin(matrix)
    visited = []
    path = []
    drawPoint(startNode.position.x, startNode.position.y,'green')
    drawPoint(endNode.position.x, endNode.position.y,'green')
    path = dfs_paths(matrix,startNode,endNode)
    for i in path:
        drawPoint(i.position.x, i.position.y, 'red')
    drawPoint(pointStart.x,pointStart.y, 'green')
    drawPoint(pointEnd.x,pointEnd.y,'green')
    win.getMouse()
    win.close()
    print(visited)

main()            

