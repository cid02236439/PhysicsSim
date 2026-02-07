import numpy as np
import matplotlib.pyplot as plt
import pygame
pygame.init()


width, height = 1200, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("gravity simulation")
centre = np.array([width/2, height/2])
G = 6.67430e-11

#-=-=-=-=-=-=-=-=-object class-=-=-=-=-=-=-=-=-=-=-=-=-
class object:

    def centreofmass(self, other):
        total_mass = self.mass + other.mass
        return (self.mass * self.position + other.mass * other.position) / total_mass
     
    scale = 250 / (5 * 1.496e11) # 1 AU = 1.496e11 m, scale to fit in window

    def __init__(self, mass, radius, position = np.array([0, 0]), velocity = np.array([0, 0]), colour = (255, 255, 255)):
        self.mass = mass
        self.radius = radius # radius in meters but will be scaled for visualisation
        self.position = centre + (position * self.scale)
        self.velocity = velocity
        self.colour = colour
        self.acceleration = np.array([0, 0])

    def draw(self, window):
        pygame.draw.circle(window, self.colour, (int(self.position[0]), int(self.position[1])), int(self.radius))

    def gravitational_acceleration(self, other):
        
        r_vector = (other.position - self.position) / self.scale # convert back to meters
        r_magnitude = np.linalg.norm(r_vector)

        if r_magnitude == 0:
            return np.array([0, 0]) # avoid division by zero
        
        force_magnitude = G * self.mass * other.mass / r_magnitude**2
        force_direction = r_vector / r_magnitude

        return force_magnitude * force_direction / self.mass # F = ma => a = F/m
    
    def update_position(self, other, dt = 60*60*24*12):
        self.acceleration = self.gravitational_acceleration(other)
        self.velocity += np.array(self.acceleration * dt, dtype = int)
        self.position += np.array(self.velocity * dt * self.scale, dtype = int) # convert back to pixels
    
#-=-=-=-=-=-=-=-=-main program-=-=-=-=-=-=-=-=-=-=-=-=-

sun = object(1.989e30, 30, np.array([0, 0]))
jupiter = object(1.898e27, 25, np.array([7.785e11, 0]), np.array([0, 13070]))

def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        window.fill((0, 0, 0))
        
        
        sun.update_position(jupiter)
        jupiter.update_position(sun)

        jupiter.draw(window)
        sun.draw(window)

        plt.plot(jupiter.position[0], jupiter.position[1], 'o', color = 'blue')
        plt.plot(sun.position[0], sun.position[1], 'o', color = 'yellow')
        

        pygame.display.flip()

    pygame.quit()

main()
#-=-=-=-=-=-=-printing parameters-=-=-=-=-=-=-=-=-=-=-=-=-
    
print("Earth's gravitational acceleration towards Sun:", jupiter.gravitational_acceleration(sun))
print("Sun's gravitational acceleration towards Earth:", sun.gravitational_acceleration(jupiter))
print('COM', jupiter.centreofmass(sun))
print('COM', sun.centreofmass(jupiter))
plt.show()