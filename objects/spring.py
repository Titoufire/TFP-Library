import pygame
from objects.ball import Ball

Vec2 = pygame.math.Vector2

class Spring():  # WARNING    Springs don't work as intended !
    
    def __init__(self, color: str, node1: Ball, node2: Ball, length=None, force=1, thickness=None):
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
        
    def simulate(self):
        '''distX = (self.node1.pos.x + self.node1.velocity.x*self.step) - (self.node2.pos.x + self.node2.velocity.x*self.step)
        distY = (self.node1.pos.y + self.node1.velocity.y*self.step) - (self.node2.pos.y + self.node2.velocity.y*self.step)
        distance = Vec2(distX, distY).length()
        
        self.node1.pos.x += -distX * (1 - self.length/distance)/2 * self.force/self.step
        self.node1.pos.y += -distY * (1 - self.length/distance)/2 * self.force/self.step
        self.node2.pos.x += distX * (1 - self.length/distance)/2 * self.force/self.step
        self.node2.pos.y += distY * (1 - self.length/distance)/2 * self.force/self.step'''
        
        lin_vec = Vec2(self.node2.pos.x-self.node1.pos.x, self.node2.pos.y-self.node1.pos.y)
        distance_to_correct = lin_vec.length()-self.length
        lin_vec.normalize_ip()
        self.node1.pos += lin_vec*self.force*distance_to_correct
        self.node2.pos -= lin_vec*self.force*distance_to_correct
        
    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.node1.pos, self.node2.pos, self.thickness)