import pygame, sys, json
from pygame.locals import *
animations = {
    "spell":0,
    "walk":8,
    "thrust":4,
    "slash":12,
    "hurt":20,
    "shoot":16
    }
directions = {
    "north":0,
    "west":1,
    "south":2,
    "east":3
    }
animation_lengths = {
    "spell":7,
    "walk":9,
    "thrust":8,
    "slash":6,
    "hurt":6,
    "shoot":13
}
def loadAssets(): # Attempts to load all assets listed in assets.json into the assets dictionary. Replaced missing textures with error texture.
    asset_list = json.loads(open('../game/metadata/asset_list.json').read())
    assets = {}
    for pair in asset_list:
        try:
            assets[pair] = pygame.image.load(asset_list[pair])
        except:
            assets[pair] = pygame.Surface((25, 25))
    return assets
def getAsset(name, assets): # Get an already loaded asset, if asset not found, replace with error texture.
    if name in assets:
        return assets[name]
    else:
        return pygame.Surface((25, 25))
def getMask(name, masks):
    if name in masks:
        return masks[name]
    else:
        return pygame.mask.from_surface(pygame.Surface((25, 25)))
def loadAsset(filename): # Attempts to load a single image, if an error occurs, it loads the error texture instead.
    try:
        return pygame.image.load(filename)
    except:
        return pygame.Surface((25, 25))
def getLevel(name, level):
    if name in level:
        return level[name]
    else:
        return pygame.Surface((25, 25))
def loadLevel(level_name):
    return {'visual':loadAsset('../game/maps/' + level_name + '/visual.png'),'walls':loadAsset('../game/maps/' + level_name + '/walls.png'),'fg':loadAsset('../game/maps/' + level_name + '/fg.png')}
def getAnimation(animation, direction, state, sheet, size=(64, 64)):
    row = animations[animation] + directions[direction]
    column = state
    sprite = pygame.Surface(size, SRCALPHA)
    sprite.fill((255,255,255,0))
    sprite.blit(sheet , ( -(column*size[0]) , -(row*size[1]) ) )
    return sprite
