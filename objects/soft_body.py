import pygame
from objects.spring import Spring
from objects.ball import Ball

Vec2 = pygame.math.Vector2

class Soft_Body():

    def __init__(self, color: str | pygame.Color,vertices: list[tuple[int, int] | Ball], edges: list[tuple[int, int]]):
        self.vertices = vertices
        self.edges = edges
        self.color = color
        self.balls = []

        if self.vertices[0] == tuple:
            self.build_from_points(self.vertices, self.edges)
        elif self.vertices[0] == Ball:
            self.build_from_balls(self.vertices, self.edges)

    def build_from_points(self, points: list[tuple[int, int]], edges: list[tuple[int, int]]):
        for point in points:
            self.balls.append(Ball(self.color, point, (0, 0)))

    def build_from_balls(self, balls: list[Ball], edges: list[tuple[int, int]]):
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

    def build_from_preset(self, preset_name: str, size: int, pos: tuple[int, int]): #not ready
        if preset_name == "square":
            pass
        elif preset_name == "triangle":
            pass
        elif preset_name == "circle":
            pass
        else:
            raise ValueError("[tfp] ValueError: Invalid preset name for soft body")