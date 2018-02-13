import pygame, sys
from pygame.locals import *
from common import DISPLAYSURF
from common import FONT
import json
import time
import math

def loadAsset(filename): # Attempts to load a single image, if an error occurs, it loads the error texture instead.
    try:
        return pygame.image.load(filename)
    except:
        return pygame.Surface((25, 25))

cursor_position = (0, 0)

def begin():
    while True:
        for event in pygame.event.get():
            if event.type is QUIT:
               pygame.quit()
               sys.exit()
            if event.type is KEYDOWN:
                if event.key is K_ESCAPE:
                    return 0
                if event.key is pygame.key.name(event.key) is options['keybinds']['action_north']:
                if event.key is pygame.key.name(event.key) is options['keybinds']['action_east']:
                if event.key is pygame.key.name(event.key) is options['keybinds']['action_south']:
                if event.key is pygame.key.name(event.key) is options['keybinds']['action_west']:
