import pygame

Vec2 = pygame.math.Vector2

class Line():

    rigid_lines: list[Line] = []
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
        else:
            Line.rigid_lines.append(self)
        
    def draw(self, screen: pygame.Surface, camera):
        screen_pos = ((self.pos[0]+camera.pos[0])*camera.zoom, (self.pos[1]+camera.pos[1])*camera.zoom)
        end_pos = ((self.end[0]+camera.pos[0])*camera.zoom, (self.end[1]+camera.pos[1])*camera.zoom)
        pygame.draw.line(screen, self.color, screen_pos, end_pos)