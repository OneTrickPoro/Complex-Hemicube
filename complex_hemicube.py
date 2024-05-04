#list version
#hemicube has 3 faces, which corrispond to the grips U,L,R
#a single hemicube will be identified my the list [U,L,R]
#we use a 0 for nothing and 1 for dot so
# eg:  core is [0,0,0], anticore is [1,1,1]

from itertools import product
grips = ["U","L","R"]
opt = [0,1]

all_position =  list(product(["U0","U1"],["L0","L1"],["R0","R1"]))
GAME = [list(i) for i in all_position]
START = [list(i) for i in all_position]

def printSTART():
    print(START[0], START[4], START[2], START[1])
    print(START[-1], START[3],START[5],START[6])

def printGAME():
    print(GAME[0], GAME[4], GAME[2], GAME[1])
    print(GAME[-1], GAME[3],GAME[5],GAME[6])

def moveU(table=GAME):
    for i in range(len(GAME)):
        if GAME[i][0][-1]=="1":
            GAME[i]=[GAME[i][0], GAME[i][2],GAME[i][1]]
    return GAME

def moveL(table=GAME):
    for i in range(len(GAME)):
        if GAME[i][1][-1]=="1":
            GAME[i]=[GAME[i][2], GAME[i][1],GAME[i][0]]
    return GAME

def moveR(table=GAME):
    for i in range(len(GAME)):
        if GAME[i][-1][-1]=="1":
            GAME[i]=[GAME[i][1], GAME[i][0],GAME[i][2]]
    return GAME

#while True:
#    printGAME()
#    inp = int(input("Digit your move: 1=U  2=L  3=R..."))
#    while inp not in [1,2,3]:
#        inp = int(input("Digit your move: 1=U  2=L  3=R..."))
#    if inp == 1: GAME=moveU(GAME)
#    elif inp == 2: GAME = moveL(GAME)
#    elif inp == 3: Game = moveR(GAME)
import pygame
import sys
import math
import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ema-Complex_HemiCube")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE =  (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
PINK = (255, 192, 203)

#rettangoli display
squares = []
for xx in range(4):
    for yy in range(2):
        squares.append(pygame.Rect(100+150*xx, 200+150*yy, 150, 150))

def check_col_sq(i):
    if START[i]==GAME[i]:
        col = GREEN
    else:
        col = RED
    return col

def check_col_hemicube(state):
    if state[0]=="U": 
        col_h = WHITE
    elif state[0]=="L":
        col_h = CYAN
    elif state[0]=="R":
        col_h = PINK
    return col_h    

def draw_hemicube(center_x, center_y, radius, state):
    a,b,c = state
    angle = 360 / 6
    hexagon_vertices = []
    for i in range(6):
        x = center_x + radius * math.cos(math.radians(angle * i - 30))
        y = center_y + radius * math.sin(math.radians(angle * i - 30))
        hexagon_vertices.append((x, y))
    pygame.draw.polygon(screen, BLACK, hexagon_vertices, 2)
    dot_centers = []
    for i in range(3):
        x = center_x + radius//2 * math.cos(math.radians(-2 * angle * i - 90))
        y = center_y + radius//2 * math.sin(math.radians(-2 * angle * i - 90))
        dot_centers.append((x,y))
    #colors
    for i in range(6):
        x1, y1 = hexagon_vertices[i]
        x2, y2 = hexagon_vertices[(i + 1) % 6]
        x3, y3 = center_x, center_y
        triangle_vertices = [(x1, y1), (x2, y2), (x3, y3)]
        if i==4 or i==5:
            pygame.draw.polygon(screen, check_col_hemicube(a), triangle_vertices)
        elif i==0 or i==1:
            pygame.draw.polygon(screen, check_col_hemicube(b), triangle_vertices)
        elif i==2 or i==3:
            pygame.draw.polygon(screen, check_col_hemicube(c), triangle_vertices)
    #dot
        if a[-1]=="1":
            pygame.draw.circle(screen, BLACK, dot_centers[0], 10 ,0)
        if b[-1]=="1":
            pygame.draw.circle(screen, BLACK, dot_centers[1], 10 ,0)
        if c[-1]=="1":
            pygame.draw.circle(screen, BLACK, dot_centers[2], 10 ,0)


#state
solved = True
def random_mov(GAME):
    num = random.choice([1,2,3])
    if num == 1:
        return moveU(GAME)
    elif num == 2:
        return moveL(GAME)
    elif num == 3:
        return moveR(GAME)

