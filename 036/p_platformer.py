######################################
# Shane Donivan
# PM Class
# Junior
# 3/10/21
# Assignment 036, Pygame Platformer
# 1 player 1 enemy and a Score with a
# mini-menu for deaths.
#######################################


import pygame, random, sys
import PySimpleGUI as sg
from pygame.locals import *

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

#This is the player class, super buggy and he can only go right
class Player(pygame.sprite.Sprite):
    walkingRight = ['assets/frames/pewman_000.png','assets/frames/pewman_000.png','assets/frames/pewman_001.png','assets/frames/pewman_001.png',
                    'assets/frames/pewman_002.png','assets/frames/pewman_002.png','assets/frames/pewman_003.png','assets/frames/pewman_003.png',
                    'assets/frames/pewman_004.png','assets/frames/pewman_005.png','assets/frames/pewman_006.png','assets/frames/pewman_006.png',
                    'assets/frames/pewman_007.png','assets/frames/pewman_007.png','assets/frames/pewman_008.png','assets/frames/pewman_008.png',
                    'assets/frames/pewman_009.png','assets/frames/pewman_009.png','assets/frames/pewman_010.png','assets/frames/pewman_010.png',
                    'assets/frames/pewman_011.png','assets/frames/pewman_011.png','assets/frames/pewman_012.png','assets/frames/pewman_012.png',
                    'assets/frames/pewman_013.png','assets/frames/pewman_013.png','assets/frames/pewman_014.png','assets/frames/pewman_014.png']


    def __init__(self):
        super(Player,self).__init__()
        self.dead = False
        self.isWalking = True
        self.isShooting = False
        self.isJumping = False
        self.walkCount = 0
        self.jumpCount = 15
        self.facing = 'right'
        self.surf = pygame.image.load(self.walkingRight[self.walkCount])
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.x = 0
        self.rect.y = 430
        self.Etype = 'Player'

    def update(self,pressed_keys,running):
        if pressed_keys[K_RIGHT]:
            self.facing = 'right'
            self.walking = True
            if self.walkCount >= len(self.walkingRight)-1:
                self.walkCount = 0
            self.surf = pygame.image.load(self.walkingRight[self.walkCount])
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            self.rect.x += 5
            self.walkCount += 1

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        if self.dead == True:
            running = False
        if pressed_keys[K_RETURN]:
            self.isShooting = True

    def setstate(self, state, value):
        if state == 'jumping':
            self.isJumping = value

    def jump(self):
        if self.isJumping:
            if self.jumpCount >= -15:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.rect.y -= self.jumpCount ** 2 * 0.25 * neg
                if self.facing == 'right':
                    self.rect.x += 3
                else:
                    self.rect.x -= 3
                self.jumpCount -= 1
            else:
                self.isJumping = False
                self.jumpCount = 15
                self.rect.y = 750

#This button is so customizable, next I'm making it let me use images. Easily the best thing I made out of this program.
class button():
    def __init__(self, color, x, y, width, height, text='', font = '',size = 60):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.size = size

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont(self.font,self.size)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

#Slime is the most functional thing in the program, it moves and exists
class slime(pygame.sprite.Sprite):
    movement = ['assets/frames/techslime1.png','assets/frames/techslime2.png','assets/frames/techslime3.png','assets/frames/techslime4.png']
    animationCount = 0
    isWalking = 0
    isAttacking = 0
    rChoice = 0
    def __init__(self):
        super(slime, self).__init__()
        self.surf = pygame.image.load(self.movement[self.animationCount])
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), 650))
        self.speed = random.randint(4, 5)
        self.type = 'low-tier'
        self.collide = False


    def update(self):
        if self.rChoice == 6:
            self.surf = pygame.image.load(self.movement[self.animationCount])
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            self.animationCount += 1
            if self.animationCount > len(self.movement) - 1:
                self.animationCount = 0
            self.rChoice = 0
        else:
            self.rChoice += 1
        self.surf = pygame.image.load(self.movement[self.animationCount])
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect.move_ip(self.speed * -1, 0)
        if self.rect.right < 0:
            self.kill()


