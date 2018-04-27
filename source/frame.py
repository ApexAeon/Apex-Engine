import game, dialog, json, pygame, sys, common
from common import *
from pygame.locals import *
from resources import *
paused = False
mode = 'main'
selected = 1
options = resources.loadData('options')

while True: # Main loop
    for event in pygame.event.get():
        if event.type is QUIT:
            pygame.quit()
            sys.exit()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if mode == 'main': # Code for the main menu. 
            DISPLAYSURF.blit(getAsset('main_menu_screen', assets), (0, 0))
            if selected is 5:
                selected = 1
            if selected is 0:
                selected = 4
            if selected is 1:
                DISPLAYSURF.blit(getAsset('main_menu_selected_play', assets), (0, 0))
            if selected is 2:
                DISPLAYSURF.blit(getAsset('main_menu_selected_load', assets), (0, 0))
            if selected is 3:
                DISPLAYSURF.blit(getAsset('main_menu_selected_options', assets), (0, 0))
            if selected is 4:
                DISPLAYSURF.blit(getAsset('main_menu_selected_quit', assets), (0, 0))
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
            DISPLAYSURF.blit(getAsset('main_menu_screen', assets), (0, 0))
            game.setGamestate(json.loads(open('../data/save/save.json','r').read()))
            mode = 'playing'
            paused = False
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if mode == 'save':
            DISPLAYSURF.blit(getAsset('main_menu_screen', assets), (0, 0))
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
            DISPLAYSURF.blit(getAsset('main_menu_screen', assets), (0, 0))
            DISPLAYSURF.blit(getAsset('options_menu_screen', assets), (0, 0))
            for keybind in options['keybinds']:
                options_list.append([keybind, options['keybinds'][keybind]])
                temp_counter += 1
                DISPLAYSURF.blit(FONT.render(keybind, False, (0,0,0) ), (25,25*(temp_counter+1)) )
                DISPLAYSURF.blit(FONT.render(options_list[temp_counter - 1][1], False, (0,0,0) ), (200,25*(temp_counter+1)) )
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
            DISPLAYSURF.blit(FONT.render(options_list[selected-1][1], False, (0,0,255) ), (200,25*(selected+1)) )
            if event.type is KEYDOWN and event.key == K_RIGHT:
                DISPLAYSURF.blit(FONT.render(options_list[selected-1][0], False, (255,0,0) ), (25,25*(selected+1)) )
                DISPLAYSURF.blit(FONT.render(options_list[selected-1][1], False, (255,0,0) ), (200,25*(selected+1)) )
                common.scale()
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
            DISPLAYSURF.blit(getAsset('main_menu_screen', assets), (0, 0))
            DISPLAYSURF.blit(getAsset('pause_menu_screen', assets), (0,0))
            if selected is 6:
                selected = 1
            if selected is 0:
                selected = 5
            if selected is 1:
                DISPLAYSURF.blit(getAsset('pause_menu_selected_resume', assets), (0, 0))
            if selected is 2:
                DISPLAYSURF.blit(getAsset('pause_menu_selected_save', assets), (0, 0))
            if selected is 3:
                DISPLAYSURF.blit(getAsset('pause_menu_selected_load', assets), (0, 0))
            if selected is 4:
                DISPLAYSURF.blit(getAsset('pause_menu_selected_options', assets), (0, 0))
            if selected is 5:
                DISPLAYSURF.blit(getAsset('pause_menu_selected_quit', assets), (0, 0))
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
            DISPLAYSURF.blit(getAsset('main_menu_screen', assets), (0, 0))
            gamemsg = game.start()
            if gamemsg is 'PAUSE':
                mode = 'paused'
            elif gamemsg is 'DIE':
                mode = 'gameover'
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if mode == 'gameover':
            DISPLAYSURF.blit(getAsset('main_menu_screen', assets), (0, 0))
            DISPLAYSURF.blit(getAsset('game_over_screen', assets), (0,0))
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
                DISPLAYSURF.blit(getAsset('game_over_screen_selected_yes', assets), (0, 0))
            if selected is 2:
                DISPLAYSURF.blit(getAsset('game_over_screen_selected_no', assets), (0, 0))   
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        common.scale()
        pygame.display.update()
#            somebody once told me the world was macoroni
#            so i took a bite out of a tree
#            it tasted pretty funny
#            so i spit it at a bunny
            
            
