import pygame, sys
from pygame.locals import *
from common import DISPLAYSURF
from common import FONT
import json
import time
import math
import pygame.mixer

gamestate = json.loads(open('../game/metadata/new_game.json').read())
assets = {}
entities = []
reslist = []
masks = {}
level = {}
assetlist = {}
data = {} 
options = json.loads(open('../data/options.json').read())

def trigger(name):
    for entity in entities:
        if entity['name'] == name:
            entity.trigger()
    
def loadAssets(): # Attempts to load all assets listed in assets.json into the assets dictionary. Replaced missing textures with error texture.
    assetlist = json.loads(open('../game/metadata/asset_list.json').read())
    for pair in assetlist:
        try:
            assets[pair] = pygame.image.load(assetlist[pair])
        except:
            assets[pair] = pygame.Surface((25, 25))

def getAsset(name): # Get an already loaded asset, if asset not found, replace with error texture.
    if name in assets:
        return assets[name]
    else:
        return pygame.Surface((25, 25))

def getMask(name):
    if name in masks:
        print('Done!')
        return masks[name]
    else:
        print('Failed!')
        return pygame.mask.from_surface(pygame.Surface((25, 25)))
    
def loadAsset(filename): # Attempts to load a single image, if an error occurs, it loads the error texture instead.
    try:
        return pygame.image.load(filename)
    except:
        return pygame.Surface((25, 25))
def getLevel(name):
    if name in level:
        return level[name]
    else:
        return pygame.Surface((25, 25))   
def getGamestate(): # Will be used for saving gamestate.
    return gamestate
def setGamestate(gamestatein): # Will be used for loading gamestate.
    gamestate = gamestatein
def calcX(x, y, z): # Convert isometrric X values into actual screen coordinates.
    if gamestate['level_mode'] == 'isometric':
        return ((x * 2 - z * 2) + 0.25 * (x-z)) * 4
    else:
        return x * 4
def calcY(x, y, z): # Convert isometrric Y values into actual screen coordinates.
    if gamestate['level_mode'] == 'isometric':
        return ((x + z - y) + 0.25 * (x+z)) * 4
    else:
        return (z - y) * 4
def loadLevel():
    level['visual'] = loadAsset('../game/maps/' + gamestate['lvl'] + '/visual.png')
    level['walls'] = loadAsset('../game/maps/' + gamestate['lvl'] + '/walls.png')
    entity_counter = 0
    for entity in json.loads(open('../game/maps/' + gamestate['lvl'] + '/entities.json').read()):
        entities[entity_counter] = objects.spawn(entity)
        entity_counter += 1
    data = json.loads(open('../game/maps/' + gamestate['lvl'] + '/data.json').read())
    masks['level'] = pygame.mask.from_surface(getLevel('walls'))
    masks['player'] = pygame.mask.from_surface(getAsset('player_hitbox'))
    gamestate['level_mode'] = data['level_mode']
