from graphics import*
import time
winWidth = 700
winHeight = 700
win = GraphWin("DDDPRO", winWidth, winHeight)


def drawFirstWin(matrix):
    # draw grid
    win.setCoords(0, 0, matrix.w, matrix.h)
    rectangle = Rectangle(Point(0, 0), Point(matrix.w, matrix.h))
    rectangle.setFill("white")
    rectangle.draw(win)
    for i in range(0, matrix.w):
        Line(Point(0, i), Point(matrix.w, i)).draw(win)
    for x in range(0, matrix.h):
        Line(Point(x, 0), Point(x, matrix.h)).draw(win)


def drawPoint(x, y, color):
    square = Rectangle(Point(x, y), Point(x+1, y+1))
    square.draw(win)
    square.setFill(color)


class MyPoint():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def getAllNeighborPoint(self, w, h):
        res = []
        if self.y-1 >= 0:
            res.append(MyPoint(self.x, self.y-1))
        if self.y+1 < h:
            res.append(MyPoint(self.x, self.y+1))
        if self.x-1 >= 0:
            res.append(MyPoint(self.x-1, self.y))
        if self.x+1 < w:
            res.append(MyPoint(self.x+1, self.y))
        if self.x-1 >= 0 and self.y-1 > 0:
            res.append(MyPoint(self.x-1, self.y-1))
        if self.x+1 < w and self.y+1 < h:
            res.append(MyPoint(self.x+1, self.y+1))
        if self.x-1 >= 0 and self.y+1 < h:
            res.append(MyPoint(self.x-1, self.y+1))
        if self.x+1 < w and self.y-1 > 0:
            res.append(MyPoint(self.x+1, self.y-1))
        return res


class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

    def __eq__(self, other):
        return self.position == other.position

    def getAllNodeNeighbor(self, w, h, end):
        res = []
        neightborPoint = self.position.getAllNeighborPoint(w, h)
        for point in neightborPoint:
            node = Node(self.position, point)
            res.append(node)
        return res


class Matrix():
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.polyInside = []

    def addPolyInside(self, poly):
        self.polyInside.append(poly)

    def getAllPolyInside(self):
        return self.polyInside


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
            return path
        # We check if the current node is already in the visited nodes set in order not to recheck it
        elif vertex not in visited:
            # enumerate all adjacent nodes, construct a new path and push it into the queue
            for current_neighbour in vertex.getAllNodeNeighbor(matrix.w, matrix.h, None):
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


def main():
    matrix = Matrix(22, 22)
    start = MyPoint(1, 1)
    end = MyPoint(10, 20)
    drawFirstWin(matrix)
    drawPoint(start.x, start.y, 'red')
    drawPoint(end.x, end.y, 'red')
    Bfs = bfs(matrix, start, end)
    for i in Bfs:
        drawPoint(i.position.x, i.position.y, 'blue')
        time.sleep(0.2)
    drawPoint(start.x, start.y, 'red')
    drawPoint(end.x, end.y, 'red')
    win.getMouse()
    win.close()


main()
