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

#-=-=-=-=-=-=-=-=-general functions-=-=-=-=-=-=-=-=-=-=-=-=-

def centreofmass(list): # DO I EVEN NEED THIS?
    total_mass = sum(obj.mass for obj in list)
    if total_mass == 0:
        return np.array([0, 0]) # avoid division by zero
    return sum(obj.mass * obj.position for obj in list) / total_mass

#-=-=-=-=-=-=-=-=-object class-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class object:
     
    scale = 250 / (1 * 1.496e11) # 1 AU = 1.496e11 m, scale to fit in window

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
    
    def update_position(self, others, dt = 60*60*24):
        self.acceleration = self.gravitational_acceleration(others)
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

    def draw(self, window):
        position = (int(self.position[0] * self.scale + centre[0]), int((self.position[1]) * self.scale + centre[1]))
        pygame.draw.circle(window, self.colour, position, int(self.radius))

    def bending(self):
        
        pass

# def draw_grid(surface, color, width, height, cell_size):
#     for x in range(0, width, cell_size):
#         pygame.draw.line(surface, color, (x, 0), (x, height))
#     for y in range(0, height, cell_size):
#         pygame.draw.line(surface, color, (0, y), (width, y))

class space_time:
    def __init__(self, unit_size):
        self.points = []
        self.unit_size = unit_size

    def draw(self, window, colour, width, height):
        points = []
        for x in range(0, width, self.unit_size):
            for y in range(0, height, self.unit_size):
                points.append((x, y))
        for point in points:
            pygame.draw.circle(window, colour, point, 1)
            #pygame.draw.line(window, colour, point)

class photon:

    scale = 250 / (1 * 1.496e11) # 1 AU = 1.496e11 m, scale to fit in window

    def __init__(self, position = np.array([-2e11,-2e11], dtype = float), direction = np.array([1,1], dtype = float)):
        self.position = np.array(position, dtype= float)
        self.direction = np.array(direction, dtype = float)

        norm = np.linalg.norm(self.direction)
        self.velocity = 50000 * np.array(self.direction/norm)
    
    def draw(self, window, dt = 60*60*24):
        self.position += self.velocity * dt
        position = (int(self.position[0] * self.scale + centre[0]), int((self.position[1]) * self.scale + centre[1]))
        pygame.draw.circle(window, (255,0,0), position, 5)

    
#-=-=-=-=-=-=-=-=-main program-=-=-=-=-=-=-=-=-=-=-=-=

spacetime = space_time(20)

sun = object(1.989e30, 0, np.array([0, 0]))
mercury = object(3.285e23, 5, np.array([5.79e10, 0]), np.array([0, 47870]))
venus = object(4.867e24, 8, np.array([1.082e11, 0]), np.array([0, 35020]))
earth = object(5.972e24, 10, np.array([1.496e11, 0]), np.array([0, 29780]))
mars = object(6.39e23, 7, np.array([2.279e11, 0]), np.array([0, 24070]))
jupiter = object(1.898e27, 20, np.array([7.785e11, 0]), np.array([0, 13070]))
saturn = object(5.683e26, 18, np.array([1.433e12, 0]), np.array([0, 9600]))
uranus = object(8.681e25, 15, np.array([2.877e12, 0]), np.array([0, 6800]))
neptune = object(1.024e26, 15, np.array([4.503e12, 0]), np.array([0, 5400]))


sun1 = object(1.989e30, 30, [0, -1e12], [10000,0])
sun2 = object(1.989e30, 30, [0, 1e12], [-10000,0])
sun3 = object(1.989e30, 30, [-1e12 , 0], [0, -10000])
sun4 = object(1.989e30, 30, [1e12 , 0], [0, 10000])

photon1 = photon()

#objects = [sun1, sun2, sun3, sun4]
objects = [sun, mercury, venus, earth, mars]


def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        window.fill((0, 0, 0))

        #draw_grid(window, (80, 80, 80), width, height, 20)
        spacetime.draw(window, (80, 80, 80), width, height)
        photon1.draw(window)
        plt.plot(photon1.position[0], photon1.position[1], '.', color = 'r')
        centre_of_mass = centreofmass(objects) * (250 / (5 * 1.496e11)) + centre
        
        for object in objects:
            object.update_position(objects)
            object.draw(window)
            plt.plot(object.position[0], object.position[1], '.', color = 'b')
        
        pygame.draw.circle(window,(255, 255, 255), centre_of_mass ,  5,1)

        pygame.display.flip()

    pygame.quit()

main()
#-=-=-=-=-=-=-printing parameters-=-=-=-=-=-=-=-=-=-=-=-=-=-


plt.axis('equal')
plt.show()