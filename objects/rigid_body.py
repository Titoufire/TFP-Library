import pygame
from objects.line import Line

Vec2 = pygame.math.Vector2

class Rigid_Body():
    
    def __init__(self, color: str, pos: tuple, velocity: tuple, vertices: list, edge_color=None, edge_thickness=1, fric=0, rest=1, fixed=False, rigid_lines=None):
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
        self.position_tracker = 100 #number of positions tracked
        self.positions = [] #for position tracker
        
        if fixed:
            try:
                self.calc_vertices()
                self.calc_faces(rigid_lines)
            except: raise ValueError(f"[tfp] Fixed Rigid_Body must receive the 'rigid_lines' argument. None was given.\n please fill the 'rigid_lines' argument with the list of lines in-world")
    
    def simulate(self, dt, gravity, lines, rigids):
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
            self.collide_rigids(rigids) #unset
        
            #second half of movement update
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
                    vertices = []
                    for vertice in self.abs_vertices:
                        position = (vertice.x-line.pos.x)*-line.normal.y + (vertice.y-line.pos.y)*line.normal.x
                        if 0 <= position <= line.length:
                            if (vertice.x-line.pos.x)*line.normal.x + (vertice.y-line.pos.y)*line.normal.y < 0:
                                #collision detected
                                vertices.append(vertice)
                    if vertices:
                        self.resolve_line_collision(line, vertices)
                        
    def resolve_line_collision(self, line, vertices):
        #collision resolution
        print("collision")
        col_friction = self.friction*line.friction
        col_restitution = self.restitution*line.restitution
        depths = []
        for vertice in vertices:
            depths.append((vertice.x-line.pos.x)*line.normal.x + (vertice.y-line.pos.y)*line.normal.y)
        print(vertices)
        print(depths)
        total_depth = sum(depths)
        try:
            vert1 = {"depth_frac": total_depth/depths[0], "pos": vertices[0], "depth": depths[0], "vel": self.velocity*self.ang_vel*((vertices[0]-self.pos).length()), "r": vertices[0]-self.pos}
            vert2 = {"depth_frac": total_depth/depths[1], "pos": vertices[1], "depth": depths[1], "vel": self.velocity*self.ang_vel*((vertices[1]-self.pos).length()), "r": vertices[1]-self.pos}
        except IndexError: pass
        for i in range(len(vertices)):
            vertice = vertices[i]
            depth = depths[i]
            #resolve collision
            '''if not self.fixed:
                self.pos += line.normal * (depth/total_depth) * -total_depth
                self.velocity -= line.normal * (self.velocity.x*line.normal.x + self.velocity.y*line.normal.y) * (1+col_restitution)
                self.velocity -= self.velocity * col_friction
                #angular velocity resolution
                r = vertice - self.pos
                torque = r.cross(line.normal * (self.velocity.x*line.normal.x + self.velocity.y*line.normal.y))
                moment_of_inertia = 0
                for vertice in self.abs_vertices:
                    r = vertice - self.pos
                    moment_of_inertia += r.length_squared()
                if moment_of_inertia != 0:
                    self.ang_vel += torque/moment_of_inertia'''
        '''#calculate impulse
        j = -(1+col_restitution) * (vert1["vel"]-vert2["vel"]).dot(line.normal) / ((vert1["r"]*line.normal)**2 /vert1["r"].length_squared())
        #solve for vert1
        vert1["vel"] -= j*line.normal*vert1["depth_frac"]
        vert1["vel"] -= vert1["vel"] * col_friction
        vert2["vel"] += j*line.normal*vert2["depth_frac"]
        vert2["vel"] -= vert2["vel"] * col_friction
        #update rigid body velocity and angular velocity
        self.velocity = (vert1["vel"]+vert2["vel"])/2'''
        for i in range(len(vertices)):
            vertice = vertices[i]
            depth = depths[i]
            norm_speed = self.velocity.x*line.normal.x + self.velocity.y*line.normal.y
            tang_speed = self.velocity.x*line.normal.y + self.velocity.y*-line.normal.x
            if norm_speed <= 0:
                self.velocity.x = -(norm_speed*line.normal.x)*col_restitution +(tang_speed*line.normal.y)*(1-col_friction)
                self.velocity.y = -(norm_speed*line.normal.y)*col_restitution +(tang_speed*-line.normal.x)*(1-col_friction)
    
    def collide_rigids(self, rigids): #unused
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

        #position tracker
        self.positions.append((self.pos[0], self.pos[1]))
        if len(self.positions) > self.position_tracker:
            self.positions.pop(0)
        for pos in self.positions:
            pygame.draw.circle(screen, 'red', pos, 1)