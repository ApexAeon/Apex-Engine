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

gs = json.loads(open('../data/save/new.json').read())
res = {}
entities = {}
mapdata = {}

def tickDoor(obj): # For every door object in a level, this will run, with the specified parameters of each specific door.
    if gs['x'] >= obj['posdict']['x'] and gs['y'] >= obj['posdict']['y'] and gs['z'] >= obj['posdict']['z'] and gs['x'] <= obj['dposdict']['x'] and gs['y'] <= obj['dposdict']['y'] and gs['z'] <= obj['dposdict']['z']:
        # Take the player to the destination if they are within the boundaries of the door.
        gs['x'] = obj['exitposdict']['x']
        gs['y'] = obj['exitposdict']['y']
        gs['z'] = obj['exitposdict']['z']
        gs['realX'] = 200 + gs['x'] + gs['z']
        gs['realY'] = 200 + gs['x'] + gs['z'] + gs['y']
        gs['lvl'] = obj['exitlvl']
        gs['isMovingUp'] = False
        gs['isMovingDown'] = False
        gs['isMovingLeft'] = False
        gs['isMovingRight'] = False
        return 'CHANGELVL'
def tickKill(obj):
    if gs['x'] >= obj['posdict']['x'] and gs['y'] >= obj['posdict']['y'] and gs['z'] >= obj['posdict']['z'] and gs['x'] <= obj['dposdict']['x'] and gs['y'] <= obj['dposdict']['y'] and gs['z'] <= obj['dposdict']['z']:
        gs['isAlive'] = False

def getGamestate(): # Will be used for saving gamestate.
    return gs
def setGamestate(gsin): # Will be used for loading gamestate.
    gs = gsin
def calcX(x, y, z): # Convert isometrric X values into actual screen coordinates.
    return ((x * 2 - z * 2) + 0.25 * (x-z)) * 4
def calcY(x, y, z): # Convert isometrric Y values into actual screen coordinates.
    return ((x + z - y) + 0.25 * (x+z)) * 4
def load():
    res['hitbox'] = pygame.image.load('../assets/error.png')
    res['lvl'] = pygame.image.load('../maps/error/visual.png')
    res['walls'] = pygame.image.load('../maps/error/walls.png')
    entities = json.loads(open('../maps/error/entities.json').read())
    res['lvlmask'] = pygame.mask.from_surface(res['walls'])
    res['hitmask'] = pygame.mask.from_surface(res['hitbox'])
    mapdata = json.loads(open('../maps/error/data.json').read())
    res['stepsounds'] = pygame.mixer.Sound('../assets/sounds/error.wav')
    res['charNorthWalk1'] = pygame.image.load('../assets/error.png')
    res['charNorthWalk2'] = pygame.image.load('../assets/error.png')
    res['charNorthIdle'] = pygame.image.load('../assets/error.png')
    res['charSouthWalk1'] = pygame.image.load('../assets/error.png')
    res['charSouthWalk2'] = pygame.image.load('../assets/error.png')
    res['charSouthIdle'] = pygame.image.load('../assets/error.png')
    res['charEastWalk1'] = pygame.image.load('../assets/error.png')
    res['charEastWalk2'] = pygame.image.load('../assets/error.png')
    res['charEastIdle'] = pygame.image.load('../assets/error.png')
    res['charWestWalk1'] = pygame.image.load('../assets/error.png')
    res['charWestWalk2'] = pygame.image.load('../assets/error.png')
    res['charWestIdle'] = pygame.image.load('../assets/error.png')
    res['charNortheastWalk1'] = pygame.image.load('../assets/error.png')
    res['charNortheastWalk2'] = pygame.image.load('../assets/error.png')
    res['charNortheastIdle'] = pygame.image.load('../assets/error.png')
    res['charNorthwestWalk1'] = pygame.image.load('../assets/error.png')
    res['charNorthwestWalk2'] = pygame.image.load('../assets/error.png')
    res['charNorthwestIdle'] = pygame.image.load('../assets/error.png')
    res['charSoutheastWalk1'] = pygame.image.load('../assets/error.png')
    res['charSoutheastWalk2'] = pygame.image.load('../assets/error.png')
    res['charSoutheastIdle'] = pygame.image.load('../assets/error.png')
    res['charSouthwestWalk1'] = pygame.image.load('../assets/error.png')
    res['charSouthwestWalk2'] = pygame.image.load('../assets/error.png')
    res['charSouthwestIdle'] = pygame.image.load('../assets/error.png')
    res['chardisplay'] = res['charEastIdle']
    try:
        res['hitbox'] = pygame.image.load('../assets/sprites/player/hitbox.png')
        res['lvl'] = pygame.image.load('../maps/' + gs['lvl'] + '/visual.png')
        res['walls'] = pygame.image.load('../maps/' + gs['lvl'] + '/walls.png')
        entities = json.loads(open('../maps/' + gs['lvl'] + '/entities.json').read())
        res['lvlmask'] = pygame.mask.from_surface(res['walls'])
        res['hitmask'] = pygame.mask.from_surface(res['hitbox'])
        mapdata = json.loads(open('../maps/' + gs['lvl'] + '/data.json').read())
        sound.play(mapdata['sounds'])
        res['stepsounds'] = pygame.mixer.Sound('../assets/sounds/player/step.wav')
        gs['isLoaded'] = True
        res['charNorthWalk1'] = pygame.image.load('../assets/sprites/player/north/walk1.png')
        res['charNorthWalk2'] = pygame.image.load('../assets/sprites/player/north/walk2.png')
        res['charNorthIdle'] = pygame.image.load('../assets/sprites/player/north/idle.png')
        
        res['charSouthWalk1'] = pygame.image.load('../assets/sprites/player/south/walk1.png')
        res['charSouthWalk2'] = pygame.image.load('../assets/sprites/player/south/walk2.png')
        res['charSouthIdle'] = pygame.image.load('../assets/sprites/player/south/idle.png')
        
        res['charEastWalk1'] = pygame.image.load('../assets/sprites/player/east/walk1.png')
        res['charEastWalk2'] = pygame.image.load('../assets/sprites/player/east/walk2.png')
        res['charEastIdle'] = pygame.image.load('../assets/sprites/player/east/idle.png')
        
        res['charWestWalk1'] = pygame.image.load('../assets/sprites/player/west/walk1.png')
        res['charWestWalk2'] = pygame.image.load('../assets/sprites/player/west/walk2.png')
        res['charWestIdle'] = pygame.image.load('../assets/sprites/player/west/idle.png')
        
        res['charNortheastWalk1'] = pygame.image.load('../assets/sprites/player/northeast/walk1.png')
        res['charNortheastWalk2'] = pygame.image.load('../assets/sprites/player/northeast/walk2.png')
        res['charNortheastIdle'] = pygame.image.load('../assets/sprites/player/northeast/idle.png')
        
        res['charNorthwestWalk1'] = pygame.image.load('../assets/error.png')
        res['charNorthwestWalk2'] = pygame.image.load('../assets/error.png')
        res['charNorthwestIdle'] = pygame.image.load('../assets/error.png')
        
        res['charSoutheastWalk1'] = pygame.image.load('../assets/error.png')
        res['charSoutheastWalk2'] = pygame.image.load('../assets/error.png')
        res['charSoutheastIdle'] = pygame.image.load('../assets/error.png')
        
        res['charSouthwestWalk1'] = pygame.image.load('../assets/sprites/player/southwest/walk1.png')
        res['charSouthwestWalk2'] = pygame.image.load('../assets/sprites/player/southwest/walk2.png')
        res['charSouthwestIdle'] = pygame.image.load('../assets/sprites/player/southwest/idle.png')

        res['chardisplay'] = res['charEastIdle']
    except:
        print("Missing or empty resources.")

    
    
