#-*-coding:utf-8-*-
# 赢时的图像

import pygame
from pygame.locals import *
from sys import exit
import sys

mainPath=sys.path[0]

class Win(object):
    def __init__(self,surface):
        self.surface=surface
        pygame.image.save(self.surface,mainPath+'/images/win.png')# 存储背景图片
        self.background_image=pygame.image.load(mainPath+'/images/win.png').convert()
        self.backcolor=(174,181,254)
        self.wincolor=(255,127,0)
        self.answercolor=(127,0,255)
        self.w,self.h=self.surface.get_size()
        self.font=pygame.font.Font(mainPath+'/fonts/comic.ttf',30)

    def get_win(self):
        self.surface.blit(self.background_image,(0,0))
        vect=(self.w/2.0-150,self.h/2.0-80)
        w=300
        h=160
        pygame.draw.rect(self.surface,self.backcolor,Rect(vect,(w,h)))
        win=self.font.render('Vectory!',True,self.wincolor)
        answer=self.font.render(' Exit   Go on ',True,self.answercolor)
        ww,wh=win.get_size()
        aw,ah=answer.get_size()
        wv=(vect[0]+w/2.0-ww/2.0,vect[1]+10)
        av=(vect[0]+w/2.0-aw/2.0,vect[1]+20+wh)
        self.surface.blit(win,wv)
        self.surface.blit(answer,av)
        pygame.image.save(self.surface,mainPath+'/images/win_game.png')
        win_image=pygame.image.load(mainPath+'/images/win_game.png').convert()

        pygame.mouse.set_visible(True)# 鼠标可见
        while True:
            self.surface.blit(win_image,(0,0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type==QUIT:
                    exit()
                elif event.type==KEYDOWN:
                        if event.key==K_ESCAPE:
                            exit()
                elif event.type==MOUSEBUTTONDOWN:
                    mx,my=pygame.mouse.get_pos()
                    if mx>=av[0] and mx<=av[0]+aw/2.0 and my>=av[1] and my<=av[1]+ah:
                        exit()
                    elif mx>av[0]+aw/2.0 and mx<=av[0]+aw and my>=av[1] and my<=av[1]+ah:
                        return True
