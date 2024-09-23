import pygame
from pygame import Vector2
import numpy as np

class Tail:
    def __init__(self,
                 pos : Vector2|tuple = (0, 0),
                 camera : Vector2|tuple = (0, 0),
                 angle : float = 0.0,
                 color : tuple = (255, 255, 255),
                 _iterations : int = 100) -> None:
        self.pos = Vector2(pos)
        self.camera = Vector2(camera)
        self.angle = angle
        self.length = 3
        self.color = color

        self.child = None

        if _iterations > 0:
            self.child = Tail(self.getEndPos(), self.camera, self.angle, self.color, _iterations-1)

    def getEndPos(self,
                  relPos : Vector2|tuple = None) -> Vector2:
        if relPos != None:
            pos = relPos
        else:
            pos = self.pos

        return pos + Vector2(
            np.cos(np.radians(self.angle)) * self.length,
            np.sin(np.radians(self.angle)) * self.length
        )
    
    def draw(self, 
             screen : pygame.display) -> None:
        pygame.draw.line(screen, self.color, self.pos - self.camera, self.getEndPos() - self.camera, 3)

    def update(self, 
               screen : pygame.display,
               camera : Vector2|tuple = (0, 0),
               newPos : Vector2|tuple = (0, 0),
               newAngle : float = 0.0) -> None:
        self.camera = Vector2(camera)
        # self.pos = newPos
        # self.angle = self.angle + (newAngle - self.angle) * .5

        midPoint = self.getEndPos() + (self.pos - self.getEndPos()) * .5
        self.pos = newPos
        self.angle = np.degrees(np.atan2(midPoint.y - self.pos.y, midPoint.x - self.pos.x))

        self.draw(screen)
        if self.child != None:
            self.child.update(screen, camera, self.getEndPos(), self.angle)