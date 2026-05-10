"""
#5
GR USED IN THE FORM OF GEODESIC EQUATIONS FOR SHWARZSCHILD METRIC TO GET THE "ACCELERATION" TERMS AND UPDATE THE "VELOCITY" TERMS
Note that this sim uses time instead of the affine parameter when displaying the next step
next steps:
    validating existing data
    investigations
"""

import numpy as np
import matplotlib.pyplot as plt
import pygame
import random

pygame.init()

width, height = 1200, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("gravity simulation")
centre = np.array([width / 2, height / 2], dtype=float)
font = pygame.font.SysFont(None, 45)

scale = 500 / (0.01 * 1.496e11)  # 1 AU = 1.496e11 m, scale to fit in window
G = 6.67430e-11
c = 299792458
dt = 100 * 60 * 60 * 24

left = (0 - centre[0]) / scale
right = (width - centre[0] + 100) / scale
top = (0 - centre[1] - 100) / scale
bottom = (height - centre[1] + 100) / scale


class object:
    def __init__(self, window, mass):
        self.window = window
        self.mass = mass
        self.r_s = 2 * G * self.mass / (c * c)
        self.dlambda = 0.05 * self.r_s / c

    def display(self):
        pygame.draw.circle(self.window, (255, 255, 255), centre, self.r_s * scale)
        pygame.draw.circle(
            self.window, (100, 100, 100), centre, self.r_s * scale * 1.5, 1
        )


blackhole = object(window, 1e35)


class photon:
    def __init__(
        self,
        window,
        mass,
        position=np.array([-2e9, 0], dtype=float),
        direction=np.array([1, 0], dtype=float),
    ):
        self.window = window
        self.mass = mass
        self.position = np.array(position, dtype=float)
        self.direction = np.array(direction, dtype=float)
        norm = np.linalg.norm(self.direction)
        self.velocity = c * np.array(self.direction / norm)
        self.out_of_bounds = False

        self.trail = []
        self.max_trail_length = 100

        self.r = np.sqrt(
            self.position[0] * self.position[0] + self.position[1] * self.position[1]
        )
        self.theta = np.arctan2(self.position[1], self.position[0])
        self.dr = self.velocity[0] * np.cos(self.theta) + self.velocity[1] * np.sin(
            self.theta
        )
        self.dtheta = (
            -self.velocity[0] * np.sin(self.theta)
            + self.velocity[1] * np.cos(self.theta)
        ) / self.r

        f = 1 - mass.r_s / self.r
        self.dt = np.sqrt(
            (self.dr * self.dr) / (f * f)
            + (self.r * self.r * self.dtheta * self.dtheta) / f
        )
        self.E = f * self.dt  # FIXED E value

    def check_boundary(self):
        d2 = self.position[0] * self.position[0] + self.position[1] * self.position[1]
        r_s = self.mass.r_s * self.mass.r_s * 1.1
        if d2 < r_s:
            self.out_of_bounds = True
            return
        if (
            self.position[0] > right
            or self.position[0] < left
            or self.position[1] < top
            or self.position[1] > bottom
        ):
            self.out_of_bounds = True

    def bend(self):
        r = self.r
        r_s = self.mass.r_s

        f = 1 - r_s / r
        self.dt = self.E / f
        dlambda = self.mass.dlambda
        #dlambda = dt / self.dt

        d2theta = -2 * self.dr * self.dtheta / r
        d2r = (
            -r_s * f * self.dt * self.dt / (2 * r * r)
            + r_s * self.dr * self.dr / (2 * r * r * f)
            + (r - r_s) * self.dtheta * self.dtheta
        )

        self.dtheta += d2theta * dlambda
        self.dr += d2r * dlambda
        self.r += self.dr * dlambda
        self.theta += self.dtheta * dlambda

        self.position[0] = self.r * np.cos(self.theta)
        self.position[1] = self.r * np.sin(self.theta)

    def display(self):
        self.check_boundary()
        if self.out_of_bounds:
            return
        self.bend()

        self.trail.append(self.position.copy())  # store tail
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

        for i in range(len(self.trail) - 1):  # tail fading algorithm
            fade = i / len(self.trail)
            colour = (int(255 * fade), 0, 0)
            pos1 = (
                int(self.trail[i][0] * scale + centre[0]),
                int(self.trail[i][1] * scale + centre[1]),
            )
            pos2 = (
                int(self.trail[i + 1][0] * scale + centre[0]),
                int(self.trail[i + 1][1] * scale + centre[1]),
            )
            pygame.draw.line(self.window, colour, pos1, pos2, 1)

        # position = (
        #     int(self.position[0] * scale + centre[0]),
        #     int((self.position[1]) * scale + centre[1]),
        # )
        # #pygame.draw.circle(self.window, (255, 0, 0), position, 2)


def make_photons(number=10, xstart = 0, ystart = 0, ysize=1, randomise=True):
    photons = []
    if not randomise:
        positions = np.linspace( (-ystart*height/2) - height * ysize / 2, (-ystart*height/2) + height * ysize / 2, number)
        for i in range(number):
            photons.append(
                photon(
                    window,
                    blackhole,
                    position=np.array([left + xstart * width / scale, positions[i] / scale], dtype=float),
                )
            )
    else:
        for i in range(number):
            positionx = random.randrange(int(-width / 2), int(width / 2)) / scale
            positiony = random.randrange(int(-height / 2), int(height / 2)) / scale
            direction = (random.uniform(-1, 1), random.uniform(-1, 1))
            photons.append(
                photon(
                    window,
                    blackhole,
                    position=(positionx, positiony),
                    direction=direction,
                )
            )
    return photons


def main():
    
    num_photons = 100
    xstart = 0
    ystart = 0.33
    ysize = 0.005
    randomise = 0
    params = num_photons, xstart, ystart, ysize, randomise

    i = 0
    photons = make_photons(*params)
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        window.fill((0, 0, 0))

        blackhole.display()
        text = font.render(str(len(photons)), True, (255, 255, 255))

        # if len(photons) < num_photons/2:
        #     photons.extend(make_photons(num_photons - len(photons), size, randomise))

        if i == 90:
            photons.extend(make_photons(*params))
            i = 0

        window.blit(text, (10, 10))
        photons = [photon for photon in photons if not photon.out_of_bounds]
        for photon in photons:
            photon.display()
        i += 1
        pygame.display.flip()
    pygame.quit()


main()
