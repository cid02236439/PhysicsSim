import numpy as np
import matplotlib.pyplot as plt
import pygame
pygame.init()

width, height = 1200, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("light simulation")

centre = np.array([width/2, height/2])
G = 6.67430e-11
scale = 250 / (1 * 1.496e11) # 1 AU = 1.496e11 m, scale to fit in window

class object:
    def __init__(self, mass, radius, position = np.array([0, 0], dtype = float), velocity = np.array([0, 0], dtype = float), colour = (255, 255, 255)):
        self.mass = mass
        self.radius = radius # radius in meters but will be scaled for visualisation
        self.position = np.array(position, dtype = float)
        self.velocity = np.array(velocity, dtype = float)
        self.colour = colour
        self.acceleration = np.array([0, 0], dtype = float)
    
    def display(self, window):
        position = (int(self.position[0] * scale + centre[0]), int((self.position[1]) * scale + centre[1]))
        pygame.draw.circle(window, self.colour, position, int(self.radius))