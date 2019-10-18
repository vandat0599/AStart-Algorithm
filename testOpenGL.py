from graphics import *

win = GraphWin("Gameboard", 700, 700)
w = 30
h = 30
win.setCoords(0, 0, w, h)

def drawBoard(window):
    rectangle = Rectangle(Point(0, 0), Point(w, h))
    rectangle.setFill("white")
    rectangle.draw(window)

    for i in range(0, w):
        Line(Point(0, i), Point(w, i)).draw(window)
    for x in range(0, h):
        Line(Point(x, 0), Point(x, h)).draw(window)
    square = Rectangle(Point(5,5), Point(6,6))
    square.draw(window)
    square.setFill('red')
    square = Rectangle(Point(0,0), Point(1,1))
    square.draw(window)
    square.setFill('blue')
    

drawBoard(win)
win.getMouse()
win.close()