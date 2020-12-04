import pygame as pg
from pygame.locals import *
import sys,Colors
def start_screen(DS,FPS_Clock,FPS,win_lose=''):
    size=DS.get_size()
    fontObj=pg.font.Font('freesansbold.ttf',32)
    if win_lose=='WIN':
        TextSurfObj_2=fontObj.render('WIN!',True,Colors.colors['GREEN'])
    elif win_lose=='LOSE':
        TextSurfObj_2=fontObj.render('Game Over!',True,Colors.colors['RED'])

    TextSurfObj=fontObj.render('Click here to (re)start',True,Colors.colors['BLACK'])
    Textrec=TextSurfObj.get_rect()
    if win_lose!='':
        Textrec_2=TextSurfObj_2.get_rect()
        Textrec_2.centerx=size[0]//2
        Textrec_2.centery=size[1]//2-Textrec.height
    Textrec.centerx=size[0]//2
    Textrec.centery=size[1]//2
    click_start=False
    while not click_start:
        

        DS.fill(Colors.colors['WHITE'])
        DS.blit(TextSurfObj,Textrec)
        if win_lose!='':
            DS.blit(TextSurfObj_2,Textrec_2)
        for event in pg.event.get():
            if event.type==QUIT:
                pg.quit()
                sys.exit(0)
            elif event.type==MOUSEBUTTONUP:
                if Textrec.collidepoint(event.pos):
                    click_start=True
        pg.display.update()
        FPS_Clock.tick(FPS)