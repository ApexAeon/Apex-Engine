import pygame, sys
from pygame.locals import *
from common import DISPLAYSURF
from common import FONT
import json
import time
import math
import sound
import pygame.mixer

pygame.mixer.init()

gamestate = json.loads(open('../data/save/new.json').read())
assets = {}
entities = {}
reslist = []
masks = {}
level = {}
assetlist = {}
data = {}

def tickDoor(obj): # For every door object in a level, this will run, with the specified parameters of each specific door.
    if gamestate['x'] >= obj['posdict']['x'] and gamestate['y'] >= obj['posdict']['y'] and gamestate['z'] >= obj['posdict']['z'] and gamestate['x'] <= obj['dposdict']['x'] and gamestate['y'] <= obj['dposdict']['y'] and gamestate['z'] <= obj['dposdict']['z']:
        # Take the player to the destination if they are within the boundaries of the door.
        gamestate['x'] = obj['exitposdict']['x']
        gamestate['y'] = obj['exitposdict']['y']
        gamestate['z'] = obj['exitposdict']['z']
        gamestate['realX'] = 200 + gamestate['x'] + gamestate['z']
        gamestate['realY'] = 200 + gamestate['x'] + gamestate['z'] + gamestate['y']
        gamestate['lvl'] = obj['exitlvl']
        gamestate['isMovingUp'] = False
        gamestate['isMovingDown'] = False
        gamestate['isMovingLeft'] = False
        gamestate['isMovingRight'] = False
        return 'CHANGELVL'
def tickKill(obj):
    if gamestate['x'] >= obj['posdict']['x'] and gamestate['y'] >= obj['posdict']['y'] and gamestate['z'] >= obj['posdict']['z'] and gamestate['x'] <= obj['dposdict']['x'] and gamestate['y'] <= obj['dposdict']['y'] and gamestate['z'] <= obj['dposdict']['z']:
        gamestate['isAlive'] = False
def loadAssets(): # Attempts to load all assets listed in assets.json into the assets dictionary. Replaced missing textures with error.png.
    assetlist = json.loads(open('../data/assets.json').read())
    for pair in assetlist:
        try:
            assets[pair[0]] = pygame.image.load(pair[1])
        except:
            assets[pair[0]] = pygame.image.load('../assets/error.png')
def getAsset(name):
    if name in assets:
        return assets[name]
    else:
        return pygame.image.load('../assets/error.png')
def getMask(name):
    if name in masks:
        return masks[name]
    else:
        return pygame.mask.from_surface(pygame.image.load('../assets/error.png'))
def loadAsset(filename): # Attempts to load a single image, if an error occurs, it loads the error texture instead.
    try:
        return pygame.image.load(filename)
    except:
        return pygame.image.load('../assets/error.png')
def getLevel(name):
    if name in level:
        return level[name]
            
def getGamestate(): # Will be used for saving gamestate.
    return gamestate
def setGamestate(gamestatein): # Will be used for loading gamestate.
    gamestate = gamestatein
def calcX(x, y, z): # Convert isometrric X values into actual screen coordinates.
    if gamestate['levelMode'] == 'iso':
        return ((x * 2 - z * 2) + 0.25 * (x-z)) * 4
    else:
        return x * 4
def calcY(x, y, z): # Convert isometrric Y values into actual screen coordinates.
    if gamestate['levelMode'] == 'iso':
        return ((x + z - y) + 0.25 * (x+z)) * 4
    else:
        return (z - y) * 4
def loadLevel():
    try:
        level['visual'] = loadAsset('../maps/' + gamestate['lvl'] + '/visual.png')
        level['bg'] = loadAsset('../maps/' + gamestate['lvl'] + '/walls.png')
        level['fg'] = loadAsset('../maps/' + gamestate['lvl'] + '/forground.png')
        level['cover'] = loadAsset('../maps/' + gamestate['lvl'] + '/cover.png')
        entities = json.loads(open('../maps/' + gamestate['lvl'] + '/entities.json').read())
        data = json.loads(open('../maps/' + gamestate['lvl'] + '/data.json').read())
        masks['level'] = pygame.mask.from_surface(loadAsset('../maps/' + gamestate['lvl'] + '/walls.png'))
        masks['player'] = pygame.mask.from_surface(loadAsset('../assets/sprites/player/hitbox.png'))
        gamestate['levelMode'] = data['levelMode']
    except:
        print ('Could not load json files!')
