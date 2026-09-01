import pygame

Vec2 = pygame.math.Vector2

class Camera():

    def __init__(self, pos: Vec2, zoom: float):
        self.pos = pos
        self.zoom = zoom