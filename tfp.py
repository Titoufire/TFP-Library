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
        self.physics_frames = physics_frames
        self.gravity = Vec2(0, 1)

    def set_gravity(self, full: Vec2=None, strenght: float=0, direction: Vec2=None):
        if full:
            self.gravity = full
        elif strenght:
            self.gravity = self.gravity.normalize_ip()*strenght
        if direction:
            self.gravity = direction*self.gravity.length()

    def new_ball(self, color: str | pygame.Color, pos: tuple[int, int], velocity: tuple[int, int],
                 rest=1, fric=0, mass=1, floating=False, radius=20):
        result = Ball(color=color, pos=pos, velocity=velocity, rest=rest, fric=fric,
                      mass=mass, floating=floating, radius=radius)
        return result

    def say_hello(self):
        print(f"hello from tfp")