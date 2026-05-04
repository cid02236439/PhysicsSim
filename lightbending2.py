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
        pygame.draw.circle(self.window, (100,100,100), centre, self.r_s * scale * 3, 1)
        pygame.draw.circle(self.window, (100,100,100), centre, self.r_s * scale * 1.5, 1)

blackhole = object(window, 1e35)


class photon:
    def __init__(self, mass, position, direction):

        self.mass = mass
        self.position = np.array(position, dtype = float)
        self.direction = np.array(direction, dtype = float)
        norm = np.linalg.norm(self.direction)
        self.velocity = c * np.array(self.direction/norm)
        self.out_of_bounds = False

        self.trail = []
        self.max_trail_length = 100
        

        self.r = np.sqrt(self.position[0] * self.position[0] + self.position[1] * self.position[1])
        self.theta = np.arctan2(self.position[1], self.position[0])
        self.dr = self.velocity[0] * np.cos(self.theta) + self.velocity[1] * np.sin(self.theta)
        self.dtheta = (-self.velocity[0] * np.sin(self.theta) + self.velocity[1]* np.cos(self.theta)) / self.r


        self.f = 1 - self.r / mass.r_s
        self.dt = np.sqrt((self.dr*self.dr) / (self.f*self.f) + (self.r*self.r * self.dtheta*self.dhtheta) / self.f)
        self.E = self.f * self.dt       #FIXED