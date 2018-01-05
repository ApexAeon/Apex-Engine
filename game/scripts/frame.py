import pygame, sys
from pygame.locals import *
import json
from enum import Enum
import game
from common import DISPLAYSURF
from common import FONT

menu_assets = {}

def loadMenuAssets(): # Attempts to load all assets listed in assets.json into the assets dictionary. Replaced missing textures with error texture.
    assetlist = json.loads(open('../data/menu_assets.json').read())
    for pair in assetlist:
        try:
            menu_assets[pair[0]] = pygame.image.load(pair[1])
        except:
            menu_assets[pair[0]] = pygame.Surface((25, 25))

def getMenuAsset(name): # Get an already loaded asset, if asset not found, replace with error texture.
    if name in menu_assets:
        return menu_assets[name]
    else:
        return pygame.Surface((25, 25))

def loadMenuAsset(filename): # Attempts to load a single image, if an error occurs, it loads the error texture instead.
    try:
        return pygame.image.load(filename)
    except:
        return pygame.Surface((25, 25))

class GameMode(Enum):
    mainmenu = 0
    options = 1
    save = 2
    load = 3
    paused = 4
    console = 5
    error = 6
    playing = 7
    gameover = 8

drawn = False
paused = False

def writescreen(strin, pos):
    DISPLAYSURF.blit(FONT.render(strin, True, (0, 128, 255)), pos)

gamemode = GameMode.mainmenu
selected = 1
gameinfo = open('..\\data\\gameinfo.json','r') # Load the gameinfo file
parsed = json.loads(gameinfo.read()) # Parse gaminfo's JSON into a dictionary
    
pygame.init()
DISPLAYSURF = pygame.display.set_mode((828, 640))
pygame.display.set_caption(parsed['name'])
pygame.display.set_icon(getMenuAsset('icon'))
FONT = pygame.font.SysFont('Bauhaus 93 Regular', 40)

