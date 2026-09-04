import pygame
import math
from Tfp.objects.spring import Spring
from Tfp.objects.ball import Ball

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

    def build_from_balls(balls: list[Ball], springs: list[tuple[int, int]], color: str | pygame.Color, force=0.5):
        soft_body = Soft_Body()
        for spring in springs:
            soft_body.edges.append(Spring(color, balls[spring[0]], balls[spring[1]], thickness=2, force=force))
        return soft_body

    def build_from_file(file_path: str): #not ready
        ''' 
        ----- USAGE -----
        to create a soft body from a preset:
        start the line with '=' then add you arguments separated by a single white space. 
        don't put parenthesies around the coordinates. example:
        {= square 500,300 black 5 length=30}  (the brackets represent code, do not put them in)

        to create a soft body from scratch:
        start a line with  '/' to create a new soft body, followed by the center of your soft body,
        optionally followed by the name of that soft body. example:
        {/ 100,50 rainbow square}

        to add vertices, start a line with '+' followed by your arguments separated by a single white space. example:
        {+ red -20,-20 0,0 floating=True radius=10}

        to add springs, start a line with '-' followed by your arguments separated by a single white space.
        for the first and second node, use the index of the the balls you want to join
        (index order is the order to added the vertices). example:
        {+ yellow 0 1 force=0.7}
        '''
        file = open(file_path, 'r')
        objects = []
        lines = file.readlines()
        for line in lines:
            line = line.split("\n")[0]

            if line.startswith('/'):
                #new object
                temp_position = line.split(" ")[1]
                position = (float(temp_position.split(",")[0]), float(temp_position.split(",")[0]))
                objects.append(Soft_Body())

            elif line.startswith('+'):
                #new vertice
                args = line.split(" ")[1:]
                color = args[0]
                pos = (float(args[1].split(",")[0]), float(args[1].split(",")[1]))
                velocity = (float(args[2].split(",")[0]), float(args[2].split(",")[1]))
                rest, fric, mass, floating, radius = 1, 0, 1, False, 20
                flags = args[3:]
                for flag in flags:
                    flagid = flag.split("=")[0]
                    flagval = flag.split("=")[1]
                    if flagid == 'rest':
                        rest = float(flagval)
                    elif flagid == 'fric':
                        fric = float(flagval)
                    elif flagid == 'mass':
                        mass == float(flagval)
                    elif flagid == 'floating':
                        if flagval == 'True':
                            floating = True
                        elif flagid == 'False':
                            floating = False
                    elif flagid == 'radius':
                        radius = float(flagval)
                    else:
                        raise ValueError(f"[tfp], wrong flag argument in soft_Body.load_from_file(). {flagid} was given")
                objects[-1].balls.append(Ball(color, (position[0]+pos[0], position[1]+pos[1]), velocity, rest=rest, fric=fric, mass=mass,
                                              floating=floating, radius=radius))

            elif line.startswith('-'):
                #new spring
                args = line.split(" ")[1:]
                color = args[0]
                node1, node2 = int(args[1]), int(args[2])
                flags = args[3:]
                length, force, thickness, damp, dz = None, 0.5, None, 0.3, 0.01
                for flag in flags:
                    flagid = flag.split("=")[0]
                    flagval = float(flag.split("=")[1])
                    if flagid == 'length':
                        length = float(flagval)
                    elif flagid == 'force':
                        force = float(flagval)
                    elif flagid == 'thickness':
                        thickness = int(flagval)
                    elif flagid == 'damp':
                        damp = float(flagval)
                    elif flagid == 'dz':
                        dz = float(flagval)
                    else:
                        raise ValueError(f"[tfp], wrong flag argument in soft_Body.load_from_file(). {flagid} was given")
                objects[-1].edges.append(Spring(color, objects[-1].balls[node1], objects[-1].balls[node2],
                                                length=length, force=force, thickness=thickness, damp=damp, dz=dz))

            elif line.startswith('='):  #that works
                #new object from preset
                args = line.split(" ")[1:]
                preset_name = args[0]
                pos = (float(args[1].split(",")[0]), float(args[1].split(",")[1]))
                color = args[2]
                rad = float(args[3])
                flags = args[4:]
                length, width, force, definition = 10, 10, 0.5, 8
                for flag in flags:
                    flagid = flag.split("=")[0]
                    flagval = float(flag.split("=")[1])
                    if flagid == 'length':
                        length = flagval
                    elif flagid == 'width':
                        width = flagval
                    elif flagid == 'force':
                        force = flagval
                    elif flagid == 'definition':
                        definition = int(flagval)
                    else:
                        raise ValueError(f"[tfp], wrong flag argument in soft_Body.load_from_file(). {flagid} was given")
                objects.append(Soft_Body.build_from_preset(preset_name, pos, color, rad, length=length, width=width,
                                                           force=force, definition=definition))
        file.close()
        return objects

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
            Soft_Body.build_from_points(points, springs, color, pos, rad, force=force, fric=0.5)
        else:
            raise ValueError(f"[tfp] ValueError: Invalid preset name for soft body, {preset_name} was given")