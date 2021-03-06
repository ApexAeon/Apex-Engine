import pygame, sys, json, time, math, pygame.mixer, resources, common
from pygame.locals import *
from resources import *
from common import *

def calcX(x, y, z): # Convert isometrric X values into actual screen coordinates.
    if gamestate['level_mode'] == 'isometric':
        return ((x * 2 - z * 2) + 0.25 * (x-z)) * 4
    elif gamestate['level_mode'] == 'scroll':
        return 1152/2
    else:
        return x * 4
def calcY(x, y, z): # Convert isometrric Y values into actual screen coordinates.
    if gamestate['level_mode'] == 'isometric':
        return ((x + z - y) + 0.25 * (x+z)) * 4
    elif gamestate['level_mode'] == 'scroll':
        return 648/2
    else:
        return (z - y) * 4

def calcLevelX(x, y, z):
    if gamestate['level_mode'] == "scroll":
        return (0-x)*4
    else:
        return 0
def calcLevelY(x, y, z):
    if gamestate['level_mode'] == "scroll":
        return (0-z)*4
    else:
        return 0

def start():
    options = json.loads(open('../data/options.json').read())
    assets['player_display'] = getAnimation(gamestate['player']['animation']['name'],gamestate['player']['direction'],math.floor(gamestate['player']['animation']['frame']),getAsset('player',assets))
    # Main Game Loop

    while True:
        if gamestate['player']['health'] <= 0:
            return "DIE"
        timeStart = time.process_time() # Maintain constant framerate.
        DISPLAYSURF.blit(resources.getLevel('visual', level),(math.floor(calcLevelX(gamestate['x'], gamestate['y'], gamestate['z'])),math.floor(calcLevelY(gamestate['x'], gamestate['y'], gamestate['z']))))
        DISPLAYSURF.blit(getAsset('player_display', assets),(math.floor(calcX(gamestate['x'], gamestate['y'], gamestate['z'])),math.floor(calcY(gamestate['x'], gamestate['y'], gamestate['z']))))
        DISPLAYSURF.blit(resources.getLevel('fg', level), (0,0))
        DISPLAYSURF.blit(FONT.render('HP '+str(int(gamestate['player']['health'])), False, (0, 0, 255)), (0,0))
        DISPLAYSURF.blit(FONT.render('AP '+str(int(gamestate['player']['armor'])), False, (0, 0, 255)), (0,30))
        DISPLAYSURF.blit(FONT.render('X '+str(int(gamestate['x'])), False, (0, 0, 255)), (0,100))
        DISPLAYSURF.blit(FONT.render('Z '+str(int(gamestate['z'])), False, (0, 0, 255)), (0,130))

        
        # Animations
        if gamestate['player']['velocity']['north'] > 0 or gamestate['player']['velocity']['south'] > 0 or gamestate['player']['velocity']['east'] > 0 or gamestate['player']['velocity']['west'] > 0:
            gamestate['player']['animation']['idle'] = False
            assets['player_display'] = getAnimation(gamestate['player']['animation']['name'],gamestate['player']['direction'],math.floor(gamestate['player']['animation']['frame']),getAsset('player',assets)) # Get the image for the current animation frame
            gamestate['player']['animation']['frame'] += gamestate['player']['animation']['speed'] # Increment the animation frame counter.
            if math.floor(gamestate['player']['animation']['frame']) == animation_lengths[gamestate['player']['animation']['name']]: # If the animation is finished then...
            	gamestate['player']['animation']['frame'] = 0.0 # Reset the frame counter.
        elif not gamestate['player']['animation']['idle']:
            assets['player_display'] = getAnimation(gamestate['player']['animation']['name'],gamestate['player']['direction'],0,getAsset('player',assets)) # Get the image for the current animation frame
            gamestate['player']['animation']['idle'] = True

        for entity in common.entities:
            entity.tick()

        # Health regen and overheal prevention
        if gamestate['player']['health'] < gamestate['player']['max_health']:
            gamestate['player']['health'] += gamestate['player']['regen_speed']
        if gamestate['player']['health'] > gamestate['player']['max_health']:
            gamestate['player']['health'] = gamestate['player']['max_health']

        # Event Processing
        if gamestate['player']['items'] and gamestate['player']['items'][gamestate['player']['selected_item']-1].data['count']>0:
            DISPLAYSURF.blit(loadAsset('../game/assets/items/'+gamestate['player']['items'][gamestate['player']['selected_item']-1].data['image']+'.png'), (0,0))
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

            if event.type is KEYDOWN and pygame.key.name(event.key) is options['keybinds']['action_use']:
                if gamestate['player']['items']:
                    gamestate['player']['items'][gamestate['player']['selected_item']-1].use()
            if event.type is KEYDOWN and pygame.key.name(event.key) is options['keybinds']['action_switch']:
                gamestate['action_switch'] = True

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
        if gamestate['level_mode'] == 'scroll':
            if gamestate['player']['velocity']['north'] > 0 and     masks['level'].overlap_area(masks['player'],(math.floor(gamestate['x']*4+(1152/2)),math.floor((gamestate['z']-gamestate['player']['velocity']['north'])*4+(648/2))))==0:
                gamestate['z'] = gamestate['z'] - gamestate['player']['velocity']['north']
            if gamestate['player']['velocity']['west'] > 0 and      masks['level'].overlap_area(masks['player'],(math.floor((gamestate['x']-gamestate['player']['velocity']['west'])*4+(1152/2)),math.floor(gamestate['z']*4+(648/2))))==0:
                gamestate['x'] = gamestate['x'] - gamestate['player']['velocity']['west']
            if gamestate['player']['velocity']['south'] > 0 and     masks['level'].overlap_area(masks['player'],(math.floor(gamestate['x']*4+(1152/2)),math.floor((gamestate['z']+gamestate['player']['velocity']['south'])*4+(648/2))))==0:
                gamestate['z'] = gamestate['z'] + gamestate['player']['velocity']['south']
            if gamestate['player']['velocity']['east'] > 0 and      masks['level'].overlap_area(masks['player'],(math.floor((gamestate['x']+gamestate['player']['velocity']['east'])*4+(1152/2)),math.floor(gamestate['z']*4+(648/2))))==0:
                gamestate['x'] = gamestate['x'] + gamestate['player']['velocity']['east']
        else:
            if gamestate['player']['velocity']['north'] > 0 and masks['level'].overlap_area( masks['player'] , ( math.floor(calcX(gamestate['x'],0,gamestate['z']-gamestate['player']['velocity']['north'])) , math.floor(calcY(gamestate['x'],0,gamestate['z']-gamestate['player']['velocity']['north'])) ) ) == 0:
                gamestate['z'] = gamestate['z'] - gamestate['player']['velocity']['north']
            if gamestate['player']['velocity']['west'] > 0 and       masks['level'].overlap_area( masks['player'] , ( math.floor(calcX(gamestate['x']-gamestate['player']['velocity']['west'],0,gamestate['z'])) , math.floor(calcY(gamestate['x']-gamestate['player']['velocity']['west'],0,gamestate['z'])) ) ) == 0:
                gamestate['x'] = gamestate['x'] - gamestate['player']['velocity']['west']
            if gamestate['player']['velocity']['south'] > 0 and      masks['level'].overlap_area( masks['player'] , ( math.floor(calcX(gamestate['x'],0,gamestate['z']+gamestate['player']['velocity']['south'])) , math.floor(calcY(gamestate['x'],0,gamestate['z']+gamestate['player']['velocity']['south'])) ) ) == 0:
                gamestate['z'] = gamestate['z'] + gamestate['player']['velocity']['south']
            if gamestate['player']['velocity']['east'] > 0 and       masks['level'].overlap_area( masks['player'] , ( math.floor(calcX(gamestate['x']+gamestate['player']['velocity']['east'],0,gamestate['z'])) , math.floor(calcY(gamestate['x']+gamestate['player']['velocity']['east'],0,gamestate['z'])) ) ) == 0:
                gamestate['x'] = gamestate['x'] + gamestate['player']['velocity']['east']

        # Maintain constant framerate.

        while True:
            if time.process_time() - timeStart > 0.03: #0.03
                common.scale()
                pygame.display.update()
                break