def scramble(GAME):
    for _ in range(50):
        GAME = random_mov(GAME)
    if GAME != [list(i) for i in all_position]:
        return GAME
    else:
        return scramble(GAME)

def reset(GAME):
    GAME = [list(i) for i in all_position]
    return GAME

#labels
font_title = pygame.font.Font(None, 36)
font_desc = pygame.font.Font(None, 24)
title_text = font_title.render("Complex Hemicube", True, BLACK, GREY)
desc_text = font_desc.render("Type for move", True, BLACK, GREY)
U_text = font_desc.render("U grip: J", False, BLACK, GREY)
L_text = font_desc.render("L grip: K", False, BLACK, GREY)
R_text = font_desc.render("R grip: L", False, BLACK, GREY)
Scramble_text = font_desc.render("Scramble: R", False, BLACK, GREY)
Reset_text = font_desc.render("Reset puzzle: Q", False, BLACK, GREY)
title_rect = title_text.get_rect(center=(width // 2, 50))
desc_rect = desc_text.get_rect(topright=( 220, title_rect.bottom + 10))
U_rect = U_text.get_rect(topright=( 200, title_rect.bottom + 30))
L_rect = L_text.get_rect(topright=( 200, title_rect.bottom + 50))
R_rect = R_text.get_rect(topright=( 200, title_rect.bottom + 70))
Scramble_rect = L_text.get_rect(topright=( 200, title_rect.bottom + 90))
Reset_rect = R_text.get_rect(topright=( 200, title_rect.bottom + 110))


def draw_writes():
    pygame.draw.rect(screen, GREY, title_rect)
    pygame.draw.rect(screen, GREY, desc_rect)
    pygame.draw.rect(screen, GREY, U_rect)
    pygame.draw.rect(screen, GREY, L_rect)
    pygame.draw.rect(screen, GREY, Scramble_rect)
    pygame.draw.rect(screen, GREY, Reset_rect)
    pygame.draw.rect(screen, GREY, R_rect)
    screen.blit(title_text, title_rect)
    screen.blit(desc_text, desc_rect)
    screen.blit(U_text, U_rect)
    screen.blit(L_text, L_rect)
    screen.blit(R_text, R_rect)
    screen.blit(Reset_text, Reset_rect)
    screen.blit(Scramble_text, Scramble_rect)

#timer
def draw_timer(timer_value):
    minutes = timer_value // 60000
    seconds = (timer_value // 1000) % 60
    centiseconds = timer_value % 100
    time_text = "{:02d}:{:02d}.{:02d}".format(minutes, seconds, centiseconds)
    font = pygame.font.Font(None, 40)
    text = font.render(time_text, True, BLACK)
    text_rect = text.get_rect(center=(width - 300, 100))
    screen.blit(text, text_rect)

clock = pygame.time.Clock()
timer_on = False
start_time = pygame.time.get_ticks()
timer_wait = False
act_time = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if timer_wait:
                timer_wait = not timer_wait
                start_time = pygame.time.get_ticks()   
            if event.key == pygame.K_j:
                GAME = moveU(GAME)
            elif event.key == pygame.K_k:
                GAME = moveL(GAME)
            elif event.key == pygame.K_l:
                GAME = moveR(GAME)
            elif event.key == pygame.K_q:
                GAME = reset(GAME)
                solved = True
                timer_on = False
            elif event.key == pygame.K_r:
                if not solved:
                    GAME = scramble(GAME)
                    timer_wait = True
                else:
                    GAME = scramble(GAME)
                    solved = False
                    if timer_on == True:
                        timer_on = False
                    else:
                        timer_on = True
                        timer_wait = True
             
    #time check
    if timer_on and timer_wait ==False:
        act_time = pygame.time.get_ticks() - start_time
   
    screen.fill(GREY)
    draw_writes()
    draw_timer(act_time)
    for i in range(len(GAME)):
        rettangolo = squares[i]
        pygame.draw.rect(screen, check_col_sq(i),rettangolo, 0)
        draw_hemicube(rettangolo.centerx, rettangolo.centery, 70, GAME[i])
    if GAME == START and solved == False:
        solved = True
    if solved and timer_on:
        print("solved!", act_time)
        timer_on = False
    pygame.display.update()
    clock.tick(60)