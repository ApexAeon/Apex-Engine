from pygame.locals import *
import game, dialog, json, pygame, sys
from common import *
load()
menuAssets = {}
def loadMenuAssets(): # Attempts to load all assets listed in assets.json into the assets dictionary. Replaced missing textures with error texture.
    assetList = json.loads(open('../game/metadata/menu_asset_list.json').read())
    for pair in assetList:
        try:
            menuAssets[pair] = pygame.image.load('../game/assets/' + assetList[pair])
        except:
            menuAssets[pair] = pygame.Surface((25, 25))
def getMenuAsset(name): # Get an already loaded asset, if asset not found, replace with error texture.
    if name in menuAssets:
        return menuAssets[name]
    else:
        return pygame.Surface((25, 25))
def loadMenuAsset(filename): # Attempts to load a single image, if an error occurs, it loads the error texture instead.
    try:
        return pygame.image.load(filename)
    except:
        return pygame.Surface((25, 25))
loadMenuAssets()
paused = False
mode = 'main'
selected = 1
info = json.loads(open('../game/metadata/info.json','r').read())
pygame.init()
DISPLAYSURF = pygame.display.set_mode((1152, 648),pygame.FULLSCREEN)
pygame.display.set_caption(info['name'])
pygame.display.set_icon(getMenuAsset('icon'))
options = json.loads(open('../data/options.json','r').read())
FONT = pygame.font.SysFont('Bauhaus 93 Regular', 40)


while True: # Main loop
    for event in pygame.event.get():
        if event.type is QUIT:
            pygame.quit()
            sys.exit()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if mode == 'main': # Code for the main menu. 
            DISPLAYSURF.blit(getMenuAsset('main_menu_screen'), (0, 0))
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
                    mode = 'playing'
                if selected is 2:
                    mode = 'load'
                if selected is 3:
                    mode = 'options'
                if selected is 4:
                    pygame.quit()
                    sys.exit()
            if event.type is KEYDOWN and (event.key == K_DOWN or event.key == K_RIGHT):
                selected = selected + 1
            if event.type is KEYDOWN and (event.key == K_UP or event.key == K_LEFT):
                selected = selected - 1
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if mode == 'load':
            DISPLAYSURF.blit(getMenuAsset('main_menu_screen'), (0, 0))
            game.setGamestate(json.loads(open('../data/save/save.json','r').read()))
            mode = 'playing'
            paused = False
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if mode == 'save':
            DISPLAYSURF.blit(getMenuAsset('main_menu_screen'), (0, 0))
            open('../data/save/save.json','w').truncate()
            open('../data/save/save.json','w').write(json.dumps(game.getGamestate()))
            if paused:
                mode = 'paused'
            else:
                mode = 'main'
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if mode == 'options':
            temp_counter = 0
            options_list = []
            DISPLAYSURF.blit(getMenuAsset('options_menu_screen'), (0, 0))
            for keybind in options['keybinds']:
                options_list.append([keybind, options['keybinds'][keybind]])
                temp_counter += 1
                DISPLAYSURF.blit(FONT.render(keybind, False, (0,0,0) ), (25,25*(temp_counter+1)) )
                DISPLAYSURF.blit(FONT.render(options_list[temp_counter - 1][1], False, (0,0,0) ), (500,25*(temp_counter+1)) )
            if event.type is KEYDOWN and event.key == K_ESCAPE:
                if paused:
                    mode = 'paused'
                else:
                    mode = 'main'
            if event.type is KEYDOWN and event.key == K_DOWN:
                selected = selected + 1
            if event.type is KEYDOWN and event.key == K_UP:
                selected = selected - 1
            if selected is 0:
                selected = len(options_list)
            if selected is len(options_list) + 1:
                selected = 1
            DISPLAYSURF.blit(FONT.render(options_list[selected-1][0], False, (0,0,255) ), (25,25*(selected+1)) )
            DISPLAYSURF.blit(FONT.render(options_list[selected-1][1], False, (0,0,255) ), (500,25*(selected+1)) )
            if event.type is KEYDOWN and event.key == K_RIGHT:
                DISPLAYSURF.blit(FONT.render(options_list[selected-1][0], False, (255,0,0) ), (25,25*(selected+1)) )
                DISPLAYSURF.blit(FONT.render(options_list[selected-1][1], False, (255,0,0) ), (500,25*(selected+1)) )
                pygame.display.update()
                recording = True
                while recording:
                    for event in pygame.event.get():
                        if event.type is KEYDOWN:
                            options_list[selected-1][1] = pygame.key.name(event.key)
                            recording = False
                for pair in options_list:
                    options['keybinds'][pair[0]] = pair[1]
                open('../data/options.json','w').write(json.dumps(options))
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if mode == 'paused':
            paused = True
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
                    mode = 'playing'
                    paused = False
                if selected is 2:
                    mode = 'save'
                if selected is 3:
                    mode = 'load'
                if selected is 4:
                    mode = 'options'
                if selected is 5:
                    pygame.quit()
                    sys.exit()
            if event.type is KEYDOWN and (event.key == K_DOWN or event.key == K_RIGHT):
                selected = selected + 1
            if event.type is KEYDOWN and (event.key == K_UP or event.key == K_LEFT):
                selected = selected - 1
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if mode == 'playing':
            selected = 1
            DISPLAYSURF.blit(getMenuAsset('main_menu_screen'), (0, 0))
            gamemsg = game.start()
            if gamemsg is 'PAUSE':
                mode = 'paused'
            elif gamemsg is 'DIE':
                mode = 'gameover'
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if mode == 'gameover':
            DISPLAYSURF.blit(getMenuAsset('main_menu_screen'), (0, 0))
            DISPLAYSURF.blit(getMenuAsset('game_over_screen'), (0,0))
            if event.type is KEYDOWN and event.key is K_RETURN:
                if selected is 1:
                    mode = 'main'
                if selected is 2:
                    pygame.quit()
                    sys.exit()
            if event.type is KEYDOWN and (event.key == K_DOWN or event.key == K_RIGHT):
                selected = selected + 1
            if event.type is KEYDOWN and (event.key == K_UP or event.key == K_LEFT):
                selected = selected - 1
            if selected is 3:
                selected = 1
            if selected is 0:
                selected = 2
            if selected is 1:
                DISPLAYSURF.blit(getMenuAsset('game_over_screen_selected_yes'), (0, 0))
            if selected is 2:
                DISPLAYSURF.blit(getMenuAsset('game_over_screen_selected_no'), (0, 0))   
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        pygame.display.update()
#            somebody once told me the world was macoroni
#            so i took a bite out of a tree
#            it tasted pretty funny
#            so i spit it at a bunny
            
            
