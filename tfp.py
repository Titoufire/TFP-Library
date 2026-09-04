import pygame
from objects.ball import Ball
from objects.line import Line
from objects.spring import Spring
from objects.rigid_body import Rigid_Body
from objects.soft_body import Soft_Body

#initialization
pygame.init()
Vec2 = pygame.math.Vector2

class Tfp():

    def __init__(self):
        self.VERSION = "Alpha 0"
        print("Using Titoufire's Physics Library version", self.VERSION, "\n")
        self.has_setup = False
        self.window = None
        self.camera = None
        self.physics_frames = 0
        self.gravity = Vec2(0, 1)
        self.ball = Ball
        self.line = Line
        self.spring = Spring
        self.rigid_body = Rigid_Body
        self.soft_body = Soft_Body
        self.pause_simulation = False
        self.rigids = []
        self.rigid_lines = []
        self.bg_color = (40, 160, 120)
        self.WIDTH = 0
        self.HEIGHT = 0

    def setup(self, window: pygame.surface, camera: Camera, physics_frames: int=10):
        self.window = window
        self.camera = camera
        self.physics_frames = physics_frames
        self.WIDTH = self.window.width
        self.HEIGHT = self.window.height
        self.has_setup = True

    def draw(self):
        if not self.has_setup: raise("Tfp was not set up yet. please call the setup() function before")
        screen = self.window
        screen.fill(self.bg_color)
        pygame.draw.line(screen, 'blue', (0, 49), (self.WIDTH, 49))
            
        for ball in Ball.balls:
            ball.draw(screen)
            
        for line in Line.lines:
            line.draw(screen)
                
        for spring in Spring.springs:
            spring.draw(screen)
                
        for rigid in self.rigids:
            rigid.draw(screen)

    def simulate(self, dt):
        if not self.has_setup: raise("Tfp was not set up yet. please call the setup() function before")
        self.WIDTH = self.window.width
        self.HEIGHT = self.window.height
        if not self.pause_simulation:
            for i in range(self.physics_frames): #execute multiple physics frames in one video frame to increase precision
                #respect order: Rigid_Body, Ball, Spring
                for rigid in self.rigids:
                    rigid.simulate(dt, self.gravity, self.rigids)
                    
                for ball in Ball.balls:
                    ball.simulate(dt, self.gravity, Line.lines+self.rigid_lines)
                    
                for spring in Spring.springs:
                    spring.simulate()

    def set_gravity(self, full: Vec2=None, strenght: float=0, direction: Vec2=None):
        if not self.has_setup: raise("Tfp was not set up yet. please call the setup() function before")
        if full:
            self.gravity = full
        elif strenght:
            self.gravity = self.gravity.normalize_ip()*strenght
        if direction:
            self.gravity = direction*self.gravity.length()

    def new_line(self, color: str, start: tuple[int, int], end: tuple[int, int], rest=1, fric=0):
        if not self.has_setup: raise("Tfp was not set up yet. please call the setup() function before")
        return Line(color=color, start=start, end=end, rest=rest, fric=fric)

    def new_ball(self, color: str | pygame.Color, pos: tuple[int, int], velocity: tuple[int, int],
                 rest=1, fric=0, mass=1, floating=False, radius=20):
        if not self.has_setup: raise("Tfp was not set up yet. please call the setup() function before")
        return Ball(color=color, pos=pos, velocity=velocity, rest=rest, fric=fric,
                      mass=mass, floating=floating, radius=radius)

    def new_spring(self, color: str | pygame.Color, node1: Ball, node2: Ball, length=None,
                 force=0.5, thickness=None, damp=0.3, dz = 0.01):
        if not self.has_setup: raise("Tfp was not set up yet. please call the setup() function before")
        return Spring(color=color, node1=node1, node2=node2, length=length,
                 force=force, thickness=thickness, damp=damp, dz = dz)

    def new_rigid(self, color: str | pygame.Color, pos: tuple[int, int], velocity: tuple[int, int], vertices: list[tuple[int, int]],
                 edge_color=None, edge_thickness=1, fric=0, rest=1, fixed=False):
        if not self.has_setup: raise("Tfp was not set up yet. please call the setup() function before")
        self.rigids.append(Rigid_Body(color=color, pos=pos, velocity=velocity, vertices=vertices, edge_color=edge_color,
                          edge_thickness=edge_thickness, fric=fric, rest=rest, fixed=fixed, rigid_lines=self.rigid_lines))
        return self.rigids[-1]

    def say_hello(self):
        print(f"hello from tfp")

    class Camera():

        def __init__(self, pos: Vec2, zoom: float=1.0):
            self.pos = pos
            self.zoom = zoom