# Constantes para o game.
import os
import pygame

BLACK_PLANE_IMG = os.path.join('images', 'black-jet.webp')
WHITE_PLANE_IMG = os.path.join('images', 'white-jet.webp')

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

ROTATE_AMOUNT = 2.5

FPS = 20
SCREEN_COLOR = (130, 130, 130)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WHITE_CONTROLS = [pygame.K_LEFT, pygame.K_RIGHT]
BLACK_CONTROLS = [pygame.K_a, pygame.K_d]
