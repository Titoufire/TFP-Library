import pygame
import random
from objects.ball import Ball
from objects.line import Line
from objects.spring import Spring
from objects.rigid_body import Rigid_Body
from objects.soft_body import Soft_Body

#initialization
pygame.init()
Vec2 = pygame.math.Vector2

#system variables
VERSION = "Alpha 0"
WIDTH = 800
HEIGHT = 600
TITLE = "TFP library test (" + VERSION + ")"
FPS = 60

print("Using Titoufire's Physics Library version", VERSION, "\n")

#screen variables
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

#main variables
physics_frames = 10
clock = pygame.time.Clock()
running = True
bg_color = (40, 160, 120)
gravity = Vec2(0, 7)
right_click = False
target_ball = None

#world import
#L1 = Line('yellow', (0, 50), (WIDTH/2, 250))
#L2 = Line('yellow', (WIDTH/1.5, HEIGHT-20), (WIDTH, 50))
#L3 = Line('yellow', (0, 250), (WIDTH/3, HEIGHT-30))
#L4 = Line('yellow', (0, 50), (0, 250))
'''lines.append(L1)
lines.append(L2)
lines.append(L3)
lines.append(L4)'''
left_wall = Line('red', (0, 50), (0, HEIGHT-30), rest=1)
right_wall = Line('red', (WIDTH-1, HEIGHT-30), (WIDTH-1, 50), rest=1)
ceiling = Line('red', (WIDTH-1, 50), (0, 50), rest=1)
floor = Line('red', (0, HEIGHT-30), (WIDTH-1, HEIGHT-30), rest=1)
#lines.append(left_wall)
#lines.append(right_wall)
#lines.append(ceiling)
#lines.append(floor)

#entities import

#big cube !!!
'''balls = [
    Ball('green', (120, 150), (0, 0), rest=1, floating=False),
    Ball('white', (120, 250), (0, 0), rest=1, floating=False),
    Ball('red', (200, 150), (0, 0), rest=1, floating=False),
    Ball('blue', (200, 250), (0, 0), rest=1, floating=False)]

Spring('orange', balls[0], balls[1], force=.05, length=150, thickness=4)
Spring('orange', balls[2], balls[3], force=.05, length=150, thickness=4)
Spring('orange', balls[0], balls[2], force=.05, length=150, thickness=4)
Spring('orange', balls[3], balls[1], force=.05, length=150, thickness=4)
Spring('red', balls[0], balls[3], force=.1, length=200, thickness=4)
Spring('red', balls[2], balls[1], force=.1, length=200, thickness=4)'''
    
rigid_lines = []

rigids = [
    #Rigid_Body('white', (200, 150), (0, 0), [(10, 10), (-10, 10), (0, -10)], fixed=True, rigid_lines=rigid_lines)
    #Rigid_Body('white', (200, 150), (0, 0), [(10, 10), (-10, 11), (0, -10)], fixed=False)
    ]

#square = Soft_Body.build_from_preset('square', (500, 300), 'white', 5, length=35)
#rectangle = Soft_Body.build_from_preset('rectangle', (600, 300), 'white', 5, length=50, width=30)
#triangle = Soft_Body.build_from_preset('triangle', (700, 300), 'white', 5, length=50, force=0.7)
#circle = Soft_Body.build_from_preset('circle', (250, 100), 'white', 5, length=50)

imports = Soft_Body.build_from_file('objects/soft_body_imports.txt')

#game loop
while running:
    
    #clock and delta time
    dt = clock.tick(FPS)/1000
    TITLE = "TFP library test (" + VERSION + ")" + " FPS:" + str(round(clock.get_fps(), 1))
    pygame.display.set_caption(TITLE)
    
    #events
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #left click
                if event.button == 1:
                    red = random.randint(0, 255)
                    green = random.randint(0, 255)
                    blue = random.randint(0, 255)
                    Ball.balls.append(Ball((red, green, blue), pygame.mouse.get_pos(), (0, 0), fric=0.1, rest=0.99))

                #right click
                elif event.button == 3:
                    right_click = True
                    for ball in Ball.balls:
                        if Vec2(pygame.mouse.get_pos()).distance_to(ball.pos) < ball.radius:
                            target_ball = ball

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    right_click = False
                    target_ball = None
    except: pass

    if right_click:
        try:
            target_ball.velocity = Vec2(0, 0)
            target_ball.pos = Vec2(pygame.mouse.get_pos())
        except: pass
 
    #physics
    for i in range(physics_frames): #execute multiple physics frames in one video frame to increase precision
        #respect order: Rigid_Body, Ball, Spring
        for rigid in rigids:
            rigid.simulate(dt, gravity, rigids)
            
        for ball in Ball.balls:
            ball.simulate(dt, gravity, Line.lines+rigid_lines)
            
        for spring in Spring.springs:
            spring.simulate()
            
    #drawing       
    screen.fill(bg_color)
    pygame.draw.line(screen, 'blue', (0, 49), (WIDTH, 49))
    
    for ball in Ball.balls:
        ball.draw(screen)
    
    for line in Line.lines:
        line.draw(screen)
        
    for spring in Spring.springs:
        spring.draw(screen)
        
    for rigid in rigids:
        rigid.draw(screen)
            
    #update screen
    pygame.display.flip()
    
pygame.quit()