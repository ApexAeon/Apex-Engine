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
last_id = -1
class Generic():
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick(self):
        pass
    def trigger(self):
        pass
class Tele(): # On a trigger input, they are teleported to another area of the same or different room.
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick(self):
        print('Object "' + self.data['name'] + '" # ' + str(self.uid) + ' of type "tele" was ticked!')
    def trigger(self):
        gamestate['x'] = self.data['x']
        gamestate['y'] = self.data['y']
        gamestate['z'] = self.data['z']
class Pickup(): # On player contact, executes some action such as putting an item into the players inventory, then becomes inactive and dissapears.
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick(self):
        pass
    def trigger(self):
        pass

class Prop(): # Something that displays a sprite.
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
        level['props']={data['prop']:{"sprite":loadAsset('../game/assets/props/'+data['prop']+'.png')}}
        #level['props'][data[prop]]['hitbox'] = loadAsset(data[prop])
    def tick(self):
        DISPLAYSURF.blit(getLevel('props')[self.data['prop']]['sprite'], (self.data['x'],self.data['y']))
    def trigger(self):
        pass
class Change(): # On a trigger input, can change the state of itself or any other entity. Example: On input, change "propfile" of "entity-360" to "chair.png."
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick(self):
        pass
    def trigger(self):
        pass
class Trigger(): # On arbitrary met condition, trigger another object's trigerable input.
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick(self):
        print('Object "' + self.data['name'] + '" # ' + str(self.uid) + ' of type "trigger" was ticked!')
        if gamestate['x'] >= self.data['x_minimum'] and gamestate['y'] >= self.data['y_minimum'] and gamestate['z'] >= self.data['z_minimum'] and gamestate['x'] <= self.data['x_maximum'] and gamestate['y'] <= self.data['y_maximum'] and gamestate['z'] <= self.data['z_maximum']:
            triggermain(self.data['output'])
    def trigger(self):
        pass
class Spawner(): # On a trigger input, creates a new entity.
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick(self):
        pass
    def trigger(self):
        pass
class Hurt():
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick(self):
        pass
    def trigger(self):
        if self.data['bypass']:
            if self.data['set']:
                gamestate['player']['health'] = self.data['health']
            elif self.data['change']:
                gamestate['player']['health'] -= self.data['health']
        else:
            gamestate['player']['armor'] -= gamestate['player']['armor_percent'] * self.data['health'] # Hit the armor.
            gamestate['player']['health'] -= self.data['health'] - (gamestate['player']['armor_percent'] * self.data['health']) # Hit the player.
            if gamestate['player']['armor'] < 0:
                gamestate['player']['health'] += gamestate['player']['armor']
                gamestate['player']['armor'] = 0
        if gamestate['player']['health'] > gamestate['player']['max_health']:
            gamestate['player']['health'] = gamestate['player']['max_health']
        
def spawn(data):
    if data['type'] == 'generic':
        return Generic(data, last_id + 1)
    elif data['type'] == 'tele':
        return Tele(data, last_id + 1)
    elif data['type'] == 'pickup':
        return Pickup(data, last_id + 1)
    elif data['type'] == 'prop':
        return Prop(data, last_id + 1)
    elif data['type'] == 'change':
        return Change(data, last_id + 1)
    elif data['type'] == 'trigger':
        return Trigger(data, last_id + 1)
    elif data['type'] == 'spawner':
        return Spawner(data, last_id + 1)


def triggermain(name):
    for entity in entities:
        if entity.data['name'] == name:
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
    level['fg'] = loadAsset('../game/maps/' + gamestate['lvl'] + '/fg.png')
    for entity in json.loads(open('../game/maps/' + gamestate['lvl'] + '/entities.json').read()):
        entities.append(spawn(entity))
    data = json.loads(open('../game/maps/' + gamestate['lvl'] + '/data.json').read())
    masks['level'] = pygame.mask.from_surface(getLevel('walls'))
    masks['player'] = pygame.mask.from_surface(getAsset('player_hitbox'))
    gamestate['level_mode'] = data['level_mode']
def start():
    options = json.loads(open('../data/options.json').read())

    # Main Game Loop

    while True:
        timeStart = time.process_time() # Maintain constant framerate.
        DISPLAYSURF.blit(getLevel('visual'), (0,0))
        DISPLAYSURF.blit(getAsset('chardisplay'),(math.floor(calcX(gamestate['x'], gamestate['y'], gamestate['z'])),math.floor(calcY(gamestate['x'], gamestate['y'], gamestate['z']))))
        DISPLAYSURF.blit(getLevel('fg'), (0,0))

        if not gamestate['isMoving']:
            assets['chardisplay'] = getAsset(gamestate['player']['direction']+'_idle')
        for entity in entities:
            entity.tick()

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
                gamestate['player']['direction'] = 'north'
            if event.type is KEYDOWN and pygame.key.name(event.key) is options['keybinds']['action_west']:
                gamestate['action_west'] = True
                gamestate['player']['direction'] = 'west'
            if event.type is KEYDOWN and pygame.key.name(event.key) is options['keybinds']['action_south']:
                gamestate['action_south'] = True
                gamestate['player']['direction'] = 'south'
            if event.type is KEYDOWN and pygame.key.name(event.key) is options['keybinds']['action_east']:
                gamestate['action_east'] = True
                gamestate['player']['direction'] = 'east'
                
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
        if gamestate['player']['velocity']['west'] > 0 and       masks['level'].overlap_area( masks['player'] , ( math.floor(calcX(gamestate['x']-gamestate['player']['velocity']['west'],0,gamestate['z'])) , math.floor(calcY(gamestate['x']-gamestate['player']['velocity']['west'],0,gamestate['z'])) ) ) == 0:
            gamestate['x'] = gamestate['x'] - gamestate['player']['velocity']['west']
        if gamestate['player']['velocity']['south'] > 0 and      masks['level'].overlap_area( masks['player'] , ( math.floor(calcX(gamestate['x'],0,gamestate['z']+gamestate['player']['velocity']['south'])) , math.floor(calcY(gamestate['x'],0,gamestate['z']+gamestate['player']['velocity']['south'])) ) ) == 0:
            gamestate['z'] = gamestate['z'] + gamestate['player']['velocity']['south']
        if gamestate['player']['velocity']['east'] > 0 and       masks['level'].overlap_area( masks['player'] , ( math.floor(calcX(gamestate['x']+gamestate['player']['velocity']['east'],0,gamestate['z'])) , math.floor(calcY(gamestate['x']+gamestate['player']['velocity']['east'],0,gamestate['z'])) ) ) == 0:
            gamestate['x'] = gamestate['x'] + gamestate['player']['velocity']['east']

        print(gamestate['x'],gamestate['z'])

        # Maintain constant framerate.

        while True: 
            if time.process_time() - timeStart > 0.03: #0.03
                pygame.display.update()
                break

loadAssets()
loadLevel()
     
            

    
    
    
