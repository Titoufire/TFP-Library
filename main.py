import pygame
import random
from objects.ball import Ball
from objects.line import Line
from objects.spring import Spring
from objects.rigid_body import Rigid_Body

#initialization
pygame.init()
Vec2 = pygame.math.Vector2

#system variables
WIDTH = 800
HEIGHT = 600
TITLE = "Physics test"
FPS = 30

#screen variables
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

#main variables
physics_frames = 10
clock = pygame.time.Clock()
running = True
bg_color = (40, 160, 120)
gravity = Vec2(0, 0.5)

#world import
lines = []
floor = Line('red', (10, HEIGHT-30), (WIDTH-20, HEIGHT-30))
lines.append(floor)

L1 = Line('yellow', (0, 50), (WIDTH/2, 250))
L2 = Line('yellow', (WIDTH/1.5, HEIGHT-20), (WIDTH, 50))
L3 = Line('yellow', (0, 250), (WIDTH/3, HEIGHT-30))
L4 = Line('yellow', (0, 50), (0, 250))
'''lines.append(L1)
lines.append(L2)
lines.append(L3)
lines.append(L4)'''

#entities import
balls = [
    Ball('red', (50, 50), (0, 0), rest=.99),
    Ball('green', (120, 50), (0, 0), rest=.99),
    Ball('blue', (50, 120), (0, 0), rest=.99),
    Ball('white', (120, 120), (0, 0), rest=.99)]
    
'''Ball('blue', (50, 50), (0, 0), fric=0.1, rest=0.99),
    Ball('aqua', (100, 50), (0, 0), fric=0.1, rest=0.99),
    Ball('bisque', (200, 50), (0, 0), fric=0.1, rest=0.99),
    Ball('chartreuse', (300, 50,), (0, 0), fric=0.1, rest=0.99),
    Ball('white', (500, 0), (0, 0), fric=0.1, rest=0.99)'''
    
springs = []
'''Spring('orange', balls[0], balls[1], force=.5, length=100, thickness=4),
    Spring('orange', balls[2], balls[3], force=.5, length=100, thickness=4),
    Spring('orange', balls[0], balls[2], force=.5, length=100, thickness=4),
    Spring('orange', balls[1], balls[3], force=.5, length=100, thickness=4),
    Spring('orange', balls[0], balls[3], force=.5, length=100, thickness=4),
    Spring('orange', balls[2], balls[1], force=.5, length=100, thickness=4)'''
    
rigids = [
    Rigid_Body('white', (200, 150), (0, 0), [(10, 10), (-10, 10), (0, -10)], fixed=False)]

#game loop
while running:
    
    #clock and delta time
    dt = clock.tick(FPS)/1000
    
    #events
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    red = random.randint(0, 255)
                    green = random.randint(0, 255)
                    blue = random.randint(0, 255)
                    balls.append(Ball((red, green, blue), pygame.mouse.get_pos(), (0, 0), fric=0.1, rest=0.99))
                    
    except: pass
    
    #physics
    for i in range(physics_frames): #execute multiple physics flames in one video frame to increase precision
        #respect order: Rigid_Body, Ball, Spring
        for rigid in rigids:
            rigid.simulate(dt, gravity, lines)
            
        for ball in balls:
            ball.simulate(dt, gravity, lines, balls)
            
        for spring in springs:
            spring.simulate()
            
    #drawing       
    screen.fill(bg_color)
    pygame.draw.line(screen, 'blue', (0, 49), (WIDTH, 49))
    
    for ball in balls:
        ball.draw(screen)
    
    for line in lines:
        line.draw(screen)
        
    for spring in springs:
        spring.draw(screen)
        
    for rigid in rigids:
        rigid.draw(screen)
            
    #update screen
    pygame.display.flip()
    
pygame.quit()