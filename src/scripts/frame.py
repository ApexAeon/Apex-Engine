import pygame, sys
from pygame.locals import *
import json
from enum import Enum
import game
from common import DISPLAYSURF
from common import FONT

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

consolelog = []
consolelines = 1
drawn = False
paused = False

def writescreen(strin, pos):
    DISPLAYSURF.blit(FONT.render(strin, True, (0, 128, 255)), pos)

def writeconsole(strin):
    consolelog.append(strin)
    if gamestate is GameState.console:
        writescreen(strin, (0, consolelines * 25))
        consolelines += 1

gamemode = GameMode.mainmenu



selected = 1


gameinfo = open('..\\data\\gameinfo.json','r') # Load the gameinfo file
parsed = json.loads(gameinfo.read()) # Parse gaminfo's JSON into a dictionary

cover = pygame.image.load(parsed['cover'])
icon = pygame.image.load(parsed['icon'])
pausebutton = pygame.image.load(parsed['pause'])
gameoverscreen = pygame.image.load(parsed['gameover'])
    
pygame.init()
DISPLAYSURF = pygame.display.set_mode((828, 640))
pygame.display.set_caption(parsed['name'])
pygame.display.set_icon(icon)
FONT = pygame.font.SysFont('Bauhaus 93 Regular', 40)

while True: # Main loop

    for event in pygame.event.get():

        if event.type is QUIT:
            pygame.quit()
            sys.exit()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if gamemode is GameMode.mainmenu: # Code for the main menu. 

            DISPLAYSURF.blit(cover, (0, 0))
            writescreen('New Game',(25,25))
            writescreen('Load',(25,50))
            writescreen('Options',(25,75))
            writescreen('Quit',(25,100))

            if selected is 5:
                selected = 1
            if selected is 0:
                selected = 4

            if selected is 1:
                DISPLAYSURF.blit(FONT.render('New Game',    True, (255, 140, 0)), (25, 25))
            if selected is 2:
                DISPLAYSURF.blit(FONT.render('Load',        True, (255, 140, 0)), (25, 50))
            if selected is 3:
                DISPLAYSURF.blit(FONT.render('Options',     True, (255, 140, 0)), (25, 75))
            if selected is 4:
                DISPLAYSURF.blit(FONT.render('Quit',        True, (255, 140, 0)), (25, 100))

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
                    
            if event.type is KEYDOWN and event.key is K_s:
                selected = selected + 1
            if event.type is KEYDOWN and event.key is K_w:
                selected = selected - 1
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if gamemode is GameMode.load:
            DISPLAYSURF.blit(cover, (0, 0))
            game.setGamestate(json.loads(open('../data/save/save.json','r').read()))
            gamemode = GameMode.playing
            paused = False
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if gamemode is GameMode.save:
            DISPLAYSURF.blit(cover, (0, 0))
            open('../data/save/save.json','w').truncate()
            open('../data/save/save.json','w').write(json.dumps(game.getGamestate()))
            if paused:
                gamemode = GameMode.paused
            else:
                gamemode = GameMode.mainmenu
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if gamemode is GameMode.options:
            DISPLAYSURF.blit(cover, (0, 0))
            writescreen( 'Options are currently not available. Please exit the program XD.' , (25,25) )
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if gamemode is GameMode.console:
            DISPLAYSURF.blit(cover, (0, 0))

            # --STUB-- The console will be implemented in other classes
            # It will be a combination of some simple commands, and also
            # a FORTH interpreter.
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if gamemode is GameMode.paused:
            paused = True
            DISPLAYSURF.blit(cover, (0, 0))
            DISPLAYSURF.blit(pausebutton, (25,25))
            writescreen('Resume',(25,50))
            writescreen('Save',(25,75))
            writescreen('Load',(25,100))
            writescreen('Options',(25,125))
            writescreen('Quit',(25,150))

            if selected is 6:
                selected = 1
            if selected is 0:
                selected = 5
                
            if selected is 1:
                DISPLAYSURF.blit(FONT.render('Resume',    True, (255, 140, 0)), (25, 50))
            if selected is 2:
                DISPLAYSURF.blit(FONT.render('Save',        True, (255, 140, 0)), (25, 75))
            if selected is 3:
                DISPLAYSURF.blit(FONT.render('Load',     True, (255, 140, 0)), (25, 100))
            if selected is 4:
                DISPLAYSURF.blit(FONT.render('Options',        True, (255, 140, 0)), (25, 125))
            if selected is 5:
                DISPLAYSURF.blit(FONT.render('Quit',        True, (255, 140, 0)), (25, 150))

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

            if event.type is KEYDOWN and event.key is K_s:
                selected = selected + 1
            if event.type is KEYDOWN and event.key is K_w:
                selected = selected - 1
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if gamemode is GameMode.error:
            DISPLAYSURF.blit(cover, (0, 0))

            # --STUB-- If a fatal error occurs, this will be like the
            # blue screen of death or something, telling you what's up,
            # throwing some error codes and dumping it to a file & etc.
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if gamemode is GameMode.playing:
            gamemsg = game.start()
            if gamemsg is 'PAUSE':
                gamemode = GameMode.paused
            elif gamemsg is 'DIE':
                gamemode = GameMode.gameover
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if gamemode is GameMode.gameover:
            DISPLAYSURF.blit(gameoverscreen, (0,0))
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
            
            