def start():

    # Main Game Loop

    while True:
        timeStart = time.process_time() # Maintain constant framerate.
        DISPLAYSURF.blit(getLevel('visual'), (0,0))
        DISPLAYSURF.blit(getAsset('chardisplay'),(math.floor(calcX(gamestate['x'], gamestate['y'], gamestate['z'])),math.floor(calcY(gamestate['x'], gamestate['y'], gamestate['z']))))
        DISPLAYSURF.blit(getLevel('walls'), (0,0))        
        if not gamestate['isMoving']:
            assets['chardisplay'] = getAsset(gamestate['player']['direction']+'_idle')

        # Event Processing

        for event in pygame.event.get():
            if event.type is QUIT:
               pygame.quit()
               sys.exit()
            if event.type is KEYDOWN and event.key is K_ESCAPE:
                return 'PAUSE'

            # Handle inputs.
            
            if event.type is KEYDOWN and pygame.key.name(event.key) is options['keybinds']['action_north']:
                gamestate['action_north'] = True
            if event.type is KEYDOWN and pygame.key.name(event.key) is options['keybinds']['action_west']:
                gamestate['action_west'] = True
            if event.type is KEYDOWN and pygame.key.name(event.key) is options['keybinds']['action_south']:
                gamestate['action_south'] = True
            if event.type is KEYDOWN and pygame.key.name(event.key) is options['keybinds']['action_east']:
                gamestate['action_east'] = True
                
            if event.type is KEYUP and pygame.key.name(event.key) is options['keybinds']['action_north']:
                gamestate['action_north'] = False
            if event.type is KEYUP and pygame.key.name(event.key) is options['keybinds']['action_west']:
                gamestate['action_west'] = False
            if event.type is KEYUP and pygame.key.name(event.key) is options['keybinds']['action_south']:
                gamestate['action_south'] = False
            if event.type is KEYUP and pygame.key.name(event.key) is options['keybinds']['action_east']:
                gamestate['action_east'] = False
                
        # Accelerate and decelerate.
        
        if gamestate['action_north'] and gamestate['player']['velocity']['north'] != gamestate['max_velocity']:
            if gamestate['player']['velocity']['north'] + gamestate['acceleration'] > gamestate['max_velocity']:
                gamestate['player']['velocity']['north'] = gamestate['max_velocity']
            else:
                gamestate['player']['velocity']['north'] += gamestate['acceleration']
        if gamestate['action_south'] and gamestate['player']['velocity']['south'] != gamestate['max_velocity']:
            if gamestate['player']['velocity']['south'] + gamestate['acceleration'] > gamestate['max_velocity']:
                gamestate['player']['velocity']['south'] = gamestate['max_velocity']
            else:
                gamestate['player']['velocity']['south'] += gamestate['acceleration']
        if gamestate['action_west'] and gamestate['player']['velocity']['west'] != gamestate['max_velocity']:
            if gamestate['player']['velocity']['west'] + gamestate['acceleration'] > gamestate['max_velocity']:
                gamestate['player']['velocity']['west'] = gamestate['max_velocity']
            else:
                gamestate['player']['velocity']['west'] += gamestate['acceleration']
        if gamestate['action_east'] and gamestate['player']['velocity']['east'] != gamestate['max_velocity']:
            if gamestate['player']['velocity']['east'] + gamestate['acceleration'] > gamestate['max_velocity']:
                gamestate['player']['velocity']['east'] = gamestate['max_velocity']
            else:
                gamestate['player']['velocity']['east'] += gamestate['acceleration']

        if not gamestate['action_north'] and gamestate['player']['velocity']['north'] > 0:
            if gamestate['player']['velocity']['north'] - gamestate['acceleration'] >= 0:
                gamestate['player']['velocity']['north'] -= gamestate['acceleration']
            else:
                gamestate['player']['velocity']['north'] = 0                
        if not gamestate['action_south'] and gamestate['player']['velocity']['south'] > 0:
            if gamestate['player']['velocity']['south'] - gamestate['acceleration'] >= 0:
                gamestate['player']['velocity']['south'] -= gamestate['acceleration']
            else:
                gamestate['player']['velocity']['south'] = 0                
        if not gamestate['action_west'] and gamestate['player']['velocity']['west'] > 0:
            if gamestate['player']['velocity']['west'] - gamestate['acceleration'] >= 0:
                gamestate['player']['velocity']['west'] -= gamestate['acceleration']
            else:
                gamestate['player']['velocity']['west'] = 0                
        if not gamestate['action_east'] and gamestate['player']['velocity']['east'] > 0:
            if gamestate['player']['velocity']['east'] - gamestate['acceleration'] >= 0:
                gamestate['player']['velocity']['east'] -= gamestate['acceleration']
            else:
                gamestate['player']['velocity']['east'] = 0

        # Collision detection and final motion implementation.

        if gamestate['player']['velocity']['north'] > 0 and masks['level'].overlap_area( masks['player'] , ( math.floor(calcX(gamestate['x'],0,gamestate['z']-gamestate['player']['velocity']['north'])) , math.floor(calcY(gamestate['x'],0,gamestate['z']-gamestate['player']['velocity']['north'])) ) ) == 0:
            gamestate['z'] = gamestate['z'] - gamestate['player']['velocity']['north']
            print('Moving!')
        if gamestate['player']['velocity']['west'] > 0 and       masks['level'].overlap_area( masks['player'] , ( math.floor(calcX(gamestate['x']-gamestate['player']['velocity']['west'],0,gamestate['z'])) , math.floor(calcY(gamestate['x']-gamestate['player']['velocity']['west'],0,gamestate['z'])) ) ) == 0:
            gamestate['x'] = gamestate['x'] - gamestate['player']['velocity']['west']
            print('Moving!')
        if gamestate['player']['velocity']['south'] > 0 and      masks['level'].overlap_area( masks['player'] , ( math.floor(calcX(gamestate['x'],0,gamestate['z']+gamestate['player']['velocity']['south'])) , math.floor(calcY(gamestate['x'],0,gamestate['z']+gamestate['player']['velocity']['south'])) ) ) == 0:
            gamestate['z'] = gamestate['z'] + gamestate['player']['velocity']['south']
            print('Moving!')
        if gamestate['player']['velocity']['east'] > 0 and       masks['level'].overlap_area( masks['player'] , ( math.floor(calcX(gamestate['x']+gamestate['player']['velocity']['east'],0,gamestate['z'])) , math.floor(calcY(gamestate['x']+gamestate['player']['velocity']['east'],0,gamestate['z'])) ) ) == 0:
            gamestate['x'] = gamestate['x'] + gamestate['player']['velocity']['east']
            print('Moving!')


        # Maintain constant framerate.
 
        while True: 
            if time.process_time() - timeStart > 0.03: #0.03
                pygame.display.update()
                break

loadAssets()
loadLevel()
for mask in masks:
    print(str(masks[mask].count()))


     
            

    
    
    