def start():
#
# Main Game Loop
#
    while True:
        if not gamestate['isAlive']:
            return 'DIE'
        gamestate['realX'] = calcX(gamestate['x'], gamestate['y'], gamestate['z'])
        gamestate['realY'] = calcY(gamestate['x'], gamestate['y'], gamestate['z'])

        timeStart = time.process_time() # Used to facilitate timing and FPS, see bottom of loop for more info.

        DISPLAYSURF.blit(getLevel('bg'), (0,0))
        DISPLAYSURF.blit(getLevel('visual'), (0,0))
        DISPLAYSURF.blit(getAsset('chardisplay'),(math.floor(gamestate['realX']),math.floor(gamestate['realY'])))
        DISPLAYSURF.blit(getLevel('cover'), (0,0))
        DISPLAYSURF.blit(getLevel('fg'), (0,0))

        for obj in entities: # Tick through every entity in the lvl
            if obj['type'] == 'door':
                if tickDoor(obj) == 'CHANGELVL':
                    return 'CHANGELVL'
            if obj['type'] == 'kill':
                tickKill(obj)
#
# Event Processing
#
        for event in pygame.event.get():
            if event.type is QUIT:
               pygame.quit()
               sys.exit()
            if event.type is KEYDOWN and event.key is K_ESCAPE:
                return 'PAUSE'
            
            if event.type is KEYDOWN and event.key is K_w:
                gamestate['isMovingUp'] = True
                gamestate['facing'] = 'up'               
                gamestate['isMoving'] = True
            if event.type is KEYDOWN and event.key is K_a:
                gamestate['isMovingLeft'] = True
                gamestate['facing'] = 'left'                
                gamestate['isMoving'] = True
            if event.type is KEYDOWN and event.key is K_s:
                gamestate['isMovingDown'] = True
                gamestate['facing'] = 'down'               
                gamestate['isMoving'] = True
            if event.type is KEYDOWN and event.key is K_d:
                gamestate['isMovingRight'] = True
                gamestate['facing'] = 'right'
                gamestate['isMoving'] = True
                
            if event.type is KEYDOWN and event.key is K_SPACE:
                gamestate['isJumping'] = True
                
            if event.type is KEYUP and event.key is K_w:
                gamestate['isMovingUp'] = False
            if event.type is KEYUP and event.key is K_a:
                gamestate['isMovingLeft'] = False
            if event.type is KEYUP and event.key is K_s:
                gamestate['isMovingDown'] = False
            if event.type is KEYUP and event.key is K_d:
                gamestate['isMovingRight'] = False
