import pygame
from pygame import Vector2
import globals as gb
from mouse import Mouse
from objects import Object
import random
import numpy as np

screen = pygame.display.set_mode((gb.SX, gb.SY), pygame.NOFRAME)

doExit = False
clock = pygame.time.Clock()

camera : Vector2 = None
player : Mouse = None
objectList : list[Object] = None

def startGame():
    global camera, player, objectList
    camera = Vector2(0, 0)

    player = Mouse(pos=(gb.SX//2, gb.SY//2))

    objectList = [Object((random.randint(0, gb.SX), random.randint(0, gb.SY)), camera, (155, 155, 155), True) for _ in range(15)]

def cameraLogic():
    global camera, player
    angleFactor = player.angleVelo/player.maxAngleVelo
    if angleFactor != 0:
        angleFactor = ((1 * (angleFactor/abs(angleFactor))) - angleFactor)
    else:
        angleFactor = 1
    angleFactor = abs(angleFactor)
    normalizedVelo = player.velo/player.maxVelo
    distanceMult = 350
    
    minAngleFactor = .75

    alteredAngleFactor = angleFactor if angleFactor <= minAngleFactor else minAngleFactor
    alteredAngleFactor *= 1/minAngleFactor

    print(angleFactor, alteredAngleFactor)

    cameraDistance = -normalizedVelo * distanceMult * alteredAngleFactor

    vec2Velo = Vector2(
        np.cos(np.radians(player.angle)) * cameraDistance,
        np.sin(np.radians(player.angle)) * cameraDistance
    )
    camera = player.pos - vec2Velo - Vector2(gb.SX//2, gb.SY//2)

startGame()
while not doExit:
    delta = clock.tick(gb.FPS)/1000
    screen.fill(gb.BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            doExit = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        startGame()

    for object in objectList:
        object.update(screen, camera)

    player.update(screen, camera, keys)

    cameraLogic()

    pygame.display.flip()
pygame.quit()