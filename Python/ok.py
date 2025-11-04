import turtle
import math
import time

def draw_heart(pen, scale=1, offset=(0, 0)):
    def heart_function(t):
        x = 16 * math.sin(t)**3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        return x * scale + offset[0], y * scale + offset[1]

    pen.penup()
    for t in range(0, 360):
        x, y = heart_function(math.radians(t))
        pen.goto(x * 10, y * 10)
        pen.pendown()
    pen.penup()

def draw_scene():
    screen = turtle.Screen()
    screen.bgcolor("white")
    screen.title("Animação de Coração")

    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("red")

    offsets = [(-200, 200), (200, 200), (-200, -200), (200, -200), (0, 300), (0, -300)]

    for _ in range(10):  # Fazer o coração "bater" 10 vezes
        pen.clear()

        # Desenhar coração principal (batendo)
        pen.begin_fill()
        draw_heart(pen, scale=1.2)  # Coração maior
        pen.end_fill()
        time.sleep(0.2)

        pen.clear()
        pen.begin_fill()
        draw_heart(pen, scale=1)  # Coração menor
        pen.end_fill()
        time.sleep(0.2)

        # Desenhar outros corações ao redor
        for offset in offsets:
            pen.color("pink")
            pen.begin_fill()
            draw_heart(pen, scale=0.5, offset=offset)
            pen.end_fill()

    pen.hideturtle()
    screen.bye()

if __name__ == "__main__":
    draw_scene()