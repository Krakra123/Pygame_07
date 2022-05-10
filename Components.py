import sys
import math
import pygame

from GameVariable import GameVariable

gameVariable = GameVariable()

class Transform:
    def __init__(self, obj, position, rotation, scale):
        self.object = obj
        self.position = position
        self.rotation = rotation
        self.scale = scale
        
    def update(self):
        self.object.rect.bottomleft = self.position
        self.object.image = pygame.transform.rotate(self.object.image, self.rotation)
        self.object.image = pygame.transform.scale(self.object.image, (self.object.rect.width * self.scale[0], self.object.rect.height * self.scale[1]))

    def set_position(self, val):
        self.position = val

    def set_rotation(self, val):
        self.rotation = val;

    def set_scale(self, val):
        self.scale = val

    def change_position(self, movement):
        self.position = (self.position[0] + movement[0], self.position[1] + movement[1])

    def rotate(self, angle):
        self.rotation = self.rotation + angle
                
    def resize(self, size):
        self.scale = size

class Rigidbody:
    def __init__(self, obj, transform_component):
        self.object = obj
        self.transform = transform_component
        self.velocity = (0, 0)
        self.gravity = gameVariable.GRAVITY

    def update(self):
        self.transform.change_position((self.velocity[0] * (1 / gameVariable.current_fps) * gameVariable.PIXEL_PER_DISTANCE, self.velocity[1] * (1 / gameVariable.current_fps) * gameVariable.PIXEL_PER_DISTANCE))
        self.transform.update()

    def gravity_update(self):
        self.velocity = (self.velocity[0], self.velocity[1] - self.gravity * (1 / gameVariable.current_fps))

    def set_velocity(self, val):
        self.velocity = val