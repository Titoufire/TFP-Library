import pygame

Vec2 = pygame.math.Vector2

class Ball():
    
    def __init__(self, color: str, pos: tuple, velocity: tuple, rest=1, fric=0, mass=1, floating=False):
        self.pos = Vec2(pos[0], pos[1])
        self.velocity = Vec2(velocity[0], velocity[1])
        self.acceleration = Vec2(0, 0)
        self.radius = 20
        self.color = color
        self.floating = floating
        self.positions = [] #for position tracker
        self.restitution = rest #0 is no bounce, 1 is perfectly elastic
        self.friction = fric #0 is no friction, 1 is instant stop
        self.mass = mass #unused
        self.collision_history = [[], [], [], [], [], [], [], [], [], []]  #for position solver when in line
        self.position_tracker = 100 #number of positions tracked
        
    def simulate(self, dt, gravity, lines, balls):
        #apply gravity
        if not self.floating:
            self.acceleration += gravity
        
        #movement update
        self.velocity += self.acceleration * dt
        self.pos += self.velocity*0.5 * dt
        self.acceleration = Vec2(0, 0)
        
        #collision detection and resolution
        self.collide_lines(lines)
        self.collide_balls(balls)
        
        #movement update 2
        self.pos += self.velocity*0.5 * dt
        
    def draw(self, screen):
        self.positions.append((self.pos[0], self.pos[1]))
        pygame.draw.circle(screen, self.color, self.pos, self.radius)
        
        #position tracker
        if len(self.positions) > self.position_tracker:
            self.positions.pop(0)
        for pos in self.positions:
            pygame.draw.circle(screen, 'red', pos, 1)
            
    def collide_lines(self, lines):
        collided = []
        for line in lines:
            dist = (self.pos.x-line.pos.x)*line.normal.x + (self.pos.y-line.pos.y)*line.normal.y
            if -self.radius < dist < self.radius:
                col_pos = (self.pos.x-line.pos.x)*-line.normal.y + (self.pos.y-line.pos.y)*line.normal.x
                col_friction = self.friction*line.friction
                col_restitution = self.restitution*line.restitution
                
                #on line collisions
                if 0 < col_pos < line.length:
                    norm_speed = self.velocity.x*line.normal.x + self.velocity.y*line.normal.y
                    tang_speed = self.velocity.x*line.normal.y + self.velocity.y*-line.normal.x
                    if norm_speed <= 0:
                        collided.append(line)
                        self.velocity.x = -(norm_speed*line.normal.x)*col_restitution +(tang_speed*line.normal.y)*(1-col_friction)
                        self.velocity.y = -(norm_speed*line.normal.y)*col_restitution +(tang_speed*-line.normal.x)*(1-col_friction)
                
                #end points collisions
                elif col_pos < 0:
                    normal = Vec2(self.pos.x-line.pos.x, self.pos.y-line.pos.y)
                    if normal.length() < self.radius:
                        normal.normalize_ip()
                        norm_speed = self.velocity.x*normal.x + self.velocity.y*normal.y
                        tang_speed = self.velocity.x*normal.y + self.velocity.y*-normal.x
                        if norm_speed <= 0:
                            collided.append(line)
                            self.velocity.x = -(norm_speed*normal.x)*col_restitution +(tang_speed*normal.y)*(1-col_friction)
                            self.velocity.y = -(norm_speed*normal.y)*col_restitution +(tang_speed*-normal.x)*(1-col_friction)
                elif col_pos > line.length:
                    normal = Vec2(self.pos.x-line.end.x, self.pos.y-line.end.y)
                    if normal.length() < self.radius:
                        normal.normalize_ip()
                        norm_speed = self.velocity.x*normal.x + self.velocity.y*normal.y
                        tang_speed = self.velocity.x*normal.y + self.velocity.y*-normal.x
                        if norm_speed <= 0:
                            collided.append(line)
                            self.velocity.x = -(norm_speed*normal.x)*col_restitution +(tang_speed*normal.y)*(1-col_friction)
                            self.velocity.y = -(norm_speed*normal.y)*col_restitution +(tang_speed*-normal.x)*(1-col_friction)
                
        #position solver
        self.collision_history.append(collided)
        self.collision_history.pop(0)
        for line in self.collision_history[0]:
            if line in self.collision_history[1]:
                if line in self.collision_history[2]:
                    if line in self.collision_history[3]:
                        if line in self.collision_history[4]:
                            if line in self.collision_history[5]:
                                if line in self.collision_history[6]:
                                    if line in self.collision_history[7]:
                                        if line in self.collision_history[8]:
                                            if line in self.collision_history[9]:
                                                self.pos += line.normal*1
                                                #print(f"position solver acted on {self.color}")
                            
    def collide_balls(self, balls):
        for ball in balls:
            if ball != self:
                normal = Vec2(self.pos.x-ball.pos.x, self.pos.y-ball.pos.y)
                if normal.length() < self.radius + ball.radius:
                    normal.normalize_ip()
                    self.collided_ball = ball
                    ball.collided_ball = self
                    col_friction = self.friction*ball.friction
                    col_restitution = self.restitution*ball.restitution
                    norm_speed = (self.velocity.x-ball.velocity.x)*normal.x + (self.velocity.y-ball.velocity.y)*normal.y
                    tang_speed = (self.velocity.x-ball.velocity.x)*normal.y + (self.velocity.y-ball.velocity.y)*-normal.x
                    if norm_speed <= 0:
                        forceX = tang_speed/2 * normal.y * col_friction
                        forceY = tang_speed/2 * -normal.x * col_friction
                        forceX += norm_speed/2 * normal.x * (1+col_restitution)
                        forceY += norm_speed/2 * normal.y * (1+col_restitution)
                        self.velocity.x -= forceX
                        self.velocity.y -= forceY
                        ball.velocity.x += forceX
                        ball.velocity.y += forceY