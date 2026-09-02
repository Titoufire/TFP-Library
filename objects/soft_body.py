import pygame
import math
from objects.spring import Spring
from objects.ball import Ball

Vec2 = pygame.math.Vector2

class Soft_Body():

    def __init__(self):
        self.edges = []
        self.balls = []

    def build_from_points(points: list[tuple[int, int]], springs: list[tuple[int, int]], color: str | pygame.Color,
                          pos: tuple[int, int], rad: int, force=0.5, fric=0):
        soft_body = Soft_Body()
        for point in points:
            soft_body.balls.append(Ball(color, (point[0]+pos[0], point[1]+pos[1]), (0, 0), radius=rad, fric=fric))
        for spring in springs:
            soft_body.edges.append(Spring(color, soft_body.balls[spring[0]], soft_body.balls[spring[1]], thickness=2, force=force))
        return soft_body

    def build_from_balls(balls: list[Ball], springs: list[tuple[int, int]], color: str | pygame.Color):
        pass

    def build_from_file(self, file_path: str): #not ready
        file = open(file_path, 'r')
        for line in file.readlines():
            if line.startswith('/'):
                print("new object")
                pass
            elif line.startswith('+'):
                print("new endpoint")
                pass
            elif line.startswith('-'):
                print("new spring")
                pass
            elif line.startswith('='):
                print("new object from preset")
                pass

    def build_from_preset(preset_name: str, pos: tuple[int, int], color: str | pygame.Color,
                          rad: int, length = 10, width = 10, force=0.5, definition = 8):
        
        if preset_name == "square":
            #requires length, rad, (force)
            Soft_Body.build_from_points(
                #points
                [
                    (-length/2, -length/2),
                    (length/2, -length/2),
                    (-length/2, length/2),
                    (length/2, length/2)
                ], [
                    #springs
                    (0, 1),
                    (2, 3),
                    (0, 2),
                    (1, 3),
                    (0, 3),
                    (1, 2)
                ], color, pos, rad, force=force)
        elif preset_name == "rectangle":
            #requires length, width, rad, (force)
            Soft_Body.build_from_points(
                #points
                [
                    (-length/2, -width/2),
                    (length/2, -width/2),
                    (-length/2, width/2),
                    (length/2, width/2)
                ], [
                    #springs
                    (0, 1),
                    (2, 3),
                    (0, 2),
                    (1, 3),
                    (0, 3),
                    (1, 2)
                ], color, pos, rad, force=force)
        elif preset_name == "triangle":
            #requires length, rad, (force)
            Soft_Body.build_from_points(
                #points
                [
                    (-length/2, length*math.sqrt(3)/4),
                    (0, -length*math.sqrt(3)/4),
                    (length/2, length*math.sqrt(3)/4)
                ], [
                    #springs
                    (0, 1),
                    (1, 2),
                    (2, 0)
                ], color, pos, rad, force=force)
        elif preset_name == "circle":
            #requires length, definition, rad, (force)
            points, springs = [], []
            for i in range(definition):
                angle = (2 * math.pi * i) / definition
                x = pos[0]/2 + length * math.cos(angle)
                y = pos[1]/2 + length * math.sin(angle)
                points.append((x, y))
            for i in range(definition):
                springs.append((i, (i + 1) % definition))
                springs.append((i, (i + 2) % definition))
                #springs.append((i, (i + 3) % definition))
                if i < definition/2:
                    springs.append((i, (i + round(definition/2)) % definition))
            print("points:", points)
            print("springs:", springs)
            Soft_Body.build_from_points(points, springs, color, pos, rad, force=force, fric=0.5)
        else:
            raise ValueError(f"[tfp] ValueError: Invalid preset name for soft body, {preset_name} was given")