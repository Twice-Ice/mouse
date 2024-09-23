import pygame
from pygame import Vector2
import globals as gb
import random
import math
import numpy as np

screen = pygame.display.set_mode((gb.SX, gb.SY), pygame.NOFRAME)

doExit = False
clock = pygame.time.Clock()

camera = Vector2(0, 0)

def getP2():
    return Vector2((random.randint(0, gb.SX), random.randint(0, gb.SY)))

p1 = Vector2((gb.SX//2, gb.SY//2))
p2 = getP2()
length = 40

while not doExit:
    delta = clock.tick(gb.FPS)/1000
    screen.fill(gb.BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            doExit = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        p2 = getP2()
    elif keys[pygame.K_t]:
        p2 = Vector2((gb.SX//2, gb.SY//2)) + Vector2(100, 0)

    pygame.draw.circle(screen, (255, 0, 0), p1, 3)
    pygame.draw.circle(screen, (0, 255, 0), p2, 3)
    pygame.draw.line(screen, (50, 50, 50), p1, p2)

    angle = np.degrees(np.atan2(p2.y - p1.y, p2.x - p1.x))

    print(angle)

    p2Short =  p1 + Vector2(
        length * np.cos(np.radians(angle)),
        length * np.sin(np.radians(angle))
    )

    pygame.draw.line(screen, (0, 0, 255), p1, p2Short)


    """
    Soh Cah Toa

    Tan(opposite/ajacent)
    
    """

    pygame.display.flip()
pygame.quit()