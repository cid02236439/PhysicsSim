import numpy as np
import matplotlib.pyplot as plt
import pygame
pygame.init()


width, height = 1200, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("gravity simulation")
centre = np.array([width/2, height/2])

G = 6.67430e-11

def centreofmass(list):
    total_mass = sum(obj.mass for obj in list)
    if total_mass == 0:
        return np.array([0, 0]) # avoid division by zero
    return sum(obj.mass * obj.position for obj in list) / total_mass

#-=-=-=-=-=-=-=-=-object class-=-=-=-=-=-=-=-=-=-=-=-=-
class object:
     
    scale = 250 / (5 * 1.496e11) # 1 AU = 1.496e11 m, scale to fit in window

    def __init__(self, mass, radius, position = np.array([0, 0], dtype = float), velocity = np.array([0, 0], dtype = float), colour = (255, 255, 255)):
        self.mass = mass
        self.radius = radius # radius in meters but will be scaled for visualisation
        self.position = np.array(position, dtype = float)
        self.velocity = np.array(velocity, dtype = float)
        self.colour = colour
        self.acceleration = np.array([0, 0], dtype = float)

    def draw(self, window):
        position = (int(self.position[0] * self.scale + centre[0]), int((self.position[1]) * self.scale + centre[1]))
        pygame.draw.circle(window, self.colour, position, int(self.radius))

    def gravitational_acceleration(self, other):
        r_vector = (other.position - self.position)
        r_magnitude = np.linalg.norm(r_vector)

        if r_magnitude == 0:
            return np.array([0, 0]) # avoid division by zero
        
        force_magnitude = G * self.mass * other.mass / r_magnitude**2
        force_direction = r_vector / r_magnitude

        return force_magnitude * force_direction / self.mass # F = ma => a = F/m
    
    def update_position(self, other, dt = 60*60*24*12):
        self.acceleration = self.gravitational_acceleration(other)
        self.velocity += np.array(self.acceleration * dt, dtype = float)
        self.position += np.array(self.velocity * dt, dtype = float)
    
    
#-=-=-=-=-=-=-=-=-main program-=-=-=-=-=-=-=-=-=-=-=-=

sun = object(1.989e30, 30, np.array([0, 0]))
jupiter = object(1.898e27, 20, np.array([7.785e11, 0]), np.array([0, 13070]))
earth = object(5.972e24, 10, np.array([1.496e11, 0]), np.array([0, 29780]))
centre_of_mass = centreofmass([sun, jupiter, earth])

def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        window.fill((0, 0, 0))
        
        
        sun.update_position(jupiter)
        jupiter.update_position(sun)
        earth.update_position(sun)
        
        
        jupiter.draw(window)
        sun.draw(window)
        earth.draw(window)
        
        plt.plot(jupiter.position[0], jupiter.position[1], 'o', color = 'blue')
        plt.plot(sun.position[0], sun.position[1], 'o', color = 'yellow')
        plt.plot(earth.position[0], earth.position[1], 'o', color = 'green')
        

        pygame.display.flip()

    pygame.quit()

main()
#-=-=-=-=-=-=-printing parameters-=-=-=-=-=-=-=-=-=-=-=-=-=-
    
print("jupiter's's gravitational acceleration towards Sun:", jupiter.gravitational_acceleration(sun))
#print("Sun's gravitational acceleration towards Jupiter:", sun.gravitational_acceleration(jupiter))
print('earth\'s gravitational acceleration towards Sun:', earth.gravitational_acceleration(sun))

print('centre of mass of the system:', centre_of_mass)
plt.show()