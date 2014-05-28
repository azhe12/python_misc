#!/usr/bin/python
#coding=utf-8
import sys, pygame
from pygame.locals import *
from random import randrange

if __name__ == '__main__':
    print '__name__ = ', __name__

class Bomb(pygame.sprite.Sprite):
    def __init__(self, image, screen_size):
        #init sprite
        #print 'init bomb'
        pygame.sprite.Sprite.__init__(self)
        #init image, rectangle
        self.image = image
        self.rect = self.image.get_rect()
        self.screen_size = screen_size
        self.reset()
    
    def reset(self):
        """
        将炸弹放到屏幕顶端的随机位置
        """
        self.rect.top = -self.rect.height
        self.rect.centerx = randrange(self.screen_size[0])
    def update(self):
        """
        显示下一帧, 炸弹下降
        """
        self.rect.top += 1
        if self.rect.top > self.screen_size[1]:
            self.reset()

def main():
    #素材的名字
    filename={}
    filename['bomb'] = 'bomb.png'
    
    #init
    print 'init pygame'
    pygame.init()
    screen_size = 800,600
    #pygame.display.set_mode(screen_size, FULLSCREEN)
    #必须设置 set_mode
    pygame.display.set_mode(screen_size)
    pygame.mouse.set_visible(0)
    
    #load bomb image
    bomb_image = pygame.image.load(filename['bomb'])
    bomb_image = bomb_image.convert()
    
    #create a sprite group
    sprites  = pygame.sprite.RenderUpdates()
    sprites.add(Bomb(bomb_image, screen_size))
    
    #get screen and fill it
    screen = pygame.display.get_surface()
    bg = (255, 255, 255) #white
    screen.fill(bg)
    pygame.display.flip()
    
    print 'finish flip'
    #clear child graphic
    def clear_callback(surf, rect):
        surf.fill(bg, rect)
    
    while True:
        #检查退出事件
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN and event.type == K_ESCAPE:
                sys.exit()
    
	    #清除前面的位置
	    sprites.clear(screen, clear_callback)
	    #更新所有子图形
	    sprites.update()
	    #绘制所有子图形
	    updates = sprites.draw(screen)
	    #更新所需显示的部分
	    pygame.display.update(updates)


#如果作为module导入的话，不运行
if __name__ == '__main__':main()
