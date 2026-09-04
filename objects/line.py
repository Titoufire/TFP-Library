import pygame

Vec2 = pygame.math.Vector2

class Line():

    lines: list[Line] = []
    def __init__(self, color: str, start: tuple[int, int], end: tuple[int, int], rest=1, fric=0, dont_self=False):
        self.pos = Vec2(start[0], start[1])
        self.end = Vec2(end[0], end[1])
        self.color = color
        self.direction = Vec2(end[0]-start[0], end[1]-start[1])
        self.norm_dir = self.direction.normalize()
        self.normal = self.direction.rotate(-90).normalize()
        self.length = self.direction.length()
        self.restitution = rest
        self.friction = fric

        if not dont_self:
            Line.lines.append(self)
        
    def draw(self, screen: pygame.Surface):
        pygame.draw.line(screen, self.color, self.pos, self.end)