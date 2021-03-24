######################################
# Shane Donivan
# PM Class
# Junior
# 3/10/21
# Assignment 036, Pygame Platformer
# A simple game involving a player
# and 3 enemies...
#######################################


import pygame
import random
import sys
import os

from pygame.locals import(
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    KEYUP,
    QUIT
)

class Player(pygame.sprite.Sprite):
    walkingRight = ['assets/playerR/Run.png','assets/playerR/Run_2.png','assets/playerR/Run_3.png','assets/playerR/Run_4.png',
                    'assets/playerR/Run_5.png','assets/playerR/Run_6.png','assets/playerR/Run_7.png',
                    'assets/playerR/Run_8.png','assets/playerR/Run_9.png','assets/playerR/Run_10.png','assets/playerR/Run_11.png']

    walkingLeft = ['assets/playerL/Run.png','assets/playerL/Run_2.png','assets/playerL/Run_3.png','assets/playerL/Run_4.png',
                    'assets/playerL/Run_5.png','assets/playerL/Run_6.png','assets/playerL/Run_7.png',
                    'assets/playerL/Run_8.png','assets/playerL/Run_9.png','assets/playerL/Run_10.png','assets/playerL/Run_11.png']
    def __init__(self):
        super(Player,self).__init__()
        self.isWalking = True
        self.isRunning = False
        self.isShooting = False
        self.walkCount = 0
        self.runCount = 0
        self.facing = 'right'
        self.surf = pygame.image.load(self.walkingRight[self.walkCount]).convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.x = 0
        self.rect.y = 720
        self.Etype = 'Player'

    def update(self,pressed_keys):
        if pressed_keys[K_LEFT]:
            self.facing = 'left'
            self.walking = True
            if self.walkCount >= len(self.walkingLeft)-1:
                self.walkCount = 0
            self.surf = pygame.image.load(self.walkingLeft[self.walkCount]).convert()
            self.surf.set_colorkey((0,0,0), RLEACCEL)
            self.rect.x -= 1
            self.walkCount += 1

        if pressed_keys[K_RIGHT]:
            self.facing = 'right'
            self.walking = True
            if self.walkCount >= len(self.walkingRight)-1:
                self.walkCount = 0
            self.surf = pygame.image.load(self.walkingLeft[self.walkCount]).convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            self.rect.x += 1
            self.walkCount += 1

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class enemy(pygame.sprite.Sprite):
    animationCount = 0
    isWalking = 0
    isAttacking = 0
    def __init__(self):
        super(enemy, self).__init__()
        self.surf = pygame.image.load('assets/enemies/slime/slime.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),700))
        self.speed = random.randint(2, 5)

    def update(self):
        walkAnimation = ['assets/enemies/slime/slime.png']

        if self.animationCount > len(walkAnimation) - 1:
            self.animationCount = 0
        self.surf = pygame.image.load(walkAnimation[self.animationCount]).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self. animationCount -= 1
        self.rect.move_ip(-1, 0)
        if self.rect.right < 0:
            self.kill()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 4000)

player = Player()

#All Sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
enemies = pygame.sprite.Group()
ground = pygame.sprite.Group()


running = True
background = ['assets/back.png']
currentBg = 0
bkgd = pygame.image.load(background[currentBg])
bg1 = pygame.image.load('assets/back.png').convert()
bg2 = pygame.image.load('assets/back.png').convert()
bg1x = 0
bg2x = bg1.get_width()
x = 0
fps = 60
isWalking = False

# Main Game
while running:
    for event in pygame.event.get():
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                isWalking = False
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                isWalking = True
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    bg1x -= 1
    bg2x -= 1

    if bg1x < bg1.get_width() * -1:
        bg1x = bg2.get_width()
    if bg2x < bg2.get_width() * -1:
        bg2x = bg1.get_width()


    screen.blit(bg1, (bg1x, 0))
    screen.blit(bg2, (bg2x, 0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    pygame.display.update()
    clock.tick(fps)