#Coins. Self explanatory and Mario wants to collect as many as he can
class coin(pygame.sprite.Sprite):
    animationCount = 0
    isWalking = 0
    isAttacking = 0
    def __init__(self):
        super(coin, self).__init__()
        self.surf = pygame.image.load('assets/coin2.png')
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), 600))
        self.speed = random.randint(2, 5)
        self.type = 'coin'

    def update(self):
        movement = ['assets/coin2.png']
        rChoice = random.randint(1, 1000) % 100
        if rChoice == 0:
            self.surf = pygame.image.load(movement[self.animationCount])
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            self.animationCount += 1
            if self.animationCount > len(movement) - 1:
                self.animationCount = 0
        self.surf = pygame.image.load(movement[self.animationCount])
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect.move_ip(self.speed * -1, 0)
        if self.rect.right < 0:
            self.kill()

#Function for the game because it's pretty neat
def game():
    global Score
    green = (0, 80, 0)
    myFont = pygame.font.SysFont("Comicsans", 40)
    Score_Label = myFont.render("Score: ", 1, green)
    Score_Value = myFont.render(str(Score), 1, green)
    myEndFont = pygame.font.SysFont("Comicsans", 80)
    End_Label = myEndFont.render("Game Over!!!", 1, green)

    background = ['assets/back.png']
    currentBg = 0
    bkgd = pygame.image.load(background[currentBg])
    bg1 = pygame.image.load('assets/back.png').convert()
    bg2 = pygame.image.load('assets/back.png').convert()
    bg1x = 0
    bg2x = bg1.get_width()
    x = 0
    fps = 30
    isWalking = False
    enemyList = ['slime', 'coin']
    global running
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    isWalking = False

            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    isWalking = True
                if event.key == K_UP:
                    player.setstate('jumping', True)

                if event.key == K_SPACE:
                    new_blast = blast()
                    blasts.add(new_blast)
                    all_sprites.add(new_blast)

            elif event.type == QUIT:
                running = False

            elif event.type == ADDENEMY:
                enemyType = random.choice(enemyList)
                if enemyType == 'slime':
                    print('slime')
                    new_enemy = slime()
                if enemyType == 'mushroom':
                    print('mushroom')
                    new_enemy = mushroom()
                if enemyType == 'potato':
                    print('potato')
                    new_enemy = potato()
                if enemyType == 'coin':
                    print('coin')
                    new_enemy = coin()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys,running)
        enemies.update()
        player.jump()

        enemyHits = pygame.sprite.spritecollideany(player, enemies)
        if enemyHits != None:
            print(f"Enemy Hits {enemyHits.type}")
            if enemyHits.type == 'low-tier':
                endgame()

            elif enemyHits.type == 'mid-tier':
                endgame()

            elif enemyHits.type == 'high-tier':
                endgame()

            elif enemyHits.type == 'coin':
                enemyHits.kill()
                Score += 5


        bg1x -= 1
        bg2x -= 1

        if bg1x < bg1.get_width() * -1:
            bg1x = bg2.get_width()
        if bg2x < bg2.get_width() * -1:
            bg2x = bg1.get_width()


        screen.blit(bg1, (bg1x, 0))
        screen.blit(bg2, (bg2x, 0))
        Score_Value = myFont.render(str(Score), 1, green)
        screen.blit(Score_Label, (SCREEN_WIDTH - 250, 2))
        screen.blit(Score_Value, (SCREEN_WIDTH - 60, 2))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        pygame.display.update()
        clock.tick(fps)

#It resets the players position and kills the enemy who dare touch thee
def endgame():
    global running
    enemyHits = pygame.sprite.spritecollideany(player, enemies)
    #die animation
    running = False
    enemyHits.kill()
    player.rect.x = 0
    playagain()

#Creates a Mini-Menu saying you died
def playagain():
    while True:
        background = button((70, 171, 97), 430, 50, 440, 500)
        background.draw(screen)
        title = button((70, 171, 97), 540, 110, 220, 10, 'You Died!','',90)
        title.draw(screen)

        button_1 = button((0,255,0), 540, 250, 220, 100, 'Try Again')
        button_2 = button((0,255,0), 540, 400, 220, 100, 'Quit')
        button_1.draw(screen)
        button_2.draw(screen)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.isOver(pos):
                    game()
                if background.isOver(pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if button_1.isOver(pos):
                    button_1.color=(200,0,0)
                else:
                    button_1.color=(0,255,0)

        pygame.display.update()
        clock.tick(60)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Initialize pygame
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
file = 'some.mp3'

#Global values are amazing.
global Score
Score = 0

#Custom event for enemy spawn and creating the player
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 4000)

player = Player()

#All Sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

enemies = pygame.sprite.Group()
ground = pygame.sprite.Group()

#I ran the game function
game()