#
# Collision Detection and Movement
#
        if gamestate['isMovingUp'] and gamestate['velocity']['north'] != gamestate['speed']:
            if gamestate['velocity']['north'] + gamestate['acceleration'] > gamestate['speed']:
                gamestate['velocity']['north'] = gamestate['speed']
            else:
                gamestate['velocity']['north'] += gamestate['acceleration']
        if gamestate['isMovingDown'] and gamestate['velocity']['south'] != gamestate['speed']:
            if gamestate['velocity']['south'] + gamestate['acceleration'] > gamestate['speed']:
                gamestate['velocity']['south'] = gamestate['speed']
            else:
                gamestate['velocity']['south'] += gamestate['acceleration']
        if gamestate['isMovingLeft'] and gamestate['velocity']['west'] != gamestate['speed']:
            if gamestate['velocity']['west'] + gamestate['acceleration'] > gamestate['speed']:
                gamestate['velocity']['west'] = gamestate['speed']
            else:
                gamestate['velocity']['west'] += gamestate['acceleration']
        if gamestate['isMovingRight'] and gamestate['velocity']['east'] != gamestate['speed']:
            if gamestate['velocity']['east'] + gamestate['acceleration'] > gamestate['speed']:
                gamestate['velocity']['east'] = gamestate['speed']
            else:
                gamestate['velocity']['east'] += gamestate['acceleration']

        if not gamestate['isMovingUp'] and gamestate['velocity']['north'] > 0:
            if gamestate['velocity']['north'] - gamestate['acceleration'] >= 0:
                gamestate['velocity']['north'] -= gamestate['acceleration']
            else:
                gamestate['velocity']['north'] = 0                
        if not gamestate['isMovingDown'] and gamestate['velocity']['south'] > 0:
            if gamestate['velocity']['south'] - gamestate['acceleration'] >= 0:
                gamestate['velocity']['south'] -= gamestate['acceleration']
            else:
                gamestate['velocity']['south'] = 0                
        if not gamestate['isMovingLeft'] and gamestate['velocity']['west'] > 0:
            if gamestate['velocity']['west'] - gamestate['acceleration'] >= 0:
                gamestate['velocity']['west'] -= gamestate['acceleration']
            else:
                gamestate['velocity']['west'] = 0                
        if not gamestate['isMovingRight'] and gamestate['velocity']['east'] > 0:
            if gamestate['velocity']['east'] - gamestate['acceleration'] >= 0:
                gamestate['velocity']['east'] -= gamestate['acceleration']
            else:
                gamestate['velocity']['east'] = 0

                
        if gamestate['velocity']['north'] > 0 and getMask('level').overlap_area( getMask('player') , ( math.floor(calcX(gamestate['x'],0,gamestate['z']-gamestate['velocity']['north'])) , math.floor(calcY(gamestate['x'],0,gamestate['z']-gamestate['velocity']['north'])) ) ) is 0:
            gamestate['z'] = gamestate['z'] - gamestate['velocity']['north']
        if gamestate['velocity']['west'] > 0 and       getMask('level').overlap_area( getMask('player') , ( math.floor(calcX(gamestate['x']-gamestate['velocity']['west'],0,gamestate['z'])) , math.floor(calcY(gamestate['x']-gamestate['velocity']['west'],0,gamestate['z'])) ) ) is 0:
            gamestate['x'] = gamestate['x'] - gamestate['velocity']['west']
        if gamestate['velocity']['south'] > 0 and      getMask('level').overlap_area( getMask('player') , ( math.floor(calcX(gamestate['x'],0,gamestate['z']+gamestate['velocity']['south'])) , math.floor(calcY(gamestate['x'],0,gamestate['z']+gamestate['velocity']['south'])) ) ) is 0:
            gamestate['z'] = gamestate['z'] + gamestate['velocity']['south'] 
        if gamestate['velocity']['east'] > 0 and       getMask('level').overlap_area( getMask('player') , ( math.floor(calcX(gamestate['x']+gamestate['velocity']['east'],0,gamestate['z'])) , math.floor(calcY(gamestate['x']+gamestate['velocity']['east'],0,gamestate['z'])) ) ) is 0:
            gamestate['x'] = gamestate['x'] + gamestate['velocity']['east']
#
# Jumping
#
        if gamestate['isJumping']:
            if gamestate['jumpHeight'] is not 50:
                gamestate['y'] = gamestate['y'] + 5
                gamestate['realY'] = gamestate['realY'] - 5
                gamestate['jumpHeight'] = gamestate['jumpHeight'] + 5
            if gamestate['jumpHeight'] is 50 and gamestate['y'] is not 0:
                gamestate['y'] = gamestate['y'] - 5
                gamestate['realY'] = gamestate['realY'] + 5
            if gamestate['jumpHeight'] is 50 and gamestate['y'] is 0:
                gamestate['jumpHeight'] = 0
                gamestate['isJumping'] = 0
#
# Debug Coordinates
#
        DISPLAYSURF.blit(FONT.render('X: ' + str(gamestate['x']) + ' Y: ' + str(gamestate['y']) + ' Z: ' + str(gamestate['z']), True, (0, 128, 255), (0, 0, 0)), (25,25)) # Display current player position for dev use.
        DISPLAYSURF.blit(FONT.render('Nvel: ' + str(gamestate['velocity']['north']) + ' Evel: ' + str(gamestate['velocity']['east']) + ' Svel: ' + str(gamestate['velocity']['south']) + ' Wvel: ' + str(gamestate['velocity']['west']), True, (0, 128, 255), (0, 0, 0)), (25,500)) # Display current player position for dev use.

#
# Animations
#

        
        while True: # Delays time and makes sure a certain amount has passed since the last tick. Prevents crazy FPS and weird timing.
            if time.process_time() - timeStart > 0.03: #0.03
                pygame.display.update()
                break

loadAssets()
loadLevel()


     
            

    
    
    
