import pygame
from Tfp.objects.line import Line

Vec2 = pygame.math.Vector2

class Rigid_Body():
    
    def __init__(self, color: str | pygame.Color, pos: tuple[int, int], velocity: tuple[int, int], vertices: list[tuple[int, int]],
                 edge_color=None, edge_thickness=1, fric=0, rest=1, fixed=False):
        
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
            self.calc_vertices()
            self.calc_faces()

    def simulate(self, dt: float, gravity: Vec2, rigids: list[Rigid_Body]):
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
            self.calc_faces()
        
            #collision detection and resolution
            #only collisions with other rigid bodies and lines.
            self.collide_lines(Line.lines)
            self.collide_rigids(rigids) #unset
        
            #second half of movement update
            self.pos += self.velocity*0.5 * dt
            self.angle += self.ang_vel*0.5 * dt

    #the following three functions are for collision detection and resolution with lines.
    #collisions with other rigid bodies are handled by the next three functions. 
    def collide_lines(self, lines: list[Line]):
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
                        
    def resolve_line_collision(self, line: Line, vertices: list[Vec2]):
        #collision resolution
        print("\nline collision")
        col_friction = self.friction*line.friction
        col_restitution = self.restitution*line.restitution
        depths = []
        for vertice in vertices:
            depths.append((vertice.x-line.pos.x)*line.normal.x + (vertice.y-line.pos.y)*line.normal.y)
        print(f"self.velocity: {self.velocity} / {self.ang_vel}")
        #print(f"vertices: {vertices}")
        #print(f"depths: {depths}")
        total_depth = sum(depths)
        try:
            vert1 = {"depth_frac": total_depth/depths[0], "pos": vertices[0], "depth": depths[0], "vel": self.velocity*self.ang_vel*((vertices[0]-self.pos).length()), "r": vertices[0]-self.pos}
            vert2 = {"depth_frac": total_depth/depths[1], "pos": vertices[1], "depth": depths[1], "vel": self.velocity*self.ang_vel*((vertices[1]-self.pos).length()), "r": vertices[1]-self.pos}
        except IndexError: pass
        res_ang_vel = [0, 0]
        res_lin_vel = [0, 0]
        norm_speeds = []
        for i in range(len(vertices)):
            vertice = vertices[i]
            depth = depths[i]
            rel_depth = 2 *depth/total_depth
            r = vertice - self.pos
            norm_speed = self.velocity.x*line.normal.x + self.velocity.y*line.normal.y
            tang_speed = self.velocity.x*line.normal.y + self.velocity.y*-line.normal.x
            #norm_speed = (self.velocity.x+r.x*self.ang_vel)*line.normal.x + (self.velocity.y+r.y*self.ang_vel)*line.normal.y
            #tang_speed = (self.velocity.x+r.x*self.ang_vel)*line.normal.y + (self.velocity.y+r.y*self.ang_vel)*-line.normal.x
            norm_speeds.append(norm_speed)
            if norm_speed < 0:
                res_vel_x = -(norm_speed*line.normal.x)*col_restitution*rel_depth +(tang_speed*line.normal.y)*(1-col_friction)
                res_vel_y = -(norm_speed*-line.normal.y)*col_restitution*rel_depth +(tang_speed*line.normal.x)*(1-col_friction)
                #angular velocity is the part of the resolution that is perpendicular to the vector to the center of mass.
                #The part that is parallel to the vector to the center of mass is linear velocity.
                r.normalize_ip()
                res_lin_vel[i] = r.dot(Vec2(res_vel_x, res_vel_y))*line.normal
                res_ang_vel[i] = r.dot(Vec2(-res_vel_y, res_vel_x))
        try:
            if norm_speeds[0] < 0 and norm_speeds[1] < 0:
                self.apply_line_collision(res_ang_vel, res_lin_vel)
            else:
                print("abandonned collision")
        except IndexError: print("abandonned collision")

    def apply_line_collision(self, res_ang_vel: list[float], res_lin_vel: list[Vec2]):
        #applying collision resolution
        print(f"res_ang_vel: {res_ang_vel}")
        print(f"res_lin_vel: {res_lin_vel}")
        added_vel = res_lin_vel[0]
        try:
            added_vel += res_lin_vel[1]
        except: pass
        #added_vel *= 1.4142
        added_vel *= 1.2
        print(f"added_vel: {added_vel} / {sum(res_ang_vel)}")
        self.velocity += added_vel#/len(res_lin_vel)
        self.ang_vel += sum(res_ang_vel)
        print(f"updated velocity: {self.velocity} / {self.ang_vel}")

    #the following three functions are for collision detection and resolution with other rigid bodies.        
    def collide_rigids(self, rigids: list[Rigid_Body]): #unused
        pass

    def resolve_rigid_collision(self, rigid: Rigid_Body): #unused
        pass

    def apply_rigid_collision(self, res_ang_vel: list[float], res_lin_vel: list[Vec2]): #unused
        pass
        
    def calc_vertices(self):
        self.abs_vertices.clear()
        for vertice in self.rel_vertices:
            self.abs_vertices.append((Vec2(vertice).rotate(self.angle)+self.pos))
        
    def calc_faces(self):
        lines = Line.rigid_lines
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
                self.faces.append(Line(self.edge_color, point[0], point[1], dont_self=True))
        self.faces.append(Line(self.edge_color, point[1], point0, dont_self=True))
            
    def draw(self, screen: pygame.Surface):
        #draw polygon then draw edges
        pygame.draw.polygon(screen, self.color, self.abs_vertices)

        #position tracker
        self.positions.append((self.pos[0], self.pos[1]))
        if len(self.positions) > self.position_tracker:
            self.positions.pop(0)
        for pos in self.positions:
            pygame.draw.circle(screen, 'red', pos, 1)