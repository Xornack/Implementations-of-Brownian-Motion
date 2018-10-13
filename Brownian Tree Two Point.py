"""Program that makes a brownian tree with two roots. You can vary the distance
between the roots, the window size, and the size of the particles"""

import Brownian_tree_input
import pygame, sys, os
from pygame.locals import *  
from random import randint

# global variables
WINDOWSIZE = 300
MAXSPEED = 10
SIZE = 3
COLOR = (255,255,0)
TIMETICK = 1
MAXPART = 50
# defualt distance between two roots.
default_distance = 50

# calls input textbox as above, a massive variable name!
params = Brownian_tree_input.input_variables(WINDOWSIZE,
                                             SIZE,
                                             default_distance)

WINDOWSIZE = params[0]
SIZE = params[1]
default_distance = params[2]
# pygame initialization lines
pygame.init()
pygame.display.set_caption("Brownian Tree Two Roots")
window = pygame.display.set_mode((WINDOWSIZE, WINDOWSIZE))
screen = pygame.display.get_surface()   

#just usefull variables relating to window
center = WINDOWSIZE/2
tenth = WINDOWSIZE/10

# adds sprite groups, freeParticles and tree
# if they are free Particles they fly around
# if they are tree they stop
freeParticles = pygame.sprite.Group()
tree = pygame.sprite.Group()

# particle class, from which all the particles get characteristics  
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
        if self.rect.left <= 0:
            self.vector = (abs(self.vector[0]), self.vector[1])
        elif self.rect.top <= 0:
            self.vector = (self.vector[0], abs(self.vector[1]))
        elif self.rect.right >= WINDOWSIZE:
            self.vector = (-abs(self.vector[0]), self.vector[1])
        elif self.rect.bottom >= WINDOWSIZE:
            self.vector = (self.vector[0], -abs(self.vector[1]))
 
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
                         (randint(0, tenth), randint(0, tenth)), 
                         screen)
            elif rand == 2:
                Particle((randint(-MAXSPEED,MAXSPEED),
                         randint(-MAXSPEED,MAXSPEED)),
                         (randint(WINDOWSIZE - tenth, WINDOWSIZE),
                          randint(WINDOWSIZE - tenth, WINDOWSIZE)), 
                          screen)
            elif rand == 3:
                Particle((randint(-MAXSPEED,MAXSPEED),
                         randint(-MAXSPEED,MAXSPEED)),
                         (randint(WINDOWSIZE - tenth, WINDOWSIZE),
                          randint(0, tenth)), 
                          screen)
            elif rand == 4:
                Particle((randint(-MAXSPEED,MAXSPEED),
                         randint(-MAXSPEED,MAXSPEED)),
                         (randint(0, tenth),
                          randint(WINDOWSIZE - tenth, WINDOWSIZE)), 
                          screen)
                
        elif event.type == TICK:
            freeParticles.update()

# if the distance will be outside the window, sets it to right at the
# window size
distance_between_roots = default_distance
distance_between_roots = int(distance_between_roots)
if distance_between_roots > WINDOWSIZE:
    distance_between_roots = WINDOWSIZE - SIZE 

# place roots 
root1 = Particle((0,0), (center + distance_between_roots/2, center),
                         screen)
root2 = Particle((0,0), (center - distance_between_roots/2, center),
                         screen)

root1.stop()
root2.stop()

while True:
    input(pygame.event.get())
    pygame.display.flip()