def start():
    if not gs['isLoaded']:
        load()
    
#
# Main Game Loop
#
    while True:
        sound.ping()
        if not gs['isAlive']:
            return 'DIE'
        gs['realX'] = calcX(gs['x'], gs['y'], gs['z'])
        gs['realY'] = calcY(gs['x'], gs['y'], gs['z'])

        timeStart = time.process_time() # Used to facilitate timing and FPS, see bottom of loop for more info.

        DISPLAYSURF.blit(res['lvl'], (0,0))
        DISPLAYSURF.blit(res['chardisplay'],(math.floor(gs['realX']),math.floor(gs['realY'])))

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
                gs['isMovingUp'] = True
                gs['facing'] = 'up'               
                gs['isMoving'] = True
            if event.type is KEYDOWN and event.key is K_a:
                gs['isMovingLeft'] = True
                gs['facing'] = 'left'                
                gs['isMoving'] = True
            if event.type is KEYDOWN and event.key is K_s:
                gs['isMovingDown'] = True
                gs['facing'] = 'down'               
                gs['isMoving'] = True
            if event.type is KEYDOWN and event.key is K_d:
                gs['isMovingRight'] = True
                gs['facing'] = 'right'
                gs['isMoving'] = True
                
            if event.type is KEYDOWN and event.key is K_SPACE:
                gs['isJumping'] = True
                
            if event.type is KEYUP and event.key is K_w:
                gs['isMovingUp'] = False
            if event.type is KEYUP and event.key is K_a:
                gs['isMovingLeft'] = False
            if event.type is KEYUP and event.key is K_s:
                gs['isMovingDown'] = False
            if event.type is KEYUP and event.key is K_d:
                gs['isMovingRight'] = False
