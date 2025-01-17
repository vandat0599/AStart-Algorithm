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
        if self.y-1>0:
            res.append(MyPoint(self.x,self.y-1))
        if self.y+1<h:
            res.append(MyPoint(self.x,self.y+1))
        if self.x-1>0:
            res.append(MyPoint(self.x-1,self.y))
        if self.x+1<w:
            res.append(MyPoint(self.x+1,self.y))
        if self.x-1>0 and self.y-1>0:
            res.append(MyPoint(self.x-1,self.y-1))
        if self.x+1<w and self.y+1<h:
            res.append(MyPoint(self.x+1,self.y+1))
        if self.x-1>0 and self.y+1<h:
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

    def getAllNodeNeighbor(self, w, h, end):
        res = []
        neightborPoint = self.position.getAllNeighborPoint(w,h)
        for point in neightborPoint:
            node = Node(self.position,point)
            if abs(node.position.x - point.x) == 1 and abs(node.position.y-point.y)==1:
                node.g = self.g + 1.5
            node.g = self.g + 1
            node.h = point.manhattanDistance(end)
            node.f = node.g + node.h
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

def aStar(matrix, start, end):
    nodeStart = Node(None,start)
    nodeEnd = Node(None, end)
    nodeStart.g = 0
    nodeStart.h = nodeStart.position.manhattanDistance(nodeEnd.position)
    nodeStart.f = nodeStart.g + nodeStart.h
    openNodes = [nodeStart]
    currentNode = nodeStart
    pathResultNode = []
    closeNodes = []
    while len(openNodes)>0:
        #find the node in openNode having the lowest fScore[] value
        for node in openNodes:
            # drawPoint(node.position.x,node.position.y,'cyan')
            if node.f <= currentNode.f:
                currentNode = node
        pathResultNode.append(currentNode)

        #check goal
        if currentNode.position == end:
            return pathResultNode
        
        openNodes.remove(currentNode)
        closeNodes.append(currentNode)

        currentNeighbor = currentNode.getAllNodeNeighbor(matrix.w,matrix.h,end)
        for node in currentNeighbor:
            if node in closeNodes:
                continue
            
            #add conditions here: check in poly and avoid it
            if node not in openNodes:
                print("-- ({},{})".format(node.position.x,node.position.y))
                openNodes.append(node)
                drawPoint(node.position.x,node.position.y,'royalblue')
    print("no no no no no no")
    return []

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

def main():
    pointStart = MyPoint(2,2)
    pointEnd = MyPoint(19,16)
    # pickupPoint = [(15,20),(20,30),(25,60),(35,50),(45,79)]
    pickupPoint = []
    matrix = Matrix(22,22)
    drawFirstWin(matrix)

    # draw poly
    poly1 = MyPoly([(8,12),(8,17),(13,12)])
    poly2 = MyPoly([(4,4),(5,9),(8,10),(9,5)])
    poly3 = MyPoly([(11,1),(11,6),(14,6),(14,1)])
    poly1.checkPointInSide(MyPoint())
    drawPoly(poly1)
    drawPoly(poly2)
    drawPoly(poly3)
    matrix.addPolyInside(poly1)
    matrix.addPolyInside(poly2)
    matrix.addPolyInside(poly3)

    for point in pickupPoint:
        drawPoint(point[0],point[1],'red')
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
            

