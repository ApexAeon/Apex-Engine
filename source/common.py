import pygame, sys, json, resources
from pygame.locals import *
from objects import spawn

gamestate = json.loads(open('../game/metadata/new_game.json').read())

DISPLAYSURF = pygame.display.set_mode((1024, 1024))
pygame.font.init()
FONT = pygame.font.SysFont('Bauhaus 93 Regular', 40)

level = resources.loadLevel(gamestate['level'])
assets = resources.loadAssets()
entities = []
masks = {'level':pygame.mask.from_surface(resources.getLevel('walls',level)),'player':pygame.mask.from_surface(resources.getAsset('player_hitbox',assets))}
options = json.loads(open('../data/options.json').read())
gamestate['level_mode'] = json.loads(open('../game/maps/' + gamestate['level'] + '/data.json').read())['level_mode']

for entity in json.loads(open('../game/maps/' + gamestate['level'] + '/entities.json').read()):
    entities.append(spawn(entity))
