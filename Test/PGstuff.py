import pygame, sys
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
import pygame_gui

class Background(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('assets/B1.png'))
        self.sprites.append(pygame.image.load('assets/B2.png'))
        self.sprites.append(pygame.image.load('assets/B3.png'))
        self.sprites.append(pygame.image.load('assets/B4.png'))
        self.sprites.append(pygame.image.load('assets/B5.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self,speed):
        self.current_sprite += speed

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 4

        self.image = self.sprites[int(self.current_sprite)]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40,40))
        self.image.fill((240,240,240))
        self.rect = self.image.get_rect(center= (400,400))
        self.current_health = 200
        self.target_health = 500
        self.maximum_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.health_change_speed = 5


    def update(self):
        self.basic_health()
        self.advanced_health()

    def get_damage(self, amount):
        if self.target_health > 0:
            self.target_health -= amount

        if self.target_health <= 0:
            self.target_health = 0

    def get_health(self, amount):
        if self.target_health < self.maximum_health:
            self.target_health += amount

        if self.target_health >= self.maximum_health:
            self.target_health = self.maximum_health

    def basic_health(self):
        pygame.draw.rect(screen, (230,0,0), (20,20, self.target_health/self.health_ratio, 25))
        pygame.draw.rect(screen, (255,255,255), (20,20,self.health_bar_length,25),4)

    def advanced_health(self):
        transition_width = 0
        transition_color = (240,0,0)

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health)/self.health_ratio)
            transition_color = (0,230,0)

        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.target_health - self.current_health)/self.health_ratio)
            transition_color = (230,230,0)

        health_bar_rect = pygame.Rect(20,60,self.current_health / self.health_ratio,25)
        transition_bar_rect = pygame.Rect(health_bar_rect.right, 60, transition_width, 25)

        pygame.draw.rect(screen,(240,0,0),health_bar_rect)
        pygame.draw.rect(screen,transition_color,transition_bar_rect)
        pygame.draw.rect(screen,(255,255,255),(20,60,self.health_bar_length,25),4)

class Loadingbar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40,40))
        self.image.fill((240,240,240))
        self.rect = self.image.get_rect(center= (400,400))
        self.current_load = 200
        self.maximum_load = 1000
        self.loadbar_length = 400
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.health_change_speed = 5


    def update(self):
        self.basic_health()

    def get_damage(self, amount):
        if self.current_load > 0:
            self.current_load -= amount
        if self.current_load <= 0:
            self.current_load = 0

    def get_health(self, amount):
        if self.current_load < self.maximum_load:
            self.current_load += amount

        if self.current_load >= self.maximum_load:
            self.current_load = self.maximum_load

    def basic_health(self):
        pygame.draw.rect(screen, (230,0,0), (20,20, self.current_load/self.health_ratio, 25))
        pygame.draw.rect(screen, (255,255,255), (20,20,self.loadbar_length,25),4)

class Button(object):

    def __init__(self, position, size):

        # create 3 images
        self._images = [
            pygame.Surface(size),
            pygame.Surface(size),
            pygame.Surface(size),
        ]

        # fill images with color - red, gree, blue
        self._images[0].fill((255,0,0))
        self._images[1].fill((0,255,0))
        self._images[2].fill((0,0,255))

        # get image size and position
        self._rect = pygame.Rect(position, size)

        # select first image
        self._index = 0

    def draw(self, screen):

        # draw selected image
        screen.blit(self._images[self._index], self._rect)

    def event_handler(self, event):

        # change selected color if rectange clicked
        if event.type == pygame.MOUSEBUTTONDOWN: # is some button clicked
            if event.button == 1: # is left button clicked
                if self._rect.collidepoint(event.pos): # is mouse over button
                    self._index = (self._index+1) % 3 # change image


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

def Loadingbartest():
    player = pygame.sprite.GroupSingle(Player())
    # Event Loop / Game Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.sprite.get_health(200)

                if event.key == pygame.K_DOWN:
                    player.sprite.get_damage(200)

        # Draw Stuff
        clock.tick(60)
        screen.fill((30,30,30))
        player.draw(screen)
        player.update()
        pygame.display.flip()

def BackgroundTest():
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

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont('Courier', font_size, bold=True)
    surface, _ = font.render(text=text,fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

class UIElement(Sprite):
    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb):
        super().__init__()

        self.mouse_over = False
        default_image = create_surface_with_text(text, font_size, bg_rgb, text_rgb)
        highlighted_image = create_surface_with_text(text, font_size * 1.2, bg_rgb, text_rgb)
        default_image.get_rect(center = center_position)
        highlighted_image.get_rect(center = center_position)


    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.images[1] if self.mouse_over else self.images[0]

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True

        else:
            self.mouse_over = True

    def draw(self, surface):
        surface.blit(self.image,self.rect)

def MenuTest():
    BLUE = (106,159,181)
    WHITE = (255,255,255)
    uielement = UIElement(
        center_position=(500,500),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text='Hello World'
    )

    while True:
        for event in pygame.event.get():
            pass
        screen.fill(BLUE)
        uielement.update(pygame.mouse.get_pos())
        uielement.draw(screen)
        pygame.display.flip()

def UImanage():
    manager = pygame_gui.UIManager((800,800))
    running = True
    DL1 = pygame.image.load('assets/DL1.png').convert_alpha()

    hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350,227),(100,50)),text='Say Hello',manager=manager)
    image_button = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((500,500),(300,300)),image_surface=DL1, manager=manager)

    while running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == hello_button:
                        print('Hello World!')

                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == image_button:
                        print('I\'m over!')

            manager.process_events(event)

        manager.update(time_delta)

        screen.blit(screen, (0,0))
        manager.draw_ui(screen)
        pygame.display.update()

def ImageTouch():
    Door = pygame.sprite.Sprite
    Door.image1 = pygame.image.load('assets/DL1.png').convert_alpha()
    Door.image2 = pygame.image.load('assets/DL2.png').convert_alpha()
    Door.image = Door.image1

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("You are clicking", event.button)
                if Door.image.get_rect(center=(200,200)).collidepoint(pygame.mouse.get_pos()):
                    print('Touching')
            if event.type == pygame.MOUSEBUTTONUP:
                print("You released", event.button)

        if Door.image.get_rect(center=(200, 200)).collidepoint(pygame.mouse.get_pos()):
            Door.image = Door.image2
        else:
            Door.image = Door.image1

        screen.fill((0,0,0))
        screen.blit(Door.image, (200, 200))  # paint to screen
        pygame.display.flip()  # paint screen one time
        pygame.display.update()

Loadingbartest()