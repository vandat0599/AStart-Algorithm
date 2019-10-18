import queue
from graphics import *
import math
import random

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

    def getAllNodeNeighbor(self, w, h, end):
        res = []
        neightborPoint = self.position.getAllNeighborPoint(w,h)
        for point in neightborPoint:
            node = Node(self,point)
            if abs(node.position.x - point.x) == 1 and abs(node.position.y-point.y)==1:
                node.g = self.g + 1.5
            node.g = self.g + 1
            node.h = point.manhattanDistance(end)
            node.f = node.g + node.h
            res.append(node)
        return res

class MyPoly():
    def __init__(self,points):
        self.points = list(points)
    
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
    while openNodes:
        # print("len: {}".format(len(openNodes)))
        #find the node in openNode having the lowest fScore[] value
        nodeTmp = Node()
        nodeTmp.f = math.inf
        for node in openNodes:
            # drawPoint(node.position.x,node.position.y,'cyan')
            if node.f <= nodeTmp.f:
                nodeTmp = node
        currentNode = nodeTmp
        pathResultNode.append(currentNode)

        #check goal
        # print("loop {}".format((currentNode.position.x,currentNode.position.y)))
        if currentNode.position == end:
            return reconstructPath(currentNode)
        if(currentNode in openNodes):
            openNodes.remove(currentNode)
        # openNodes.remove(currentNode)
        closeNodes.append(currentNode)
        currentNeighbor = currentNode.getAllNodeNeighbor(matrix.w,matrix.h,end)
        for node in currentNeighbor:
            if node in closeNodes:
                # print("in closeNodes {}".format((currentNode.position.x,currentNode.position.y)))
                continue
            #add conditions here: check in poly and avoid it
            if node not in openNodes:
                if not(isPointInPolyInMatrix(matrix,node.position)) and \
                (node.position.x,node.position.y) not in matrix.polyDrawedPositions:
                    print("-- ({},{})".format(node.position.x,node.position.y))
                    openNodes.append(node)
                    colors = ['royalblue','royalblue1','royalblue2','royalblue3','royalblue4']
                    drawPoint(node.position.x,node.position.y,colors[random.randint(0, 5)-1])
    print("--------------------no no no no no no path not found-------------------------")
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
            

