import numpy as np
import matplotlib.pyplot as plt
import pygame
pygame.init()

#=-=-=-=-=-=-=-=-=-=window setup-=-=-=-=-=-=-=-=-=-=-=-=-

width, height = 1200, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("gravity simulation")
centre = np.array([width/2, height/2])

G = 6.67430e-11
c = 299792458

class object:
    def __init__(self, mass, radius):
        self.mass = mass
        self.radius = radius
        self.r_s = 2 * G * self.mass / (c*c)

    def display(self, window):
        pygame.draw.circle(window, (0,0,0), centre, self.radius)
blackhole = object(1e35, 30)


def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        

        window.fill((255,255,255))
        blackhole.display(window)


        pygame.display.flip()
    pygame.quit()

main()
