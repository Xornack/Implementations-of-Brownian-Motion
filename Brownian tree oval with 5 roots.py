import pygame, sys, os
from pygame.locals import *  
from random import randint
import Brownian_tree_input2
import math
pygame.init()

window_width = 400
window_height = 300
MAXSPEED = 10
SIZE = 4 #particle size
COLOR = (105,105,105)
TIMETICK = 1
MAXPART = 50
# size to increase roots by (larger than particles)
root_augment_size = 4
# angle in radians to shift roots around ellipse
shift_angle = 0
# width and height of the ellipse
e_width = 70
e_height = 30
# asks for window size as small, medium or large
params = Brownian_tree_input2.input_variables(window_width,
                                              window_height,
                                              e_width,
                                              e_height,
                                              SIZE,
                                              root_augment_size,
                                              shift_angle,
                                              )

window_width = params[0]
window_height = params[1]
e_width = params[2]
e_height = params[3]
SIZE = params[4]
root_augment_size = params[5]
shift_angle = params[6]

# needed for reposition of particles
a = e_width/2
b = e_height/2
# redundant variable: [window_width, window_height]
# but it was already in the code, so I didn't change it
WINDOWSIZE = [window_width, window_height]
# initialize pygame variables, screen
window = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Brownian Tree Ellipse 5 Roots")
screen = pygame.display.get_surface()

#just usefull variables relating to window
center = [int(window_width/2), int(window_height/2)]
tenth = [int(window_width/10), int(window_height/10)]

# distance between foci of the ellipse
"""
c = math.sqrt( (b/2)**2 + (a/2)**2 )
c = round(c)
F1 = [center + c, center]
F2 = [center - c, center]
"""
# Ramanujan approximation of the perimeter of the ellipse
# e_perimeter = math.pi*(3*(a + b) - math.sqrt((3*a + b)*(a + 3*b)))

# divide ellipse into 5 equal parts to later put a root on the ellipse
angle1 = 0 + shift_angle
angle2 = angle1 + (2*math.pi)/5
angle3 = angle2 + (2*math.pi)/5
angle4 = angle3 + (2*math.pi)/5
angle5 = angle4 + (2*math.pi)/5
e_x1 = int(a*math.cos(angle1))
e_y1 = int(b*math.sin(angle1))
e_x2 = int(a*math.cos(angle2))
e_y2 = int(b*math.sin(angle2))
e_x3 = int(a*math.cos(angle3))
e_y3 = int(b*math.sin(angle3))
e_x4 = int(a*math.cos(angle4))
e_y4 = int(b*math.sin(angle4))
e_x5 = int(a*math.cos(angle5))
e_y5 = int(b*math.sin(angle5))

# adds sprite groups, freeParticles and tree
# if they are free Particles they fly around
# if they are tree they stop
freeParticles = pygame.sprite.Group()
tree = pygame.sprite.Group()
 
window = pygame.display.set_mode((WINDOWSIZE[0], WINDOWSIZE[1]))
pygame.display.set_caption("Brownian Tree 5 Roots Around an Ellipse")
screen = pygame.display.get_surface()
  
