import turtle
class Star():

    def __init__(self,size,color):
        self.size = size
        self.color = color
        

    def draw(self,x = 0,y = 0):
        t = turtle.Pen()
        t.hideturtle()
        t.speed(0)
        t.penup()
        t.goto(x,y)
        t.pendown()
        t.color(str(self.color))
        for m in range(self.size):
            t.fd(m)
            t.right(144)
            t.width(m/10)

    def clickDraw(self,bgcolor = 'white'):
        turtle.bgcolor(bgcolor)
        turtle.onscreenclick(self.draw)
