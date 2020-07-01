"""
a side scrolling runner game using Python
a project created summer of 2020

@author ashley hui
@art ashley hui
@music james hammond @ http://jameshammondrf.bandcamp.com
"""

import pygame as pg
from pygame import mixer
import random

# initialize pygame
pg.init()

# create the screen
height = 600
width = 800
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock()     #use to increase speed of FPS
score = 0
BASICFONT = pg.font.Font('8bitpusab.ttf', 21)
FPS = 2

# music
mixer.music.load("/sounds/bg.mp3")
mixer.music.play(-1)


# title and icon
pg.display.set_caption('star dasher')
icon = pg.image.load('/images/logo.png')
pg.display.set_icon(icon)

# game background scroll

bg = pg.image.load('/images/bg/background1.png')
bg2 = pg.image.load('/images/bg/background2.png')
bgX = 0
bgX2 = bg.get_width()


def pressKeyMsg(count):
    pressKeyText1 = BASICFONT.render('Press any key to play', True, (255, 217, 0))
    pressKeyText2 = BASICFONT.render('Press any key to play', True, (255, 255, 255))
    pressKeyRect = pressKeyText1.get_rect()
    pressKeyRect.center = (round(width/2), round(height/2 + 260))

    text = [pressKeyText1, pressKeyText2]

    if count%2 == 0:
        screen.blit(text[0], pressKeyRect)
    else:
        screen.blit(text[1], pressKeyRect)

    pg.display.update()
    clock.tick(FPS)


def checkForKeyPress():
    if len(pg.event.get(pg.QUIT)) > 0:
        pg.quit()
    keyUpEvents = pg.event.get(pg.KEYUP)
    if len(keyUpEvents) == 0:
        run = False
        return None
    if keyUpEvents[0].key == pg.K_ESCAPE:
        pg.quit()
    return keyUpEvents[0].key


def showStart():
    startScreen = pg.image.load('/images/bg/startscreen.png')
    titleFont = pg.font.Font('8bitpusab.ttf', 55)

    title1 = titleFont.render('STAR DASHER', True, (116, 60, 89))

    titleRect1 = title1.get_rect()
    titleRect1.center = (round(width/2), round(height/2 + 130))

    colorCount = 0


    while True:
        colorCount += 1

        screen.blit(startScreen, (0,0))
        screen.blit(title1, titleRect1)

        pressKeyMsg(colorCount)

        if checkForKeyPress():
            pg.event.get()
            return
        pg.display.update()

def showEnd():
    end = True
    while end:
        endScreen = pg.image.load('/images/bg/endscreen.png')
        titleFont = pg.font.Font('8bitpusab.ttf', 55)

        title1 = titleFont.render('GAME OVER', True, (116, 60, 89))

        titleRect1 = title1.get_rect()
        titleRect1.center = (round(width/2), round(height/2 + 130))

        colorCount = 0

        while True:
            colorCount += 1

            screen.blit(endScreen, (0,0))
            screen.blit(title1, titleRect1)

            pressKeyMsg(colorCount)

            if checkForKeyPress():
                pg.event.get()
                end = False
                return
            pg.display.update()

def draw():
    screen.blit(bg, (round(bgX), 0))
    screen.blit(bg2, (round(bgX2), 0))
    girl.draw(screen)
    for object in objects:
        object.draw(screen)
    pg.display.update()

# character
class Girl(object):
    girl = pg.image.load('/images/character/run1.png')

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.falling = False
        self.lost = False
        self.runCount = 0

    def draw(self, screen):
        if self.jumping:
            self.y -= 3.5
            screen.blit(self.girl, (round(self.x), round(self.y)))
            if self.y < 100:    # if cat passes max height
                self.falling = True
                self.jumping = False
            self.hitbox = (self.x + 30, self.y, self.width - 50, self.height - 40)
        if self.falling:
            self.y += 4
            screen.blit(self.girl, (round(self.x), round(self.y)))
            if self.y > ground:
                self.falling = False
            self.hitbox = (self.x + 30, self.y, self.width - 50, self.height - 80)
        elif self.lost:
            screen.blit(self.girl, (round(self.x), round(self.y + 30)))
        else:
            screen.blit(self.girl, (round(self.x), round(self.y)))
            self.hitbox = (self.x + 30, self.y, self.width - 50, self.height - 30)
        # pg.draw.rect(screen, (255,0,0), self.hitbox, 1)

# ground obstacle

class groundObj(object):
    groundStar = pg.image.load('/images/objects/groundObj.png')

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)

    def draw(self, screen):
        self.hitbox = (self.x + 35, self.y + 20, self.width - 50, self.height - 30)
        screen.blit(self.groundStar, (round(self.x), round(self.y)))
        # pg.draw.rect(screen, (255, 0, 0), self.hitbox, 1)

    def collide(self, hit):
        if hit[0] + hit[2] > self.hitbox[0] and hit[0] < self.hitbox[0] + self.hitbox[2]:
            if hit[1] + hit[3] > self.hitbox[1]:
                return True
            return False



# loop to keep game running
gameRunning = True
pg.time.set_timer(pg.USEREVENT+2, 3000)
ground = 330.00
girl = Girl(100.00, ground, 120, 140)
objects = []
showStart()


while gameRunning:
    draw()
    bgX -= 1.4
    bgX2 -= 1.4

    if bgX < bg.get_width () * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    for object in objects:
        if object.collide(girl.hitbox):
            girl.lost = True
            showEnd()
        object.x -= 1.4
        if object.x < object.width * -1:    # remove object if off screen
            objects.remove(object)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameRunning = False
        if event.type == pg.USEREVENT+2:
            r = random.randrange(0,2)
            if r == 0:
                objects.append(groundObj(810, 390, 110, 70))

    key = pg.key.get_pressed()

    if key[pg.K_UP]:
        if not girl.jumping and not girl.falling:
            girl.jumping = True
        # if event.key == pg.K_DOWN:
        #     self.y += 0.2
    # if event.type == pg.KEYUP:
    #     if event.key == pg.K_DOWN or event.key == pg.K_UP:
    #         print("button released")

    pg.display.update()