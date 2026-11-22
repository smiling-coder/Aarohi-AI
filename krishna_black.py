import turtle
import math
import random

# ---------- Setup (black screen, like the video) ----------
screen = turtle.Screen()
screen.setup(800, 870)
screen.setworldcoordinates(-400, -400, 400, 470)
screen.bgcolor("black")
screen.title("Lord Krishna - Python Turtle")
screen.tracer(6, 0)          # bigger number = faster drawing

t = turtle.Turtle()
t.hideturtle()
t.speed(0)

BG = "black"
SKIN = "#4fc3f7"      # glowing blue outline
GOLD = "#ffc107"
PINK = "#ff6f91"
RED = "#ff5252"
GREEN = "#26d98a"
HAIR = "#b39ddb"
WHITE = "#f5f5f5"
BROWN = "#c0654a"


# ---------- Helpers ----------
def goto(x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()


def polygon(points, color, width=2, solid=True):
    """Outline in colour; filled with black so front parts hide back parts."""
    t.pencolor(color)
    t.pensize(width)
    goto(*points[0])
    if solid:
        t.fillcolor(BG)
        t.begin_fill()
    for p in points[1:]:
        t.goto(p)
    t.goto(points[0])
    if solid:
        t.end_fill()


def line(points, color, width=2):
    t.pencolor(color)
    t.pensize(width)
    goto(*points[0])
    for p in points[1:]:
        t.goto(p)


def bezier(p0, p1, p2, p3, color, width=2, steps=40):
    t.pencolor(color)
    t.pensize(width)
    goto(*p0)
    for i in range(1, steps + 1):
        u = i / steps
        x = ((1 - u) ** 3 * p0[0] + 3 * (1 - u) ** 2 * u * p1[0]
             + 3 * (1 - u) * u ** 2 * p2[0] + u ** 3 * p3[0])
        y = ((1 - u) ** 3 * p0[1] + 3 * (1 - u) ** 2 * u * p1[1]
             + 3 * (1 - u) * u ** 2 * p2[1] + u ** 3 * p3[1])
        t.goto(x, y)


def ellipse(cx, cy, rx, ry, color, width=2, solid=True, a0=0, a1=360):
    pts = [(cx + rx * math.cos(math.radians(a)),
            cy + ry * math.sin(math.radians(a))) for a in range(a0, a1 + 1, 6)]
    if solid and (a1 - a0) == 360:
        polygon(pts, color, width, True)
    else:
        line(pts, color, width)


def dot(x, y, r, color, solid=True):
    ellipse(x, y, r, r, color, 1, solid)
    if solid:
        t.pencolor(color)
        goto(x, y)
        t.dot(max(2, r * 1.2), color)


# ---------- Background: stars + halo ----------
def draw_stars():
    random.seed(7)
    for _ in range(70):
        x = random.randint(-390, 390)
        y = random.randint(-380, 460)
        if abs(x) < 170 and -300 < y < 440:
            continue
        goto(x, y)
        t.dot(random.choice([2, 2, 3]), random.choice(["#ffffff", "#ffe082", "#b3e5fc"]))


def draw_halo():
    # glowing ring + rays behind the head
    for r, c, w in [(150, "#7a5c00", 5), (140, GOLD, 2)]:
        ellipse(0, 170, r, r, c, w, solid=False)
    for a in range(0, 360, 15):
        x1 = 0 + 150 * math.cos(math.radians(a))
        y1 = 170 + 150 * math.sin(math.radians(a))
        x2 = 0 + 172 * math.cos(math.radians(a))
        y2 = 170 + 172 * math.sin(math.radians(a))
        line([(x1, y1), (x2, y2)], GOLD, 2)


# ---------- Blossom tree (same idea as the video) ----------
def tree(i):
    if i < 10:
        return
    t.pensize(max(1, i / 25))
    t.pencolor(BROWN)
    t.forward(i)
    t.pencolor(PINK)
    t.circle(2)
    t.pencolor(BROWN)
    t.left(20)
    tree(4 * i / 5)
    t.right(40)
    tree(4 * i / 5)
    t.left(20)
    t.pencolor(BROWN)
    t.backward(i)


def draw_trees():
    for x, y, size in [(-275, -330, 44), (275, -330, 44)]:
        goto(x, y)
        t.setheading(90)
        tree(size)


# ---------- Krishna (line art) ----------
def draw_hair_back():
    ellipse(0, 185, 84, 88, HAIR, 2)
    ellipse(-78, 120, 14, 50, HAIR, 2)
    ellipse(78, 120, 14, 50, HAIR, 2)
    # hair strands
    for k in range(-3, 4):
        bezier((k * 22, 262), (k * 26, 230), (k * 30, 200), (k * 34, 170), HAIR, 1)


def draw_body():
    polygon([(-22, 100), (22, 100), (24, 60), (-24, 60)], SKIN, 2)
    polygon([(-28, 72), (-115, 45), (-130, -70), (130, -70), (115, 45), (28, 72)], SKIN, 2)
    # dhoti
    polygon([(-130, -60), (130, -60), (160, -300), (-160, -300)], GOLD, 2)
    for x in (-90, -45, 0, 45, 90):
        bezier((x * 0.85, -62), (x * 1.0, -140), (x * 1.1, -220), (x * 1.2, -298), GOLD, 1)
    # waist band
    polygon([(-130, -45), (130, -45), (130, -68), (-130, -68)], RED, 2)
    for x in range(-110, 111, 22):
        goto(x, -56)
        t.dot(5, GOLD)


def draw_garland():
    bezier((-72, 62), (-65, -25), (65, -25), (72, 62), PINK, 3)
    bezier((-62, 60), (-55, -10), (55, -10), (62, 60), GOLD, 2)
    for x, y in [(-50, 8), (-30, -8), (0, -13), (30, -8), (50, 8)]:
        ellipse(x, y, 7, 7, PINK, 2)
        goto(x, y)
        t.dot(3, PINK)
    ellipse(0, -22, 9, 9, GOLD, 2)
    goto(0, -22)
    t.dot(5, RED)


def draw_arms():
    # outline trick: wide coloured line, then slightly thinner black line on top
    for path in ([(105, 38), (158, -15), (135, 82)],
                 [(-105, 38), (-40, -45), (80, 90)]):
        line(path, SKIN, 30)
        line(path, BG, 26)
    for p in [(150, -5), (-70, -22)]:
        goto(*p)
        t.dot(8, GOLD)


def draw_face():
    ellipse(-69, 150, 10, 20, SKIN, 2)
    ellipse(69, 150, 10, 20, SKIN, 2)
    ellipse(-69, 124, 7, 7, GOLD, 2)
    ellipse(69, 124, 7, 7, GOLD, 2)
    ellipse(0, 148, 66, 82, SKIN, 3)
    # fringe
    polygon([(-64, 190), (-40, 220), (0, 226), (40, 220), (64, 190),
             (30, 205), (0, 210), (-30, 205)], HAIR, 2)


def draw_features():
    for x in (-28, 28):
        ellipse(x, 160, 17, 9, WHITE, 2)
        goto(x, 160)
        t.dot(11, SKIN)
        goto(x + 2, 162)
        t.dot(4, WHITE)
    bezier((-48, 178), (-36, 188), (-20, 188), (-10, 178), WHITE, 3)
    bezier((48, 178), (36, 188), (20, 188), (10, 178), WHITE, 3)
    bezier((0, 150), (-6, 135), (-6, 128), (0, 126), SKIN, 2)
    bezier((-20, 108), (-10, 94), (10, 94), (20, 108), RED, 3)
    line([(0, 183), (0, 212)], RED, 5)
    bezier((-9, 205), (-9, 188), (9, 188), (9, 205), WHITE, 2)


def draw_crown():
    polygon([(-52, 222), (-64, 288), (-32, 262), (0, 308), (32, 262), (64, 288), (52, 222)], GOLD, 3)
    polygon([(-52, 222), (52, 222), (52, 236), (-52, 236)], GOLD, 2)
    for x, y, c, s in [(0, 262, RED, 9), (-30, 254, GREEN, 6), (30, 254, GREEN, 6),
                       (-60, 288, RED, 6), (60, 288, RED, 6)]:
        goto(x, y)
        t.dot(s, c)


def draw_feather():
    bezier((0, 306), (10, 345), (55, 350), (62, 392), GOLD, 3)
    for k in range(9):
        u = 0.22 + k * 0.08
        x = 62 * u * u * (3 - 2 * u) * 0.9 + 4
        y = 306 + 90 * u
        line([(x, y), (x - 15, y + 9)], GREEN, 2)
        line([(x, y), (x + 15, y + 9)], GREEN, 2)
    ellipse(62, 418, 22, 34, GREEN, 2)
    ellipse(62, 414, 14, 24, "#448aff", 2)
    ellipse(62, 410, 7, 13, GOLD, 2)


def draw_flute():
    line([(10, 112), (185, 78)], "#d89a5b", 9)
    line([(10, 112), (185, 78)], BG, 5)
    for i in range(5):
        x = 70 + i * 24
        y = 112 - (x - 10) * (34 / 175)
        goto(x, y)
        t.dot(4, GOLD)
    for p in [(82, 96), (135, 86)]:
        ellipse(p[0], p[1], 13, 13, SKIN, 2)


def draw_text():
    t.penup()
    t.goto(0, -375)
    t.pencolor(GOLD)
    t.write("Jai Shri Krishna", align="center", font=("Georgia", 24, "bold italic"))


# ---------- Main ----------
draw_stars()
draw_halo()
draw_hair_back()
draw_body()
draw_garland()
draw_arms()
draw_face()
draw_features()
draw_crown()
draw_feather()
draw_flute()
draw_trees()
draw_text()

t.hideturtle()
screen.update()
screen.mainloop()
