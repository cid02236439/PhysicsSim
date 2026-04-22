import numpy as np
import matplotlib.pyplot as plt
import pygame
import random
pygame.init()


width, height = 1200, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("gravity simulation")
centre = np.array([width/2, height/2], dtype = float)


dt = 1*60*60*24                     #timestep for one frame/calculation
scale = 500 / (0.01 * 1.496e11)     # 1 AU = 1.496e11 m, scale to fit in window
G = 6.67430e-11
c = 299792458


class object:
    def __init__(self,window, mass):
        self.window = window
        self.mass = mass
        self.r_s = 2 * G * self.mass / (c*c)

    def display(self):
        pygame.draw.circle(self.window, (255,255,255), centre, self.r_s * scale)

blackhole = object(window, 1e35)


class photon:                       #introduces 3 variables: self.position, self.direction, self.velocity
    def __init__(self, window, position = np.array([-2e9, 0], dtype = float), direction = np.array([1,0], dtype = float)):
        self.window = window
        self.position = np.array(position, dtype = float)
        self.direction = np.array(direction, dtype = float)
        norm = np.linalg.norm(self.direction)
        self.velocity = 3e2 * np.array(self.direction/norm)
        self.trail = []
        self.max_trail_length = 100

    def display(self):              #modifies 1 variable: self.position
        self.position += self.velocity * dt
        self.trail.append(self.position.copy()) #store tail
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

        for i in range(len(self.trail) - 1):    #tail fading algorithm
            fade = i / len(self.trail)
            colour = ( int(255* fade), 0, 0)
            pos1 = (int(self.trail[i][0] * scale + centre[0]), int(self.trail[i][1] * scale + centre[1]))
            pos2 = (int(self.trail[i+1][0] * scale + centre[0]), int(self.trail[i+1][1] * scale + centre[1]))
            pygame.draw.line(self.window, colour, pos1, pos2, 2)

        position = (int(self.position[0] * scale + centre[0]), int((self.position[1]) * scale + centre[1]))
        pygame.draw.circle(self.window, (255,0,0), position, 2)
    
    def check_boundary(self):
        if self.position[0] > 2e9 or self.position[0] < -2e9 :
            


def make_photons(number=10, randomise = True):
    photons = [] 
    if not randomise:
        positions = np.linspace(-height/2, height/2, number)
        for i in range(number):
            photons.append(photon(window, position = np.array([-2e9, positions[i] / scale], dtype = float)))
    else:
        for i in range(number):
            positionx = random.randrange(int(-width/2),int(width/2)) / scale
            positiony = random.randrange(int(-height/2),int(height/2)) / scale
            direction = (random.uniform(-1,1), random.uniform(-1,1))
            photons.append(photon(window, position = (positionx, positiony), direction = direction))

    return photons

photons = make_photons(300)


def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        window.fill((0,0,0))
        
        
        blackhole.display()
        for i in range(len(photons)):
            photons[i].display()


        pygame.display.flip()
    pygame.quit()

main()
