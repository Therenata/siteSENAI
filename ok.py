import turtle
import math
import time

def draw_heart():
    screen = turtle.Screen()
    screen.bgcolor("white")
    screen.title("Animação de Coração")

    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("red")

    def heart_function(t):
        x = 16 * math.sin(t)**3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        return x, y

    pen.penup()
    for t in range(0, 360):
        x, y = heart_function(math.radians(t))
        pen.goto(x * 10, y * 10)
        pen.pendown()

    pen.penup()
    pen.hideturtle()

    time.sleep(5)
    screen.bye()

if __name__ == "__main__":
    draw_heart()