import pygame

Vec2 = pygame.math.Vector2

class Line():
    
    def __init__(self, color: str, start: tuple, end: tuple, rest=1, fric=0):
        self.pos = Vec2(start[0], start[1])
        self.end = Vec2(end[0], end[1])
        self.color = color
        self.direction = Vec2(end[0]-start[0], end[1]-start[1])
        self.normal = self.direction.rotate(-90).normalize()
        self.lenght = self.direction.length()
        self.restitution = rest
        self.friction = fric
        
    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.pos, self.end)