#
# Collision Detection and Movement
#
        if gs['isMovingUp'] and gs['velocity']['north'] != gs['speed']:
            if gs['velocity']['north'] + gs['acceleration'] > gs['speed']:
                gs['velocity']['north'] = gs['speed']
            else:
                gs['velocity']['north'] += gs['acceleration']
        if gs['isMovingDown'] and gs['velocity']['south'] != gs['speed']:
            if gs['velocity']['south'] + gs['acceleration'] > gs['speed']:
                gs['velocity']['south'] = gs['speed']
            else:
                gs['velocity']['south'] += gs['acceleration']
        if gs['isMovingLeft'] and gs['velocity']['west'] != gs['speed']:
            if gs['velocity']['west'] + gs['acceleration'] > gs['speed']:
                gs['velocity']['west'] = gs['speed']
            else:
                gs['velocity']['west'] += gs['acceleration']
        if gs['isMovingRight'] and gs['velocity']['east'] != gs['speed']:
            if gs['velocity']['east'] + gs['acceleration'] > gs['speed']:
                gs['velocity']['east'] = gs['speed']
            else:
                gs['velocity']['east'] += gs['acceleration']

        if not gs['isMovingUp'] and gs['velocity']['north'] > 0:
            if gs['velocity']['north'] - gs['acceleration'] >= 0:
                gs['velocity']['north'] -= gs['acceleration']
            else:
                gs['velocity']['north'] = 0                
        if not gs['isMovingDown'] and gs['velocity']['south'] > 0:
            if gs['velocity']['south'] - gs['acceleration'] >= 0:
                gs['velocity']['south'] -= gs['acceleration']
            else:
                gs['velocity']['south'] = 0                
        if not gs['isMovingLeft'] and gs['velocity']['west'] > 0:
            if gs['velocity']['west'] - gs['acceleration'] >= 0:
                gs['velocity']['west'] -= gs['acceleration']
            else:
                gs['velocity']['west'] = 0                
        if not gs['isMovingRight'] and gs['velocity']['east'] > 0:
            if gs['velocity']['east'] - gs['acceleration'] >= 0:
                gs['velocity']['east'] -= gs['acceleration']
            else:
                gs['velocity']['east'] = 0

                
        if gs['velocity']['north'] > 0 and     res['lvlmask'].overlap_area( res['hitmask'] , ( math.floor(calcX(gs['x'],0,gs['z']-gs['velocity']['north'])) , math.floor(calcY(gs['x'],0,gs['z']-gs['velocity']['north'])) ) ) is 0:
            gs['z'] = gs['z'] - gs['velocity']['north']
        if gs['velocity']['west'] > 0 and   res['lvlmask'].overlap_area( res['hitmask'] , ( math.floor(calcX(gs['x']-gs['velocity']['west'],0,gs['z'])) , math.floor(calcY(gs['x']-gs['velocity']['west'],0,gs['z'])) ) ) is 0:
            gs['x'] = gs['x'] - gs['velocity']['west']
        if gs['velocity']['south'] > 0 and   res['lvlmask'].overlap_area( res['hitmask'] , ( math.floor(calcX(gs['x'],0,gs['z']+gs['velocity']['south'])) , math.floor(calcY(gs['x'],0,gs['z']+gs['velocity']['south'])) ) ) is 0:
            gs['z'] = gs['z'] + gs['velocity']['south'] 
        if gs['velocity']['east'] > 0 and  res['lvlmask'].overlap_area( res['hitmask'] , ( math.floor(calcX(gs['x']+gs['velocity']['east'],0,gs['z'])) , math.floor(calcY(gs['x']+gs['velocity']['east'],0,gs['z'])) ) ) is 0:
            gs['x'] = gs['x'] + gs['velocity']['east']
#
# Jumping
#
        if gs['isJumping']:
            if gs['jumpHeight'] is not 50:
                gs['y'] = gs['y'] + 5
                gs['realY'] = gs['realY'] - 5
                gs['jumpHeight'] = gs['jumpHeight'] + 5
            if gs['jumpHeight'] is 50 and gs['y'] is not 0:
                gs['y'] = gs['y'] - 5
                gs['realY'] = gs['realY'] + 5
            if gs['jumpHeight'] is 50 and gs['y'] is 0:
                gs['jumpHeight'] = 0
                gs['isJumping'] = 0
#
# Debug Coordinates
#
        DISPLAYSURF.blit(FONT.render('X: ' + str(gs['x']) + ' Y: ' + str(gs['y']) + ' Z: ' + str(gs['z']), True, (0, 128, 255), (0, 0, 0)), (25,25)) # Display current player position for dev use.
        DISPLAYSURF.blit(FONT.render('Nvel: ' + str(gs['velocity']['north']) + ' Evel: ' + str(gs['velocity']['east']) + ' Svel: ' + str(gs['velocity']['south']) + ' Wvel: ' + str(gs['velocity']['west']), True, (0, 128, 255), (0, 0, 0)), (25,500)) # Display current player position for dev use.

#
# Animations
#
        if gs['velocity']['north'] + gs['velocity']['south'] + gs['velocity']['east'] + gs['velocity']['west'] is 0:
            if gs['facing'] == "left":
                res['chardisplay'] = res['charWestIdle']
            if gs['facing'] == "right":
                res['chardisplay'] = res['charEastIdle']
            if gs['facing'] == "up":
                res['chardisplay'] = res['charNorthIdle']
            if gs['facing'] == "down":
                res['chardisplay'] = res['charSouthIdle']
        
        
        while True: # Delays time and makes sure a certain amount has passed since the last tick. Prevents crazy FPS and weird timing.
            if time.process_time() - timeStart > 0.03: #0.03
                pygame.display.update()
                break

     
            

    
    
    
