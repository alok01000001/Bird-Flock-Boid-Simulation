import pygame, random, math
pygame.init() 

WIDTH, HEIGHT = 800, 600 
NUM_BOIDS = 50
desired_separation=50
NEIGHBOR_RADIUS = 200
MAX_SPEED = 2; MAX_FORCE = 1

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#Mathematical functions for Vector handling
def add(a, b):  return [a[0] + b[0], a[1] + b[1]]
def sub(a, b):  return [a[0] - b[0], a[1] - b[1]]
def mult(a, scalar):   return [a[0] * scalar, a[1] * scalar]
def div(a, scalar):
    if scalar == 0:
        return [0, 0]
    return [a[0] / scalar, a[1] / scalar]
def mag(a):  return math.hypot(a[0], a[1])
def normalize(a):           # make length 1 (if possible)
    m = mag(a)
    if m == 0:
        return [0, 0]
    return [a[0] / m, a[1] / m]
def limit(a, max_val):      # if vector is too long, shorten it
    m = mag(a)
    if m > max_val:
        return mult(normalize(a), max_val)
    return a


#Fn to get neighbors
def get_neighbors(my_boid, all_boids, radius):
    neighbors = []
    for other in all_boids:
        if other is my_boid:
            continue
        dx = other.pos[0] - my_boid.pos[0]
        dy = other.pos[1] - my_boid.pos[1]
        distance = (dx*dx + dy*dy) ** 0.5
        if distance < radius:
            neighbors.append(other)
    return neighbors



class Boid:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.x = x
        self.y = y
        # initial random velocity
        self.vel = [random.uniform(-1,1), random.uniform(-1,1)]
        self.acc = [0.0, 0.0]

    #To scan for seperation
    def separation(self, neighbors):
        steer = [0, 0]
        count = 0
        for other in neighbors:
            dx = self.pos[0] - other.pos[0]
            dy = self.pos[1] - other.pos[1]
            d = (dx*dx + dy*dy) ** 0.5
            if d > 0 and d < desired_separation:
                # direction away inversely proportional to distance
                away = [dx / d, dy / d]
                steer = add(steer, away)
                count += 1
        if count > 0:
            steer = div(steer, count)       # average
            steer = normalize(steer)
            steer = mult(steer, MAX_SPEED)  # wanted velocity
            steer = sub(steer, self.vel)    # steering = desired - current
            steer = limit(steer, MAX_FORCE)
        return steer

    #Alignment with the neighbors
    def alignment(self, neighbors):
        avg = [0, 0]
        count = 0
        for other in neighbors:
            avg = add(avg, other.vel)
            count += 1
        if count > 0:
            avg = div(avg, count)            # average velocity
            avg = normalize(avg)
            avg = mult(avg, MAX_SPEED)
            steer = sub(avg, self.vel)
            steer = limit(steer, MAX_FORCE)
            return steer
        return [0, 0]
    
    #Cohesion with neighbors
    def cohesion(self, neighbors):
        center = [0, 0]
        count = 0
        for other in neighbors:
            center = add(center, other.pos)
            count += 1
        if count > 0:
            center = div(center, count)
            desired = sub(center, self.pos)  # vector toward center
            desired = normalize(desired)
            desired = mult(desired, MAX_SPEED)
            steer = sub(desired, self.vel)
            steer = limit(steer, MAX_FORCE)
            return steer
        return [0, 0]
    
    def apply_force(self, force):
        self.acc = add(self.acc, force)

    def flock(self, boids):
        neighbors = get_neighbors(self, boids, NEIGHBOR_RADIUS)
        sep = self.separation(neighbors)
        ali = self.alignment(neighbors)
        coh = self.cohesion(neighbors)

        # weights (tweak these)
        sep = mult(sep, 1.5)
        ali = mult(ali, 1.0)
        coh = mult(coh, 1.0)

        # apply forces (accumulated)
        self.apply_force(sep)
        self.apply_force(ali)
        self.apply_force(coh)

    def draw(self, surf):
        pygame.draw.circle(surf, (255,255,255), (int(self.pos[0]), int(self.pos[1])), 3)
    
    def edges(self):
        # wrap-around
        if self.pos[0] < 0: self.pos[0] += WIDTH
        if self.pos[0] >= WIDTH: self.pos[0] -= WIDTH
        if self.pos[1] < 0: self.pos[1] += HEIGHT
        if self.pos[1] >= HEIGHT: self.pos[1] -= HEIGHT

    def update(self):
        # velocity changes by acceleration
        self.vel = add(self.vel, self.acc)
        # limit speed
        self.vel = limit(self.vel, MAX_SPEED)
        # position changes by velocity
        self.pos = add(self.pos, self.vel)
        # reset acceleration
        self.acc = [0, 0]
        self.edges()


# ---- setup ----
boids = [Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_BOIDS)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))

    for b in boids:
        b.flock(boids)
    for b in boids:
        b.update()
        b.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()