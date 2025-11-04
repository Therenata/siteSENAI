import turtle

t = turtle.Turtle()

# t.shapesize(0.2, 0.2)

s = turtle.Screen()

s.bgcolor('black')
t.fillcolor("red")
t.begin_fill()
t.left(50)
t.forward(120)  
t.circle(45, 200)  
t.left(221)
t.circle(45, 200)  
t.forward(130)  

t.end_fill()
turtle.done()