class Particle(pygame.sprite.Sprite):
    def __init__(self, vector, location, surface):
        pygame.sprite.Sprite.__init__(self)
        self.vector = vector
        self.surface = surface
        self.accelerate(vector)
        self.add(freeParticles)
        self.rect = pygame.Rect(location[0], location[1], SIZE, SIZE)
        self.surface.fill(COLOR, self.rect)
 
    def onEdge(self):
        dx = self.rect.centerx - center[0]
        dy = self.rect.centery - center[1]
        dist = math.hypot(dx, dy)
        # distance of an ellipse from center
        t = math.atan2(dy, dx)
        # added an internal fudge factor that changes with ellipse size
        e_dist = int(math.hypot(b*math.sin(t), a*math.cos(t))) \
                 - (e_width + e_height)/50
                    
        if self.rect.left <= 0:
            self.vector = (abs(self.vector[0]), self.vector[1])
        elif self.rect.top <= 0:
            self.vector = (self.vector[0], abs(self.vector[1]))
        elif self.rect.right >= WINDOWSIZE[0]:
            self.vector = (-abs(self.vector[0]), self.vector[1])
        elif self.rect.bottom >= WINDOWSIZE[1]:
            self.vector = (self.vector[0], -abs(self.vector[1]))
        # bounce off ellipse, SIZE is the 'fudge factor'
        # future, make angle of incidence == angle of reflection
        elif dist < (e_dist + SIZE):
            self.vector = (-self.vector[0],
                           -self.vector[1])
 
    def update(self):
        if freeParticles in self.groups():
            self.surface.fill((0,0,0), self.rect)
            self.remove(freeParticles)
            if pygame.sprite.spritecollideany(self, freeParticles):
                self.accelerate((randint(-MAXSPEED, MAXSPEED), 
                                 randint(-MAXSPEED, MAXSPEED)))
                self.add(freeParticles)
            elif pygame.sprite.spritecollideany(self, tree):
                self.stop()
            else:
                self.add(freeParticles)
 
            self.onEdge()
 
            if (self.vector == (0,0)) and tree not in self.groups():
                self.accelerate((randint(-MAXSPEED, MAXSPEED), 
                                 randint(-MAXSPEED, MAXSPEED)))
            self.rect.move_ip(self.vector[0], self.vector[1])
        self.surface.fill(COLOR, self.rect)
 
    def stop(self):
        self.vector = (0,0)
        self.remove(freeParticles)
        self.add(tree)
 
    def accelerate(self, vector):
        self.vector = vector
 
NEW = USEREVENT + 1
TICK = USEREVENT + 2
 
pygame.time.set_timer(NEW, 50)
pygame.time.set_timer(TICK, TIMETICK)
 
def input(events):
    for event in events:
        if event.type == QUIT:
            pygame.quit(), sys.exit(0)
        elif event.type == NEW and (len(freeParticles) < MAXPART):
            # make the particles appear away from the center
            # give four corners for Particles to appear
            rand = randint(1, 4)
            
            if rand == 1:
                Particle((randint(-MAXSPEED,MAXSPEED),
                          randint(-MAXSPEED,MAXSPEED)),
                         (randint(0, tenth[0]), randint(0, tenth[1])), 
                         screen)
            elif rand == 2:
                Particle((randint(-MAXSPEED,MAXSPEED),
                         randint(-MAXSPEED,MAXSPEED)),
                         (randint(WINDOWSIZE[0] - tenth[0], WINDOWSIZE[0]),
                          randint(WINDOWSIZE[1] - tenth[1], WINDOWSIZE[1])), 
                          screen)
            elif rand == 3:
                Particle((randint(-MAXSPEED,MAXSPEED),
                         randint(-MAXSPEED,MAXSPEED)),
                         (randint(WINDOWSIZE[0] - tenth[0], WINDOWSIZE[0]),
                          randint(0, tenth[1])), 
                          screen)
            elif rand == 4:
                Particle((randint(-MAXSPEED,MAXSPEED),
                         randint(-MAXSPEED,MAXSPEED)),
                         (randint(0, tenth[0]),
                          randint(WINDOWSIZE[1] - tenth[1], WINDOWSIZE[1])), 
                          screen)
                
        elif event.type == TICK:
            freeParticles.update()

        

# place 5 roots around a oval
SIZE = SIZE + root_augment_size

root1 = Particle((0, 0), (center[0] + e_x1, center[1] + e_y1), screen)
root1.stop()
root2 = Particle((0, 0), (center[0] + e_x2, center[1] + e_y2), screen)
root2.stop()
root3 = Particle((0, 0), (center[0] + e_x3, center[1] + e_y3), screen)
root3.stop()
root4 = Particle((0, 0), (center[0] + e_x4, center[1] + e_y4 - SIZE), screen)
root4.stop()
root5 = Particle((0, 0), (center[0] + e_x5, center[1] + e_y5 - SIZE), screen)
root5.stop()

SIZE = SIZE - root_augment_size

while True:
    input(pygame.event.get())

    pygame.draw.ellipse(screen,
                        (112,128,144),
                        [int(center[0] - (e_width/2)),
                         int(center[1] - (e_height/2)),
                         int(e_width),
                         int(e_height)],
                         3
                        )
    pygame.display.flip()
