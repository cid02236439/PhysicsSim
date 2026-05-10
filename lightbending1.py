"""
#4
THIS SIMULATION IS INCOMPLETE AND NOT FULLY PHYSICALLY ACCURATE.
THE dλ IS TAKEN AS dt. --> check this
THE GR EQUATIONS USED ARE FROM EFFECTIVE POTENTIAL FORMULATION WHICH WORKS FOR FAR PHOTONS I THINK.
MAYBE COULD BE IMPROVED BY FIXING STEP INTEGRATION AND THE IF STATEMENT IN BEND FUNCTION. 
"""

import numpy as np
import matplotlib.pyplot as plt
import pygame
import random
pygame.init()


width, height = 1200, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("gravity simulation")
centre = np.array([width/2, height/2], dtype = float)
font = pygame.font.SysFont(None, 48)


dt = 100*60*60*24                   #timestep for one frame/calculation
scale = 500 / (0.01 * 1.496e11)     # 1 AU = 1.496e11 m, scale to fit in window
G = 6.67430e-11
c = 299792458

scaled_width, scaled_height = width/scale, height/scale
scaled_centre = centre /scale

left   = (0 - centre[0]) / scale
right  = (width - centre[0]) / scale
top    = (0 - centre[1]) / scale
bottom = (height - centre[1]) / scale

class object:
    def __init__(self,window, mass):
        self.window = window
        self.mass = mass
        self.r_s = 2 * G * self.mass / (c*c)

    def display(self):
        pygame.draw.circle(self.window, (255,255,255), centre, self.r_s * scale)
        pygame.draw.circle(self.window, (100,100,100), centre, self.r_s * scale * 3, 1)
        pygame.draw.circle(self.window, (100,100,100), centre, self.r_s * scale * 1.5, 1)

blackhole = object(window, 1e35)


class photon:                       #introduces 3 variables: self.position, self.direction, self.velocity
    def __init__(self, window,mass, position = np.array([-2e9, 0], dtype = float), direction = np.array([1,0], dtype = float)):
        self.window = window
        self.position = np.array(position, dtype = float)
        self.direction = np.array(direction, dtype = float)
        norm = np.linalg.norm(self.direction)
        self.velocity = c * np.array(self.direction/norm)
        self.trail = []
        self.max_trail_length = 100
        self.out_of_bounds = False
        self.mass = mass
        self.sign = -1 if np.dot(self.position,self.direction) < 0 else 1

        self.r = np.sqrt(self.position[0] * self.position[0] + self.position[1] * self.position[1])
        self.phi = np.arctan2(self.position[1], self.position[0])

        cross = self.position[0] * self.velocity[1] - self.position[1] * self.velocity[0]
        self.b = cross / c

    def display(self):              #modifies 1 variable: self.position
        #self.position += self.velocity * dt
        self.bend()
        
        self.check_boundary()
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

    def bend(self):
        r_s = self.mass.r_s
        inside = 1 - (1 - r_s/self.r) * self.b*self.b / (self.r*self.r)

        if inside < 0:
            inside *= -1
            self.sign *= -1

        self.r += ((1 - r_s/self.r) * np.sqrt(inside)) * dt * self.sign
        self.phi += self.b * (1 - r_s/ self.r) / (self.r*self.r) * dt

        self.position[0] = self.r * np.cos(self.phi)
        self.position[1] = self.r * np.sin(self.phi)

    def check_boundary(self):
        dx = self.position[0]
        dy = self.position[1]
        r_s = self.mass.r_s
        if (dx*dx + dy*dy) < (r_s*r_s + 0.1*r_s*r_s):
            self.out_of_bounds = True
        left   = (0 - centre[0]) / scale
        right  = (width - centre[0]) / scale
        top    = (0 - centre[1]) / scale
        bottom = (height - centre[1]) / scale
        if right < self.position[0] or self.position[0] < left-100 or self.position[1] < top-100 or self.position[1] > bottom+100:
            self.out_of_bounds = True

def make_photons(number=10, randomise = True):
    photons = []
    if not randomise:
        positions = np.linspace(-height/2, height/2, number)
        for i in range(number):
            photons.append(photon(window,blackhole, position = np.array([left, positions[i] / scale], dtype = float)))
    else:
        for i in range(number):
            positionx = random.randrange(int(-width/2),int(width/2)) / scale
            positiony = random.randrange(int(-height/2),int(height/2)) / scale
            direction = (random.uniform(-1,1), random.uniform(-1,1))
            photons.append(photon(window,blackhole, position = (positionx, positiony), direction = direction))
    return photons


def main():
    num_photons, randomise = 200, 1 
    photons = make_photons(num_photons, randomise)
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        window.fill((0,0,0))


        blackhole.display()
        text = font.render(str(len(photons)), True, (255,255,255))
        if len(photons) < num_photons:
            photons.extend(make_photons(num_photons-len(photons), randomise))
        window.blit(text, (10, 10))
        photons = [photon for photon in photons if not photon.out_of_bounds]
        for photon in photons:
            photon.display()


        pygame.display.flip()
    pygame.quit()

main()