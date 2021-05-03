import pygame, sys
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.velocity = [0, 0]

    def update(self):
        self.rect.move_ip(*self.velocity)


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


class button2():
    width = 180
    height = 70

    def __init__(self, x, y,button,hover,clicked):
        self.x = x
        self.y = y
        self.button = button
        self.hover = hover
        self.clicked = clicked

    def draw(self):

        global clicked
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.width, self.height)

        # check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(screen, self.clicked, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(screen, self.hover, button_rect)
        else:
            pygame.draw.rect(screen, self.button, button_rect)

        return action

def main_menu():
    # Non copyright music, "Bread" by LuKremBo
    pygame.mixer.music.stop()
    pygame.mixer.music.load('bread.mp3')
    pygame.mixer.music.play(-1)
    while True:

        screen.fill((70, 171, 97))
        title = button((70, 171, 97), 540, 50, 220, 100, 'Main Menu')
        title.draw(screen)

        button_1 = button((0,255,0), 540, 200, 220, 100, 'Start',('Comic Sans MS',60))
        button_2 = button((0,255,0), 540, 350, 220, 100, 'Options',('Comic Sans MS',60))
        button_3 = button((0,255,0), 540, 500, 220, 100, 'Quit',('Comic Sans MS',60))
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



def game():
    # NCS, "Sunburst" by Tobu & Itro
    pygame.mixer.music.stop()
    pygame.mixer.music.load('sunburst.mp3')
    pygame.mixer.music.play(-1)
    running = True
    player = Player()
    while running:
        dt = clock.tick(FPS) / 1000
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
                pygame.QUIT()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.velocity[1] = -200 * dt  # 200 pixels per second
                elif event.key == pygame.K_s:
                    player.velocity[1] = 200 * dt
                elif event.key == pygame.K_a:
                    player.velocity[0] = -200 * dt
                elif event.key == pygame.K_d:
                    player.velocity[0] = 200 * dt
                if event.key == K_ESCAPE:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('bread.mp3')
                    pygame.mixer.music.play(-1)
                    running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player.velocity[1] = 0
                elif event.key == pygame.K_a or event.key == pygame.K_d:
                    player.velocity[0] = 0

        player.update()

        screen.blit(player.image, player.rect)
        pygame.display.update()


def options():
    running = True
    global num
    global fullscreen
    monitor_size = [pygame.display.Info().current_w,pygame.display.Info().current_h]
    if fullscreen:
        screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((1280,720))
    while running:
        screen.fill((70, 171, 97))

        title = button((70, 171, 97), 540, 50, 220, 100, 'Options',('Comic Sans MS'),60)
        title.draw(screen)
        button1 = button((0, 255, 0), 540, 500, 220, 100, 'Back',('Comic Sans MS'),60)
        button2 = button((0,255,0), 540, 200, 220, 100, 'FullScreen',('Comic Sans MS'),40)
        button1.draw(screen)
        button2.draw(screen)

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
                if button2.isOver(pos):
                    num += 1
                    if (num % 2) == 0:
                        fullscreen = True
                    else:
                        fullscreen = False
                    if fullscreen:
                        screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((1280,720))


        pygame.display.update()
        clock.tick(60)

pygame.init()
pygame.mixer.init()
mainClock = pygame.time.Clock()
pygame.display.set_caption('Pygame Test')
font = 'Comic Sans MS'

successes, failures = pygame.init()
print("Initializing pygame: {0} successes and {1} failures.".format(successes, failures))
pygame.time.delay(1000)
screen = pygame.display.set_mode((1280, 720))
global fullscreen
fullscreen = False
global num
num = 1
clock = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
file = 'some.mp3'
DL1 = 'DL1.png'
DL2 = 'DL2.png'
DL3 = 'DL1.png'

main_menu()