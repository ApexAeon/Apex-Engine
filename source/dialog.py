import pygame, sys
from pygame.locals import *
pygame.font.init()
FONT = pygame.font.SysFont('Calibri', 18)
class Box():
    def __init__(self, content='', border_width=1, border_color=(255,255,255), background_color=(0,0,255),width=200,height=50):
        self.content=content
        self.border_width=border_width
        self.border_color=border_color
        self.width=width
        self.height=height
        self.background_color=background_color
    def render(self):
        self.image=pygame.Surface((self.width,self.height))
        self.image.fill(self.border_color)
        self.image.fill(self.background_color,pygame.Rect((self.border_width,self.border_width),(self.width-self.border_width*2,self.height-self.border_width*2)))
        self.image.blit(FONT.render(self.content, False, self.border_color),(self.border_width+5,self.border_width+5))
        return self.image
    def setContent(self, stuff):
        self.content = stuff
    def addContent(self, stuff):
        self.content += stuff
