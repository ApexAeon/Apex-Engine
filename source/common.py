import pygame, sys, json, resources
from pygame.locals import *
from objects import spawn
pygame.init()
FONT = pygame.font.SysFont('Bauhaus 93 Regular', 40)
gamestate = json.loads(open('../game/metadata/new_game.json').read())
DISPLAYSURF = pygame.display.set_mode((1152, 648),pygame.FULLSCREEN)
pygame.font.init()
level = resources.loadLevel(gamestate['level'])
assets = resources.loadAssets()
entities = []
info = json.loads(open('../game/metadata/info.json','r').read())
pygame.display.set_caption(info['name'])
pygame.display.set_icon(resources.getAsset('icon', assets))
masks = {'level':pygame.mask.from_surface(resources.getLevel('walls',level)),'player':pygame.mask.from_surface(resources.getAsset('player_hitbox',assets))}
options = json.loads(open('../data/options.json').read())
gamestate['level_mode'] = json.loads(open('../game/maps/' + gamestate['level'] + '/data.json').read())['level_mode']
for entity in json.loads(open('../game/maps/' + gamestate['level'] + '/entities.json').read()):
    entities.append(spawn(entity))
def load():
    print('Loading level: '+gamestate['level'])
    entities = [0]
    level = {0}
    masks = {0}
    level = resources.loadLevel(gamestate['level'])
    masks = {'level':pygame.mask.from_surface(resources.getLevel('walls',level)),'player':pygame.mask.from_surface(resources.getAsset('player_hitbox',assets))}
    gamestate['level_mode'] = json.loads(open('../game/maps/' + gamestate['level'] + '/data.json').read())['level_mode']
    for entity in json.loads(open('../game/maps/' + gamestate['level'] + '/entities.json').read()):
        entities.append(spawn(entity))
