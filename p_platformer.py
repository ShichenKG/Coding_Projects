######################################
# Shane Donivan
# PM Class
# Junior
# 3/10/21
# Assignment 036, Pygame Platformer
# A simple game involving a player
# and 3 enemies...
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

class Player(pygame.sprite.Sprite):
    walkingRight = ['assets/playerR/Run.png','assets/playerR/Run_2.png','assets/playerR/Run_3.png','assets/playerR/Run_4.png',
                    'assets/playerR/Run_5.png','assets/playerR/Run_6.png','assets/playerR/Run_7.png',
                    'assets/playerR/Run_8.png','assets/playerR/Run_9.png','assets/playerR/Run_10.png','assets/playerR/Run_11.png']

    walkingLeft = ['assets/playerL/Run.png','assets/playerL/Run_2.png','assets/playerL/Run_3.png','assets/playerL/Run_4.png',
                    'assets/playerL/Run_5.png','assets/playerL/Run_6.png','assets/playerL/Run_7.png',
                    'assets/playerL/Run_8.png','assets/playerL/Run_9.png','assets/playerL/Run_10.png','assets/playerL/Run_11.png']
    blast = ['assets/pew.png']

    def __init__(self):
        super(Player,self).__init__()
        self.dead = False
        self.isWalking = True
        self.isShooting = False
        self.isJumping = False
        self.walkCount = 0
        self.runCount = 0
        self.jumpCount = 15
        self.facing = 'right'
        self.surf = pygame.image.load(self.walkingRight[self.walkCount])
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.x = 0
        self.rect.y = 720
        self.Etype = 'Player'

    def update(self,pressed_keys,running):
        if pressed_keys[K_LEFT]:
            self.facing = 'left'
            self.walking = True
            if self.walkCount >= len(self.walkingLeft)-1:
                self.walkCount = 0
            self.surf = pygame.image.load(self.walkingLeft[self.walkCount])
            self.surf.set_colorkey((0,0,0), RLEACCEL)
            self.rect.x -= 5
            self.walkCount += 1

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
            self.rect(center = player.rect.bottomright)
            self.surf = pygame.image.load('assets/pew.png')

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

class slime(pygame.sprite.Sprite):
    animationCount = 0
    isWalking = 0
    isAttacking = 0
    def __init__(self):
        super(slime, self).__init__()
        self.surf = pygame.image.load('assets/enemies/slime/slime.png')
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), 600))
        self.speed = random.randint(2, 5)
        self.type = 'low-tier'
        self.collide = False


    def update(self):
        movement = ['assets/enemies/slime/slime.png']
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

class mushroom(pygame.sprite.Sprite):
    animationCount = 0
    isWalking = 0
    isAttacking = 0
    def __init__(self):
        super(mushroom, self).__init__()
        self.surf = pygame.image.load('assets/enemies/mushroom/mushroom.png')
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), 600))
        self.speed = random.randint(2, 5)
        self.type = 'mid-tier'

    def update(self):
        movement = ['assets/enemies/mushroom/mushroom.png']
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

class potato(pygame.sprite.Sprite):
    animationCount = 0
    isWalking = 0
    isAttacking = 0
    def __init__(self):
        super(potato, self).__init__()
        self.surf = pygame.image.load('assets/enemies/potato/potato.png')
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), 600))
        self.speed = random.randint(2, 5)
        self.type = 'high-tier'

    def update(self):
        movement = ['assets/enemies/potato/potato.png']
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

# Main Game
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
    fps = 60
    isWalking = False
    enemyList = ['slime', 'mushroom', 'potato', 'coin']
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

class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('Comic Sans MS', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

def endgame():
    global running
    enemyHits = pygame.sprite.spritecollideany(player, enemies)
    #die animation
    running = False
    enemyHits.kill()
    player.rect.x = 0

def playagain():
    pass

def main_menu():
    # Non copyright music, "Bread" by LuKremBo
    pygame.mixer.music.stop()
    pygame.mixer.music.load('bread.mp3')
    pygame.mixer.music.play(-1)
    while True:

        screen.fill((70, 171, 97))
        title = button((70, 171, 97), 540, 50, 220, 100, 'Main Menu')
        title.draw(screen)

        button_1 = button((0,255,0), 540, 200, 220, 100, 'Start')
        button_2 = button((0,255,0), 540, 350, 220, 100, 'Options')
        button_3 = button((0,255,0), 540, 500, 220, 100, 'Quit')
        button_1.draw(screen)
        button_2.draw(screen)
        button_3.draw(screen)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.isOver(pos):
                    game()
                if button_2.isOver(pos):
                    options()
                if button_3.isOver(pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if button_1.isOver(pos):
                    button_1.color=(200,0,0)
                else:
                    button_1.color=(0,255,0)

        pygame.display.update()
        clock.tick(60)

def options():
    running = True
    while running:
        screen.fill((70, 171, 97))

        title = button((70, 171, 97), 540, 50, 220, 100, 'Options')
        title.draw(screen)
        button1 = button((0, 255, 0), 540, 200, 220, 100, 'Back')
        button1.draw(screen)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if button1.isOver(pos):
                    running = False

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

global Score
Score = 0
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 4000)

player = Player()

#All Sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
enemies = pygame.sprite.Group()
ground = pygame.sprite.Group()


main_menu()