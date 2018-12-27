from tkinter import *
import random

red = "#EA0A0A"
light_blue = "#3399ff"
yellow = "#ffff00"
light_green = "#99ff99"
aqua = "#00ffff"

WIDTH = 900
HEIGHT = 300

PAD_W = 10
PAD_H = 100

PAD_SPEED = 5
LEFT_PAD_SPEED = 0
RIGHT_PAD_SPEED = 0

BALL_SPEED_UP = 1
BALL_MAX_SPEED = 30
BALL_X_SPEED = 15
BALL_Y_SPEED = 15

right_edge_distance = WIDTH - PAD_W

PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

INITIAL_SPEED = 10

BALL_RADIUS = 30

root = Tk()
root.title("Пинг-понг")

c = Canvas(root, width=WIDTH, height=HEIGHT, background=light_green)
c.pack()

c.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT, fill="black")

BALL = c.create_oval(WIDTH/2-BALL_RADIUS/2, HEIGHT/2-BALL_RADIUS/2, WIDTH/2+BALL_RADIUS/2, HEIGHT/2+BALL_RADIUS/2, fill="#FFFFFF")

player_1_text = c.create_text(WIDTH - WIDTH/6,
                              PAD_H/4,
                              text=PLAYER_1_SCORE,
                              font="Arial 20",
                              fill=light_blue)
player_2_text = c.create_text(WIDTH/6,
                              PAD_H/4,
                              text=PLAYER_2_SCORE,
                              font="Arial 20",
                              fill=light_blue)

LEFT_PAD = c.create_line(PAD_W/2+2, 0, PAD_W/2+2, PAD_H, width=20, fill=red)
RIGHT_PAD = c.create_line(WIDTH-PAD_W/2, 0, WIDTH-PAD_W/2, PAD_H, width=20, fill=red)

def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == 'right':
        PLAYER_1_SCORE = PLAYER_1_SCORE + 1
        c.itemconfig(player_1_text,
                     text=PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE = PLAYER_2_SCORE + 1
        c.itemconfig(player_2_text,
                     text=PLAYER_2_SCORE)

def spawn_ball():
    global BALL_X_SPEED
    c.coords(BALL, WIDTH/2-BALL_RADIUS/2,
             HEIGHT/2-BALL_RADIUS/2,
             WIDTH/2+BALL_RADIUS/2,
             HEIGHT/2+BALL_RADIUS/2)
    BALL_X_SPEED = -(BALL_X_SPEED * (-INITIAL_SPEED))/abs(BALL_X_SPEED)

def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    if action == 'strike':
        BALL_Y_SPEED = random.randrange(-10, 10)
        if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
            BALL_X_SPEED *= -BALL_SPEED_UP
        else:
            BALL_X_SPEED = -BALL_X_SPEED
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED

def move_pads():
    PADS = {LEFT_PAD: LEFT_PAD_SPEED,
            RIGHT_PAD: RIGHT_PAD_SPEED}

    for pad in PADS:
        c.move(pad, 0, PADS[pad])
        if c.coords(pad)[1] < 0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > HEIGHT:
            c.move(pad, 0, HEIGHT - c.coords(pad)[3])

c.focus_set()

def move_event_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym == 'w':
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == 's':
        LEFT_PAD_SPEED = PAD_SPEED
    elif event.keysym == 'Up':
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == 'Down':
        RIGHT_PAD_SPEED = PAD_SPEED

c.bind("<KeyPress>", move_event_handler)

def stop_pad(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym in 'ws':
        LEFT_PAD_SPEED = 0
    elif event.keysym in ('Up', 'Down'):
        RIGHT_PAD_SPEED = 0

c.bind("<KeyRelease>", stop_pad)

def move_ball():
    ball_left, ball_top, ball_right, ball_bottom = c.coords(BALL)
    ball_center = (ball_top + ball_bottom) / 2

    if ball_right + BALL_X_SPEED < right_edge_distance and ball_left + BALL_X_SPEED > PAD_W:
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
    elif ball_right == right_edge_distance or ball_left == PAD_W:
        if ball_right > WIDTH/2:
            if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]:
                bounce('strike')
            else:
                update_score('left')
                spawn_ball()
        else:
            if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]:
                bounce('strike')
            else:
                update_score('right')
                spawn_ball()
    else:
        if ball_right > WIDTH/2:
            c.move(BALL, right_edge_distance-ball_right, BALL_Y_SPEED)
        else:
            c.move(BALL, -ball_left+PAD_W, BALL_Y_SPEED)
    if ball_top + BALL_Y_SPEED < 0 or ball_bottom + BALL_Y_SPEED > HEIGHT:
        bounce('ricochet')


def main():
    move_ball()
    move_pads()
    root.after(20, main)

main()
root.mainloop()