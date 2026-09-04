import pygame
from objects.ball import Ball
from objects.line import Line
from objects.spring import Spring
from objects.rigid_body import Rigid_Body
from objects.soft_body import Soft_Body
from camera import Camera

#initialization
pygame.init()
Vec2 = pygame.math.Vector2

class Tfp():

    def __init__(self, window: pygame.surface, camera: Camera, physics_frames: int=10):
        self.VERSION = "Alpha 0"
        print("Using Titoufire's Physics Library version", self.VERSION, "\n")
        self.window = window
        self.camera = camera
        self.physics_frames = physics_frames
        self.gravity = Vec2(0, 1)
        self.ball = Ball
        self.line = Line
        self.spring = Spring
        self.rigid_body = Rigid_Body
        self.soft_body = Soft_Body

    def set_gravity(self, full: Vec2=None, strenght: float=0, direction: Vec2=None):
        if full:
            self.gravity = full
        elif strenght:
            self.gravity = self.gravity.normalize_ip()*strenght
        if direction:
            self.gravity = direction*self.gravity.length()

    def new_line(self, color: str, start: tuple[int, int], end: tuple[int, int], rest=1, fric=0):
        return Line(color=color, start=start, end=end, rest=rest, fric=fric)

    def new_ball(self, color: str | pygame.Color, pos: tuple[int, int], velocity: tuple[int, int],
                 rest=1, fric=0, mass=1, floating=False, radius=20):
        return Ball(color=color, pos=pos, velocity=velocity, rest=rest, fric=fric,
                      mass=mass, floating=floating, radius=radius)

    def new_spring(self, color: str | pygame.Color, node1: Ball, node2: Ball, length=None,
                 force=0.5, thickness=None, damp=0.3, dz = 0.01):
        return Spring(color=color, node1=node1, node2=node2, length=length,
                 force=force, thickness=thickness, damp=damp, dz = dz)

    def new_rigid(self, color: str | pygame.Color, pos: tuple[int, int], velocity: tuple[int, int], vertices: list[tuple[int, int]],
                 edge_color=None, edge_thickness=1, fric=0, rest=1, fixed=False, rigid_lines=None):
        return Rigid_Body(color=color, pos=pos, velocity=velocity, vertices=vertices, edge_color=edge_color,
                          edge_thickness=edge_thickness, fric=fric, rest=rest, fixed=fixed, rigid_lines=rigid_lines)

    def say_hello(self):
        print(f"hello from tfp")