while True: # Main loop

    for event in pygame.event.get():

        if event.type is QUIT:
            pygame.quit()
            sys.exit()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if gamemode is GameMode.mainmenu: # Code for the main menu. 

            DISPLAYSURF.blit(getMenuAsset('cover'), (0, 0))

            if selected is 5:
                selected = 1
            if selected is 0:
                selected = 4

            if selected is 1:
                DISPLAYSURF.blit(getMenuAsset('main_menu_selected_play'), (0, 0))
            if selected is 2:
                DISPLAYSURF.blit(getMenuAsset('main_menu_selected_load'), (0, 0))
            if selected is 3:
                DISPLAYSURF.blit(getMenuAsset('main_menu_selected_options'), (0, 0))
            if selected is 4:
                DISPLAYSURF.blit(getMenuAsset('main_menu_selected_quit'), (0, 0))

            if event.type is KEYDOWN and event.key is K_RETURN:
                if selected is 1:
                    gamemode = GameMode.playing
                if selected is 2:
                    gamemode = GameMode.load
                if selected is 3:
                    gamemode = GameMode.options
                if selected is 4:
                    pygame.quit()
                    sys.exit()
                    
            if event.type is KEYDOWN and (event.key == K_DOWN or event.key == K_RIGHT):
                selected = selected + 1
            if event.type is KEYDOWN and (event.key == K_UP or event.key == K_LEFT):
                selected = selected - 1
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if gamemode is GameMode.load:
            DISPLAYSURF.blit(getMenuAsset('cover'), (0, 0))
            game.setGamestate(json.loads(open('../data/save/save.json','r').read()))
            gamemode = GameMode.playing
            paused = False
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if gamemode is GameMode.save:
            DISPLAYSURF.blit(getMenuAsset('cover'), (0, 0))
            open('../data/save/save.json','w').truncate()
            open('../data/save/save.json','w').write(json.dumps(game.getGamestate()))
            if paused:
                gamemode = GameMode.paused
            else:
                gamemode = GameMode.mainmenu
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if gamemode is GameMode.options:
            DISPLAYSURF.blit(getMenuAsset(getMenuAsset('cover')), (0, 0))
            writescreen( 'Options are currently not available. Please exit the program XD.' , (25,25) )
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if gamemode is GameMode.paused:
            paused = True
            DISPLAYSURF.blit(getMenuAsset('main_menu_screen'), (0, 0))
            DISPLAYSURF.blit(getMenuAsset('pause_menu_screen'), (0,0))

            if selected is 6:
                selected = 1
            if selected is 0:
                selected = 5
                
            if selected is 1:
                DISPLAYSURF.blit(getMenuAsset('pause_menu_selected_resume'), (0, 0))
            if selected is 2:
                DISPLAYSURF.blit(getMenuAsset('pause_menu_selected_save'), (0, 0))
            if selected is 3:
                DISPLAYSURF.blit(getMenuAsset('pause_menu_selected_load'), (0, 0))
            if selected is 4:
                DISPLAYSURF.blit(getMenuAsset('pause_menu_selected_options'), (0, 0))
            if selected is 5:
                DISPLAYSURF.blit(getMenuAsset('pause_menu_selected_quit'), (0, 0))

            if event.type is KEYDOWN and event.key is K_RETURN:
                if selected is 1:
                    gamemode = GameMode.playing
                    paused = False
                if selected is 2:
                    gamemode = GameMode.save
                if selected is 3:
                    gamemode = GameMode.load
                if selected is 4:
                    gamemode = GameMode.options
                if selected is 5:
                    pygame.quit()
                    sys.exit()

            if event.type is KEYDOWN and (event.key == K_DOWN or event.key == K_RIGHT):
                selected = selected + 1
            if event.type is KEYDOWN and (event.key == K_UP or event.key == K_LEFT):
                selected = selected - 1
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if gamemode is GameMode.playing:
            try:
                gamemsg = game.start()
                if gamemsg is 'PAUSE':
                    gamemode = GameMode.paused
                elif gamemsg is 'DIE':
                    gamemode = GameMode.gameover
            except IOError:
                DISPLAYSURF.blit(getMenuAsset('cover'), (0, 0))
                writescreen('File read error. IO.',(25,50))
            except ValueError:
                DISPLAYSURF.blit(getMenuAsset('cover'), (0, 0))
                writescreen('File read error. Value.',(25,50))
            except ImportError:
                DISPLAYSURF.blit(getMenuAsset('cover'), (0, 0))
                writescreen('Module import error.',(25,50))
            except EOFError:
                DISPLAYSURF.blit(getMenuAsset('cover'), (0, 0))
                writescreen('File read error. EOF.',(25,50))
            except KeyboardInterrupt:
                DISPLAYSURF.blit(getMenuAsset('cover'), (0, 0))
                writescreen('Operation cancel error.',(25,50))
            except:
                DISPLAYSURF.blit(getMenuAsset('cover'), (0, 0))
                writescreen('Unknown error.',(25,50))

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if gamemode is GameMode.gameover:
            DISPLAYSURF.blit(getMenuAsset('gameoverscreen'), (0,0))
            writescreen('Yes',(25,175))
            writescreen('No',(25,200))
            if event.type is KEYDOWN and event.key is K_RETURN:
                if selected is 1:
                    gamemode = GameMode.playing
                if selected is 2:
                    pygame.quit()
                    sys.exit()

            if event.type is KEYDOWN and event.key is K_s:
                selected = selected + 1
            if event.type is KEYDOWN and event.key is K_w:
                selected = selected - 1

            if selected is 3:
                selected = 1
            if selected is 0:
                selected = 2

            if selected is 1:
                DISPLAYSURF.blit(FONT.render('Yes', True, (255, 140, 0)), (25, 175))
            if selected is 2:
                DISPLAYSURF.blit(FONT.render('No', True, (255, 140, 0)), (25, 200))
                
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        pygame.display.update()


#            somebody once told me the world was macoroni
#            so i took a bite out of a tree
#            it tasted pretty funny
#            so i spit it at a bunny
            
            
