import pygame
from objects.ball import Ball

Vec2 = pygame.math.Vector2

clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
class Spring():

    springs: list[Spring] = []
    def __init__(self, color: str | pygame.Color, node1: Ball, node2: Ball, length=None,
                 force=0.5, thickness=None, damp=0.3, dz = 0.01):
        
        self.node1 = node1
        self.node2 = node2
        self.length = length
        if length == None:
            self.length = Vec2(node1.pos.x-node2.pos.x, node1.pos.y-node2.pos.y).length()
        self.force = force
        self.step = 1
        self.color = color
        self.thickness = thickness
        if thickness == None:
            self.thickness = round(force/2)
        self.damping = damp
        self.dead_zone = dz
        self.steps_ahead = 2

        Spring.springs.append(self)
        
    def simulate(self):
        distX = (self.node1.pos.x+self.node1.velocity.x*self.steps_ahead)-(self.node2.pos.x+self.node2.velocity.x*self.steps_ahead)
        distY = (self.node1.pos.y+self.node1.velocity.y*self.steps_ahead)-(self.node2.pos.y+self.node2.velocity.y*self.steps_ahead)
        try:
            distance = (distX**2 + distY**2)**0.5
        except OverflowError:
            raise OverflowError("[tfp] OverflowError: distance calculation overflowed, consider making the spring smaller")

        if not -self.dead_zone < self.length - distance < self.dead_zone:
            vel1X = -distX * (1-self.length/distance)/2 * self.force
            vel1Y = -distY * (1-self.length/distance)/2 * self.force
            vel2X = distX * (1-self.length/distance)/2 * self.force
            vel2Y = distY * (1-self.length/distance)/2 * self.force
            self.node1.velocity.x += vel1X
            self.node1.velocity.y += vel1Y
            self.node2.velocity.x += vel2X
            self.node2.velocity.y += vel2Y

    def draw(self, screen: pygame.Surface):
        pygame.draw.line(screen, self.color, self.node1.pos, self.node2.pos, self.thickness)