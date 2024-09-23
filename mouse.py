import pygame
from pygame import Vector2
import numpy as np
from tail import Tail

class Mouse:
    def __init__(self, 
                 pos : Vector2|tuple = (0, 0),
                 camera : Vector2|tuple = (0, 0)) -> None:
        self.pos = Vector2(pos)
        self.camera = Vector2(camera)
        self.velo = 0.0
        self.maxVelo = 10.0
        self.angleVelo = 0.0
        self.maxAngleVelo = 10.0
        self.color = (100, 0, 255)
        self.size = 15
        self.angle = -90.0
        self.acceleration = .25
        self.angleAcceleration = .5
        self.drag = self.acceleration/10
        self.angleDrag = self.angleAcceleration/2

        self.tail : Tail = Tail(
            (np.cos(np.radians(self.angle + 180)) * self.size,
             np.sin(np.radians(self.angle + 180)) * self.size),
             camera,
             self.angle,
             self.color
        )

    def move(self, keys : list) -> None:
        #input
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velo += self.acceleration
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velo -= self.acceleration
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.angleVelo -= self.angleAcceleration
        if keys[pygame.K_s] or keys[pygame.K_RIGHT]:
            self.angleVelo += self.angleAcceleration

        #limit velos to their max
        if abs(self.velo) > self.maxVelo:
            self.velo = self.maxVelo * (self.velo/abs(self.velo))
        if abs(self.angleVelo) > self.maxAngleVelo:
            self.angleVelo = self.maxAngleVelo * (self.angleVelo/abs(self.angleVelo))

        #drag
        if self.velo != 0:
            self.velo += self.drag * (-1 * (self.velo/abs(self.velo)) )
            if abs(self.velo) < self.drag:
                self.velo = 0

        if self.angleVelo != 0:
            self.angleVelo += self.angleDrag * (-1 * (self.angleVelo/abs(self.angleVelo)))
            if abs(self.angleVelo) < self.angleDrag:
                self.angleVelo = 0

        #update angle based on angleVelo
        self.angle = self.angle + self.angleVelo

        #update position based on velo
        self.pos += Vector2(self.velo * np.cos(np.radians(self.angle)),
                            self.velo * np.sin(np.radians(self.angle)))
        
    def draw(self,
             screen : pygame.display) -> None:
        pygame.draw.circle(screen, self.color, self.pos - self.camera, self.size)
        pygame.draw.polygon(screen, self.color, (
            self.pos - self.camera + Vector2((self.size * 3) * np.cos(np.radians(self.angle)), (self.size * 3) * np.sin(np.radians(self.angle))),
            self.pos - self.camera + Vector2(self.size * np.cos(np.radians(self.angle + 90)), self.size * np.sin(np.radians(self.angle + 90))),
            self.pos - self.camera + Vector2(self.size * np.cos(np.radians(self.angle - 90)), self.size * np.sin(np.radians(self.angle - 90)))
        ))

    def update(self,
               screen : pygame.display,
               camera : Vector2|tuple = (0, 0),
               keys : list = None) -> None:
        if keys == None:
            raise SyntaxError("You need to import pygame.keys.get_pressed()")

        self.camera = camera

        self.move(keys)

        self.tail.update(screen,
                         self.camera,
                         self.pos + (np.cos(np.radians(self.angle + 180)) * self.size,
                          np.sin(np.radians(self.angle + 180)) * self.size),
                          self.angle + 180)

        self.draw(screen)