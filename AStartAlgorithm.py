import queue

class Point():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self,other):
        return self.x == other.x and self.y == other.y

    def manhattanDistance(self,other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def getAllNeighborPoint(self, w, h):
        res = []
        if y-1>0:
            res.append(Point(x,y-1))
        if y+1<h:
            res.append(Point(x,y+1))
        if x-1>0:
            res.append(Point(x-1,y))
        if x+1<w:
            res.append(Point(x+1,y))
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
            node.g = self.g + 1
            node.h = point.manhattanDistance(end)
            node.f = node.g + node.h
            res.append(node)
        return res


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
    while openNodes is not None:
        #find the node in openNode having the lowest fScore[] value
        for node in openNodes:
            if node.f < currentNode.f:
                currentNode = node
        pathResultNode.append(currentNode)

        #check goal
        if currentNode.position == end:
            return pathResultNode
        
        openNodes.remove(currentNode)
        closeNodes.append(currentNode)


