import pygame
from Tfp.objects.line import Line

Vec2 = pygame.math.Vector2

class Rigid_Body():

    rigids: list[Rigid_Body] = []
    def __init__(self):

        self.abs_vertices = []
        self.faces = []
        '''self.color = self.edge_color = self.edge_thickness = self.rel_vertices = self.pos = self.velocity = None
        self.acceleration = self.angle = self.ang_vel = self.ang_acc = self.restitution = self.friction = None
        self.fixed = self.position_tracker = self.positions = self.shape = self.mass = self.inv_mass = None
        self.height = self.width = self.inertia = self.inv_inertia = self.collision_manifold = self.mass_center = None'''

        Rigid_Body.rigids.append(self)

    def build_from_points(color: str | pygame.Color, pos: tuple[int, int], velocity: tuple[int, int],
                          vertices: list[tuple[int, int]], edge_color=None, edge_thickness=1, fric=0, rest=1, fixed=False,
                          shape="custom", mass=1, height=None, width=None):
        body = Rigid_Body()
        body.color = color
        body.edge_color = edge_color
        if edge_color == None:
            body.edge_color = body.color
        body.edge_thickness = edge_thickness
        if len(vertices) < 3:
            raise ValueError(f"[tfp] Rigid_Body MUST have at least 3 vertices !!! {len(vertices)} were given\n Use Line() instead")
        body.rel_vertices = vertices
        body.pos = Vec2(pos[0], pos[1])
        body.velocity = Vec2(velocity[0], velocity[1])
        body.acceleration = Vec2(0, 0)
        body.angle, body.ang_vel, body.ang_acc = 0, 0, 0
        body.restitution = rest
        body.friction = fric
        body.fixed = fixed
        body.position_tracker = 100 #number of positions tracked
        body.positions = [] #for position tracker
        body.shape = shape
        body.mass = mass
        body.inv_mass = 1/mass
        body.height = height
        body.width = width
        if fixed:
            body.inv_mass = 0
        body.collision_manifold = (None, None)
        body.mass_center = body.pos

        body.calc_vertices()
        body.calc_faces()
        body.calc_inertia()

        return body

    def simulate(self, dt: float, gravity: Vec2):
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
            self.collide_lines()
            self.collide_rigids()
        
            #second half of movement update
            self.pos += self.velocity*0.5 * dt
            self.angle += self.ang_vel*0.5 * dt

    #the following three functions are for collision detection and resolution with lines.
    #collisions with other rigid bodies are handled by the next three functions. 
    def collide_lines(self):
        lines = Line.lines
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
        col_friction = self.friction*line.friction
        col_restitution = self.restitution*line.restitution
        depths = []
        for vertice in vertices:
            depths.append((vertice.x-line.pos.x)*line.normal.x + (vertice.y-line.pos.y)*line.normal.y)
        total_depth = sum(depths)
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
                try:
                    res_lin_vel[i] = r.dot(Vec2(res_vel_x, res_vel_y))*line.normal
                    res_ang_vel[i] = r.dot(Vec2(-res_vel_y, res_vel_x))
                except IndexError:
                    print(vertices)

        try:
            if norm_speeds[0] < 0 and norm_speeds[1] < 0:
                self.apply_line_collision(res_ang_vel, res_lin_vel)
            else:
                pass
        except IndexError: pass

    def apply_line_collision(self, res_ang_vel: list[float], res_lin_vel: list[Vec2]):
        #applying collision resolution
        added_vel = res_lin_vel[0]
        try:
            added_vel += res_lin_vel[1]
        except: pass
        #added_vel *= 1.4142
        added_vel *= 1.2
        self.velocity += added_vel#/len(res_lin_vel)
        self.ang_vel += sum(res_ang_vel)

    #the following three functions are for collision detection and resolution with other rigid bodies.        
    def collide_rigids(self):

        # using the separating axis theorem (SAT)
        rigids = Rigid_Body.rigids
        for rigid in rigids:
            if rigid != self:
                #reset collision_manifold
                self.collision_manifold = [None, None]

                #iterate for all rigid body pairs
                all_faces = rigid.faces.copy() + self.faces.copy()
                abandoned = False
                normal_lengths = []
                edges = []
                for face in all_faces:

                    #do the projection calculations for all faces
                    self_distri = []
                    other_distri = []
                    for vertice in self.abs_vertices:
                        self_distri.append(((vertice.x - face.pos.x)*face.normal.x + (vertice.y - face.pos.y)*face.normal.y))
                    for vertice in rigid.abs_vertices:
                        other_distri.append(((vertice.x - face.pos.x)*face.normal.x + (vertice.y - face.pos.y)*face.normal.y))
                    self_bounds = (min(self_distri), max(self_distri))
                    other_bounds = (min(other_distri), max(other_distri))
                    if self_bounds[1] < other_bounds[0]:
                        abandoned = True
                        break
                    elif other_bounds[1] < self_bounds[0]:
                        abandoned = True
                        break
                    else:
                        if other_bounds[1] > 0 and self_bounds[0] < 0:
                            #print("line middle: ", self_bounds, other_bounds, face.owner.fixed, face.normal)
                            penetration = min(
                                self_bounds[1]-other_bounds[0],
                                other_bounds[1]-self_bounds[0])
                            normal_lengths.append(penetration)
                            edges.append(face)

                #once every projection for every face has been calculated
                if not abandoned:
                    #if there is collision
                    Vrel = rigid.velocity - self.velocity
                    self.color = "red"
                    #calculate shortest penetration: that will be our normal vector for the collision
                    #index = normal_lengths.index(min(normal_lengths))
                    indices = [i for i, x in enumerate(normal_lengths) if x == min(normal_lengths)]
                    index = indices[0]
                    lowest_normal = edges[index].normal
                    edge = edges[index]
                    Vnormal = lowest_normal.normalize().dot(Vrel)
                    if Vnormal <= 0:
                        self.resolve_rigid_collision(rigid, lowest_normal, Vrel, Vnormal, edge)
                    else:
                        print("Abandonned collision. Reason: moving away")
                else:
                    #if no collision
                    self.color = "green"

    def resolve_rigid_collision(self, rigid: Rigid_Body, normal: Vec2, Vrel: Vec2, Vnormal: float, ref_edge: Line):
        #It's formula time !
        #First, let's get the reference polygon and edge, and incident polygon and edge
        ref_poly = ref_edge.owner
        if ref_poly == self:
            inc_poly = rigid
        else:
            inc_poly = self
        print("ref_poly fixed:", ref_poly.fixed)
        oppositions = []
        for edge in inc_poly.faces:
            oppositions.append(edge.normal.dot(normal))
        inc_edge = inc_poly.faces[oppositions.index(min(oppositions))]

        #let's calculate the collision manifold (1 or two points considered in collision resolution)
        #first, clip the inc edge, to only consider the points between the end points of the ref edge
        #check both inc edge endpoints
        relative = ref_edge.pos
        p = Vec2(-normal.y, normal.x) #edge tangent vector
        start = p.dot(inc_edge.pos-relative)
        end = p.dot(inc_edge.end-relative)
        end_points = [None, None]
        if start >= 0 and end >= 0:
            if start <= ref_edge.length and end <= ref_edge.length:
                end_points = [inc_edge.end, inc_edge.pos]
            elif start <= ref_edge.length and end > ref_edge.length:
                end_points[1] = inc_edge.pos
            elif start > ref_edge.length and end <= ref_edge.length:
                end_points[0] = inc_edge.end
        elif start >= 0 and end < 0:
            if start <= ref_edge.length:
                end_points[1] = inc_edge.pos
        elif start < 0 and end >= 0:
            if end <= ref_edge.length:
                end_points[0] = inc_edge.end
        else:
             print("no collision ?")

        #now calculate the cliped point(s) is there is any
        if end_points[0] == None:
            #calculate the clipped point
            rel_vec: Vec2 = ref_edge.pos - inc_edge.pos
            ptA = inc_edge.pos + rel_vec.dot(inc_edge.norm_dir)*inc_edge.norm_dir
            end_points[0] = ptA
        if end_points[1] == None:
            #calculate the clipped point
            rel_vec: Vec2 = ref_edge.end - inc_edge.end
            ptB = inc_edge.end + rel_vec.dot(inc_edge.norm_dir)*inc_edge.norm_dir
            end_points[1] = ptB

        #calculate if end points are behind the edge normal and add them to collision manifold
        if (end_points[0] - ref_edge.pos).dot(normal) <= 0:
            self.collision_manifold[0] = end_points[0]
            if (end_points[1] - ref_edge.pos).dot(normal) <= 0:
                self.collision_manifold[1] = end_points[1]
        else:
            if (end_points[1] - ref_edge.pos).dot(normal) <= 0:
                self.collision_manifold[0] = end_points[1]

        print("manifold:", self.collision_manifold)

        #point = Vec2(coords)
        #collision manifold now equals: [point, point] or [point, None]
        if self.collision_manifold[1] == None:
            self.collision_manifold = [self.collision_manifold[0]]

        #collision manifold now equals: [points, point] or [point]
        penetrations = []
        for point in self.collision_manifold:
            penetrations.append((point - ref_edge.pos).dot(ref_edge.normal))
        if penetrations[-1] >= 0:
            penetrations.pop(-1)
            self.collision_manifold.pop(-1)
        if penetrations[0] >= 0:
            penetrations.pop(0)
            self.collision_manifold.pop(0)

        #reset manifold is both penetration yield 0 (preventing division by zero later)
        if self.collision_manifold == []:
            self.collision_manifold = [None, None]
            return

        scalar_impulses = []
        col_rest = ref_poly.restitution + inc_poly.restitution
        total_penetration = sum(penetrations)
        for i in range(len(self.collision_manifold)):
            point = self.collision_manifold[i]
            #calculate variables
            ra = point - ref_poly.mass_center
            rb = point - inc_poly.mass_center
            #Vpa = ref_poly.velocity + (-ref_poly.ang_vel * ra.y, ref_poly.ang_vel * ra.x)
            #Vpb = inc_poly.velocity + (-inc_poly.ang_vel * rb.y, inc_poly.ang_vel * rb.x)
            Vpa = (ref_poly.velocity+ref_poly.ang_vel*ra)
            Vpb = (inc_poly.velocity+inc_poly.ang_vel*rb)
            vrel = Vpb - Vpa
            #calculate scalar impulses
            #denominator = (ref_poly.inv_mass + inc_poly.inv_mass +
                           #((ra*normal)**2)/ref_poly.inertia + ((rb*normal)**2)/inc_poly.inertia)
            denominator = (ref_poly.inv_mass + inc_poly.inv_mass +
                            ((ra*normal)**2)*ref_poly.inv_inertia + 
                            ((rb*normal)**2)*inc_poly.inv_inertia)
            J = ( -(1+col_rest)*vrel.dot(normal) ) / denominator
            scalar_impulses.append(J)
            #weight scalar impulses with penetration
            relative_penetration = penetrations[i]/total_penetration
            J *= relative_penetration

        #resolve collision
        print("result impulses", scalar_impulses)
        self.apply_rigid_collision(scalar_impulses, ref_poly, inc_poly, normal)

    def apply_rigid_collision(self, scalar_impulse: Vec2, ref_poly: Rigid_Body, inc_poly: Rigid_Body, normal: Vec2):
        #process both points again
        print("")
        ref_vel, inc_vel, ref_ang_vel, inc_ang_vel = [Vec2(0, 0), Vec2(0, 0)], [Vec2(0, 0), Vec2(0, 0)], [0, 0], [0, 0]
        for i in range(len(self.collision_manifold)):
            point = self.collision_manifold[i]
            print("considered point is:", point)
            J = scalar_impulse[i]
            ra = point - ref_poly.mass_center
            rb = point - inc_poly.mass_center
            print("ra:", ra)
            print("normal vector:", normal)
            Vpa = (ref_poly.velocity+ref_poly.ang_vel*ra)
            Vpb = (inc_poly.velocity+inc_poly.ang_vel*rb)
            vrel = Vpb - Vpa
            #both above variables are nominal, therefore the only untested common variable is J...
            ref_vel[i] = ref_poly.velocity - (J*ref_poly.inv_mass) * normal
            inc_vel[i] = inc_poly.velocity + (J*inc_poly.inv_mass) * normal
            print("ra*normal:", ra*normal)
            ref_ang_vel[i] = ref_poly.ang_vel - (J*(ra*normal.rotate(90)))*ref_poly.inv_inertia
            inc_ang_vel[i] = inc_poly.ang_vel + (J*(rb*normal.rotate(90)))*inc_poly.inv_inertia

        print("")
        print("ref_vel:", ref_vel, "compared to:", ref_poly.velocity)
        print("ref_ang_vel:", ref_ang_vel, "compared to:", ref_poly.ang_vel)
        fin_ref_vel = ref_vel[0]+ref_vel[1]  #sum doesn't work because items are Vec2
        fin_inc_vel = inc_vel[0]+inc_vel[1]  #sum doesn't work because items are Vec2
        fin_ref_ang = sum(ref_ang_vel)
        fin_inc_ang = sum(inc_ang_vel)
        print("final velocities:", fin_ref_vel, fin_inc_vel, "/", fin_ref_ang, fin_inc_ang)
        ref_poly.velocity = fin_ref_vel
        inc_poly.velocity = fin_inc_vel
        ref_poly.ang_vel = -fin_ref_ang
        inc_poly.ang_vel = -fin_inc_ang
        print("-"*50)
        
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
                self.faces.append(Line(self.edge_color, point[0], point[1], dont_self=True, owner=self))
        self.faces.append(Line(self.edge_color, point[1], point0, dont_self=True, owner=self))

    def calc_inertia(self):
        if self.shape == "rectangle":
            self.inertia = (1/12) * self.mass * (self.height**2 + self.width**2)
            self.inv_inertia = 1/self.inertia
        elif self.shape == "custom":
            # here will be heavy double integral calculation of moment of inertia
            # r = sqrt(x**2 + y**2)   r**2 = X**2 + Y**2   #distance relative to center of mass
            # SS-max(r)->max(r) (m/v)*r**2 dxdy
            # I = 1/12 * ∑k=0/n−1 (Xk*Yk+1 − Xk+1Yk)(xk+1**2 + Xk+1Xk + Xk**2 + Yk+1**2 + Yk+1Yk + Yk**2)
            # ???
            pass
        if self.fixed:
            self.inv_inertia = 0
            
    def draw(self, screen: pygame.Surface, camera):
        screen_vertices = []
        for vertice in self.abs_vertices:
            screen_vertices.append(((vertice.x+camera.pos[0])*camera.zoom, (vertice.y+camera.pos[1])*camera.zoom))
        #draw polygon then draw edges
        pygame.draw.polygon(screen, self.color, screen_vertices)
        for i in range(len(screen_vertices)):
            pygame.draw.line(screen, self.edge_color, screen_vertices[i], screen_vertices[(i+1)%len(screen_vertices)],
                             max(round(self.edge_thickness*camera.zoom), 1))

        #position tracker
        self.positions.append((self.pos[0], self.pos[1]))
        if len(self.positions) > self.position_tracker:
            self.positions.pop(0)
        for pos in self.positions:
            track_pos = ((pos[0]+camera.pos[0])*camera.zoom, (pos[1]+camera.pos[1])*camera.zoom)
            pygame.draw.circle(screen, 'red', track_pos, 1)

        #collision manifold tracker
        if self.collision_manifold[0] != None:
            pos = self.collision_manifold[0]
            col_pos = ((pos[0]+camera.pos[0])*camera.zoom, (pos[1]+camera.pos[1])*camera.zoom)
            pygame.draw.circle(screen, 'yellow', col_pos, 3*camera.zoom)
        try:
            if self.collision_manifold[1] != None:
                pos = self.collision_manifold[1]
                col_pos = ((pos[0]+camera.pos[0])*camera.zoom, (pos[1]+camera.pos[1])*camera.zoom)
                pygame.draw.circle(screen, 'yellow', col_pos, 3*camera.zoom)
        except: pass