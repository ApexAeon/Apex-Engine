import pygame, sys, json, resources
from pygame.locals import *
from objects import spawn
pygame.init()
FONT = pygame.font.SysFont('Bauhaus 93 Regular', 30)
gamestate = resources.loadData('new_game')
options = resources.loadData('options')
DISPLAYSURF = pygame.Surface((gamestate['game_width'],gamestate['game_height']))
REALSURF = pygame.display.set_mode((options['screen_width'], options['screen_height'])) # ,pygame.FULLSCREEN 
pygame.font.init()
level = resources.loadLevel(gamestate['level'])
assets = resources.loadAssets()
entities = []
info = json.loads(open('../game/metadata/info.json','r').read())
pygame.display.set_caption(info['name'])
pygame.display.set_icon(resources.getAsset('icon', assets))
masks = {'level':pygame.mask.from_surface(resources.getLevel('walls',level)),'player':pygame.mask.from_surface(resources.getAsset('player_hitbox',assets))}
gamestate['level_mode'] = json.loads(open('../game/maps/' + gamestate['level'] + '/data.json').read())['level_mode']
for entity in json.loads(open('../game/maps/' + gamestate['level'] + '/entities.json').read()):
    entities.append(spawn(entity))
def load():
    global assets
    global level
    global entities
    global gamestate
    global masks
    print('Loading level: '+gamestate['level'])
    entities.clear()
    level.clear()
    masks.clear()
    level.update( resources.loadLevel(gamestate['level']) )
    masks.update( {'level':pygame.mask.from_surface(resources.getLevel('walls',level)),'player':pygame.mask.from_surface(resources.getAsset('player_hitbox',assets))} )
    gamestate['level_mode'] = json.loads(open('../game/maps/' + gamestate['level'] + '/data.json').read())['level_mode']
    for entity in json.loads(open('../game/maps/' + gamestate['level'] + '/entities.json').read()):
        entities.append(spawn(entity))
def scale():
    REALSURF.blit(pygame.transform.scale(DISPLAYSURF, (screenWidth, screenHeight)), (0,0))
    

