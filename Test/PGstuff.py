import pygame, sys

class Background(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('B1.png'))
        self.sprites.append(pygame.image.load('B2.png'))
        self.sprites.append(pygame.image.load('B3.png'))
        self.sprites.append(pygame.image.load('B4.png'))
        self.sprites.append(pygame.image.load('B5.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self,speed):
        self.current_sprite += speed

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 4

        self.image = self.sprites[int(self.current_sprite)]

class Loadingbar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40,40))
        self.image.fill((240,240,240))
        self.rect = self.image.get_rect(center= (400,400))

    def update(self):
        pass

# Initialize and Time
pygame.init()
clock = pygame.time.Clock()

# Game Screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Test Stuff')

# Creating the sprites and groups
moving_sprites = pygame.sprite.Group()
bckgrnd = Background(0,0)
moving_sprites.add(bckgrnd)

def Gametest1():
    # Event Loop / Game Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Draw stuff
            pygame.display.flip()
        clock.tick(60)

def Gametest2():
    # Event Loop / Game Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Draw stuff
            moving_sprites.draw(screen)
            moving_sprites.update(0.28)
            pygame.display.flip()
        clock.tick(60)

Gametest2()

