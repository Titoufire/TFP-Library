import pygame
from objects.line import Line

Vec2 = pygame.math.Vector2

class Rigid_Body():
    
    def __init__(self, color: str, pos: tuple, velocity: tuple, vertices: list, edge_color=None, edge_thickness=1, fric=0, rest=1, fixed=False, lines=None):
        self.color = color
        self.edge_color = edge_color
        if edge_color == None:
            self.edge_color = self.color
        self.edge_thickness = edge_thickness
        if len(vertices) < 3:
            raise ValueError(f"[tfp] Rigid_Body MUST have at least 3 vertices !!! {len(vertices)} were given\n Use Line() instead")
        self.rel_vertices = vertices
        self.abs_vertices = []
        self.faces = []
        self.pos = Vec2(pos[0], pos[1])
        self.velocity = Vec2(velocity[0], velocity[1])
        self.acceleration = Vec2(0, 0)
        self.angle = 0
        self.ang_vel = 0
        self.ang_acc = 0
        self.restitution = rest
        self.friction = fric
        self.fixed = fixed
        
        if fixed:
            try:
                self.calc_vertices()
                self.calc_faces(lines)
            except: raise ValueError(f"[tfp] Fixed Rigid_Body must receive the 'lines' argument. None was given.\n please fill the 'lines' argument with the list of lines in-world")
    
    def simulate(self, dt, gravity, lines):
        if not self.fixed:
            #apply gravity
            self.acceleration += gravity
        
            #update position and all with dt
            self.velocity += self.acceleration * dt
            self.pos += self.velocity*0.5 * dt
            self.acceleration = Vec2(0, 0)
            self.ang_vel += self.ang_acc * dt
            self.angle += self.ang_vel*0.5 * dt
            self.ang_acc = 0
        
            #calculate absolute vertices and faces
            self.calc_vertices()
            self.calc_faces(lines)
        
        #collision detection and resolution
        #only collisions with other rigid bodies and lines.
        self.collide_lines(lines)
        self.collide_rigids() #unset
        
        #second half of movement update
        if not self.fixed:
            self.pos += self.velocity*0.5 * dt
            self.angle += self.ang_vel*0.5 * dt
            
    def collide_lines(self, lines):
        #collision detection
        for line in lines:
            if not line in self.faces:
                distribution = []
                for vertice in self.abs_vertices:
                    distribution.append((vertice.x-line.pos.x)*line.normal.x + (vertice.y-line.pos.y)*line.normal.y)
                if min(distribution) < 0 and max(distribution) > 0:
                    #potential collision
                    positions = ()
                    for vertice in self.abs_vertices:
                        position = (vertice.x-line.pos.x)*-line.normal.y + (vertice.y-line.pos.y)*line.normal.x
                        if 0 <= position <= line.length:
                            positions.append(vertice)
                    if positions:
                        self.handle_line_collision(line, positions=positions)
                        
    def handle_line_collision(self, line, positions=None):
        #collision resolution
        print("collision")
        col_friction = self.friction*line.friction
        col_restitution = self.restitution*line.restitution
    
    def collide_rigids(self): #unused
        pass
        
    def calc_vertices(self):
        self.abs_vertices.clear()
        for vertice in self.rel_vertices:
            self.abs_vertices.append(vertice+self.pos)
        
    def calc_faces(self, lines):
        #clear old faces
        for face in self.faces:
            try:
                lines.remove(face)
            except: pass
        self.faces.clear()
        
        #generate new faces
        point = [None, None]
        for vertice in self.abs_vertices:
            point.append(vertice)
            point.pop(0)
            if None == point[0]:
                point0 = vertice
            else:
                self.faces.append(Line(self.edge_color, point[0], point[1]))
        self.faces.append(Line(self.edge_color, point[1], point0))
        
        #export faces
        for line in self.faces:
            lines.append(line)
            
    def draw(self, screen):
        #draw polygon then draw edges
        pygame.draw.polygon(screen, self.color, self.abs_vertices)