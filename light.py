import numpy as np
import matplotlib.pyplot as plt
import pygame
import random

pygame.init()

width, height = 1400, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("ray trace")
centre = np.array([width / 2, height / 2], dtype=float)
font = pygame.font.SysFont(None, 30)
dt = 3e-8

c = 299792458
# 400 to 790 e12 Hz
red = 400e12
green = 595e12
blue = 790e12

frequency_range = [400e12, 596e12, 700e12]
colour_range = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]


class light:
    def __init__(self, window, position, direction, frequency=400e12):
        self.frequency = frequency
        self.direction = np.array(direction, dtype=float)
        self.position = np.array(position, dtype=float)
        self.window = window
        self.wavelength = c / self.frequency
        self.colour = [
            np.interp(self.frequency, frequency_range, colour_range[0]),
            np.interp(self.frequency, frequency_range, colour_range[1]),
            np.interp(self.frequency, frequency_range, colour_range[2]),
        ]
        norm = np.linalg.norm(self.direction)
        self.velocity = c * np.array(self.direction / norm)
        self.out_of_bounds = False

        self.trail = []
        self.max_trail_length = 20

    def move(self):
        self.position += self.velocity * dt

    def draw(self):
        self.move()
        self.trail.append(self.position.copy())  # store tail
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

        for i in range(len(self.trail) - 1):  # tail fading algorithm
            fade = i / len(self.trail)
            colour = (int(255 * fade), 0, 0)
            pos1 = (
                int(self.trail[i][0]),
                int(self.trail[i][1]),
            )
            pos2 = (
                int(self.trail[i + 1][0]),
                int(self.trail[i + 1][1]),
            )
            pygame.draw.line(self.window, self.colour, pos1, pos2, 2)


class atom:
    def __init__(self, window, position = [300,300], radius = 5):
        self.window = window
        self.position = np.array(position, dtype=float)
        self.radius = radius
        self.size = np.pi * self.radius * self.radius

    def draw(self):
        pygame.draw.circle(self.window, (255, 255, 255), self.position, self.radius, 2)


a = light(window, (300, 500), (1, 0))
b = atom(window, (500, 500), 5)

def make_lattice(x_num = 10, y_num = 10, xstart = 0.5, ystart = 0.5, randomise = 1):
    atoms = []
    if not randomise:
        positionx = np.linspace(xstart * width, width, x_num)
        positiony = np.linspace(ystart*height, height, y_num)
        for x in positionx:
            for y in positiony:
                atoms.append(atom(window, position = (x,y)))
    else:
        for _ in range(x_num * y_num):
            positionx = random.randint(int(xstart * width), width)
            positiony = random.randint(int(ystart * height), height)
            atoms.append(atom(window, position = (positionx, positiony)))
    return atoms

lattice = make_lattice()

def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        window.fill((0, 0, 0))

        for atom in lattice:
            atom.draw()
        a.draw()
        b.draw()

        pygame.display.flip()
    pygame.quit()


main()
