import pygame
from pygame import Vector2
import globals as gb

class Object:
    def __init__(self,
                 pos : Vector2|tuple = (0, 0),
                 camera : Vector2|tuple = (0, 0),
                 color : tuple = (255, 255, 255),
                 screenWrapping : bool = False):
        self.pos = Vector2(pos)
        self.camera = Vector2(camera)
        self.color = color
        self.screenWrapping = screenWrapping

    def screenWrappedPos(self,
                         pos : Vector2|tuple) -> Vector2:
        return Vector2(pos.x % gb.SX, pos.y % gb.SY)

    def draw(self,
             screen : pygame.display):
        pos = self.pos - self.camera
        if self.screenWrapping:
            pos = self.screenWrappedPos(pos)
        pygame.draw.circle(screen, self.color, pos, 10)

    def update(self,
               screen : pygame.display,
               camera : Vector2|tuple = (0, 0)):
        self.camera = Vector2(camera)
        self.draw(screen)