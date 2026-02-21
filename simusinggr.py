import numpy as np
import matplotlib.pyplot as plt
import pygame
pygame.init()

#=-=-=-=-=-=-=-=-=-=window setup-=-=-=-=-=-=-=-=-=-=-=-=-

width, height = 1200, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("gravity simulation")
centre = np.array([width/2, height/2])

#=-=-=-=-=-=-=-=-=-=-=constants-=-=-=-=-=-=-=-=-=-=-=-=-=-

G = 6.67430e-11
scale = 250 / (1 * 1.496e11) # 1 AU = 1.496e11 m, scale to fit in window
dt = 1*60*60*24 #timestep for one frame/calculation

#-=-=-=-=-=-=-=-=-=classes=-=-=-=-=-=-=-=-=-=-=-=--=-=-

class space_time:
    def __init__(self, unit_size = 20):
        self.unit_size = unit_size

        X = np.arange(0, width + self.unit_size, self.unit_size)
        Y = np.arange(0, height + self.unit_size , self.unit_size)

        self.x, self.y = np.meshgrid(X, Y)
        self.points = np.column_stack((self.x.flatten(), self.y.flatten()))
        
        
    def draw(self, window):
        # for i in range(len(self.points)): #for displaying the actual dots
        #     pygame.draw.circle(window, (80,80,80), self.points[i], 1)
        
        for i in range(self.x.shape[0]-1):
            for j in range(self.x.shape[1]-1):
                pygame.draw.line(window, (80,80,80), (self.x[i][j], self.y[i][j]), (self.x[i+1][j],self.y[i+1][j])) # x
                pygame.draw.line(window, (80,80,80), (self.x[i][j], self.y[i][j]), (self.x[i][j+1],self.y[i][j+1])) # y

    def bending(self, objects):
        for object in objects:
            i = 0
        pass

class object:
    def __init__(self, mass, radius, position = np.array([0, 0], dtype = float), velocity = np.array([0, 0], dtype = float), colour = (255, 255, 255)):
        self.mass = mass
        self.radius = radius # radius in meters but will be scaled for visualisation
        self.position = np.array(position, dtype = float)
        self.velocity = np.array(velocity, dtype = float)
        self.colour = colour
        self.acceleration = np.array([0, 0], dtype = float)
    
    def gravitational_acceleration(self, others):
        acceleration = np.array([0, 0], dtype = float)
        for other in others:
            if other is self:
                continue
            r_vector = (other.position - self.position)
            r_magnitude = np.linalg.norm(r_vector)

            if r_magnitude == 0:
                continue # avoid division by zero
            
            force_magnitude = G * self.mass * other.mass / r_magnitude**2
            force_direction = r_vector / r_magnitude

            acceleration += force_magnitude * force_direction / self.mass
        return acceleration
    
    def update_position(self, others):
        self.acceleration = self.gravitational_acceleration(others)
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

    def draw(self, window):
        position = (int(self.position[0] * scale + centre[0]), int((self.position[1]) * scale + centre[1]))
        pygame.draw.circle(window, self.colour, position, int(self.radius))
            
class photon:
    def __init__(self, position = np.array([-2e11, -2e11], dtype = float), direction = np.array([1,1], dtype = float)):
        self.position = np.array(position, dtype= float)
        self.direction = np.array(direction, dtype = float)
        norm = np.linalg.norm(self.direction)
        self.velocity = 3e4 * np.array(self.direction/norm)
    
    def draw(self, window):
        self.position += self.velocity * dt
        position = (int(self.position[0] * scale + centre[0]), int((self.position[1]) * scale + centre[1]))
        pygame.draw.circle(window, (255,0,0), position, 5)

#-=-=-=-=-=-=-=-=-=-main-=-=-=-=-=-=-=-=-=-=-=-=

spacetime = space_time()
photon = photon()

def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        window.fill((0, 0, 0))
        photon.draw(window)

        spacetime.draw(window)
        
        pygame.display.flip()

    pygame.quit()

main()