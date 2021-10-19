######################################
# Shane Donivan
# PM Class
# Senior
# 8/26/21
# 01 - Game Refresher
# A Crossy type game where you get
# to the other side
#######################################

import pygame, sys

# Pygame setup screen + Variables
pygame.init()
pygame.mixer.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = 'Crossy 2.0'
GRAY = (84,84,84)
BLACK = (0,0,0)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Comic Sans MS',65)
Level = 1

# Woo Buttons
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

# Parent Class that controls the entire game
class Game:
    TICK = 60
    running = True

    def __init__(self, image, title, width, height):
        self.image = image
        self.title = title
        self.width = width
        self.height = height

        self.SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.SCREEN.fill(GRAY)
        pygame.display.set_caption(SCREEN_TITLE)

        background = pygame.image.load(image)
        self.image = pygame.transform.scale(background, (width, height))

    def playagain(self):
        play = True
        while play:
            background = button((86, 91, 94), 400, 320, 440, 350)
            background.draw(self.SCREEN)

            button_1 = button((141, 156, 166), 510, 370, 220, 100, 'Try Again')
            button_2 = button((141, 156, 166), 510, 520, 220, 100, 'Quit')
            button_1.draw(self.SCREEN)
            button_2.draw(self.SCREEN)

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_RETURN:
                        global Level
                        Level = 1
                        new_game.gameloop(1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_1.isOver(pos):
                        Level = 1
                        new_game.gameloop(1)
                    if background.isOver(pos):
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    if button_1.isOver(pos):
                        button_1.color=(200,0,0)
                    else:
                        button_1.color=(0,255,0)
            pygame.display.update()
            clock.tick(30)

    # Shows stuff on screen, and runs events
    def gameloop(self,level_speed):
        running = True
        win = False
        direction = 0
        direction2 = 0

        player = Player('p.png','p2.png',280,650, 50, 50)
        player2 = Player('p.png','p2.png',875,650, 50, 50)
        enemy1 = Enemy('e.png','ee.png', 20, 560,50,50)
        enemy1.speed *= level_speed
        enemy2 = Enemy('e2.png','ee2.png', 200, 450, 50, 50)
        enemy2.speed *= level_speed
        enemy3 = Enemy('e3.png','ee3.png', 400, 330, 50, 50)
        enemy3.speed *= level_speed
        enemy4 = Enemy('e4.png','ee4.png', 800, 200, 50, 50)
        enemy4.speed *= level_speed
        enemies = [enemy1, enemy2, enemy3,enemy4]

        treasure = GameObject('t.png','t.png',280, 50, 50, 50)
        treasure2 = GameObject('t.png','t.png',875, 50, 50, 50)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction2 = 1
                    elif event.key == pygame.K_DOWN:
                        direction2 = -1
                    elif event.key == pygame.K_w:
                        direction = 1
                    elif event.key == pygame.K_s:
                        direction = -1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction2 = 0
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        direction = 0

            self.SCREEN.fill(GRAY)
            self.SCREEN.blit(self.image,(0,0))

            treasure.draw(self.SCREEN)
            treasure2.draw(self.SCREEN)
            player.move(direction,self.height)
            player.draw(self.SCREEN)
            player2.move(direction2, self.height)
            player2.draw(self.SCREEN)

            enemy1.move(self.width)
            enemy1.draw(self.SCREEN)

            # Increases the number of enemies for the rest of the levels
            if level_speed > 2:
                enemy2.move(self.width)
                enemy2.draw(self.SCREEN)
            if level_speed > 4:
                enemy3.move(self.width)
                enemy3.draw(self.SCREEN)
            if level_speed > 6:
                enemy4.move(self.width)
                enemy4.draw(self.SCREEN)

            # Collision for every enemy, changes animation, and shows Score
            for enemy in enemies:
                if player.detection(enemy):
                    global Level
                    running = False
                    win = False
                    player.draw2(self.SCREEN)
                    enemy1.draw2(self.SCREEN)
                    if level_speed > 2:
                        enemy2.draw2(self.SCREEN)
                    if level_speed > 4:
                        enemy3.draw2(self.SCREEN)
                    if level_speed > 6:
                        enemy4.draw2(self.SCREEN)
                    text = font.render('You Lose', True, BLACK)
                    self.SCREEN.blit(text, (280, 150))
                    text2 = font.render('You made it to level: ' + str(Level), True, BLACK)
                    self.SCREEN.blit(text2, (320, 30))
                    Game.playagain(self)
                    pygame.display.update()
                    clock.tick(0.3)

                if player2.detection(enemy):
                    running = False
                    win = False
                    player.draw2(self.SCREEN)
                    enemy1.draw2(self.SCREEN)
                    if level_speed > 2:
                        enemy2.draw2(self.SCREEN)
                    if level_speed > 4:
                        enemy3.draw2(self.SCREEN)
                    if level_speed > 6:
                        enemy4.draw2(self.SCREEN)
                    text = font.render('You Lose', True, BLACK)
                    self.SCREEN.blit(text, (875, 150))
                    text2 = font.render('You made it to level: ' + str(Level), True, BLACK)
                    self.SCREEN.blit(text2, (320, 30))
                    Game.playagain(self)
                    pygame.display.update()
                    clock.tick(0.3)

            if player.detection(treasure) and player2.detection(treasure2):
                Level += 1
                print(Level)
                running = False
                win = True
                text = font.render('Level ' + str(Level), True, BLACK)
                self.SCREEN.blit(text, (530, 150))
                player.draw(self.SCREEN)
                pygame.display.update()
                clock.tick(0.4)
            pygame.display.update()
            clock.tick(self.TICK)

        # For every Level completed the game gets harder
        if win == True:
            self.gameloop(level_speed + 0.5)
        else:
            pass

# Parent Class for the Player and Enemies
class GameObject:

    # Sets up animation, position on screen, and scale of object
    def __init__(self, img,img2, x, y, width, height):
        object_image = pygame.image.load(img)
        object_image2 = pygame.image.load((img2))
        self.image = pygame.transform.scale(object_image, (width, height))
        self.image2 = pygame.transform.scale(object_image2, (width, height))

        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height

    def draw(self,background):
        background.blit(self.image,(self.x_pos,self.y_pos))

    def draw2(self, background):
        background.blit(self.image2, (self.x_pos, self.y_pos))

# Sets up movement calculations
class Player(GameObject):
    speed = 20
    def __init__(self,img,img2, x, y, width, height):
        super().__init__(img,img2, x, y, width, height)

    def move(self, direction, max_height):
        if direction > 0:
            self.y_pos -= self.speed
        elif direction < 0:
            self.y_pos += self.speed

        if self.y_pos >= max_height - 50:
            self.y_pos = max_height - 50
        elif self.y_pos <= 0:
            self.y_pos = 0


    def detection(self, other_body):
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False

        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            return False

        return True

# Makes Enemy bounce back and forth
class Enemy(GameObject):
    speed = 5
    def __init__(self, img,img2, x, y, width, height):
        super().__init__(img,img2, x, y, width, height)

    def move(self,max_width):
        if self.x_pos <= 20:
            self.speed = abs(self.speed)
        elif self.x_pos >= max_width - 60:
            self.speed = -abs(self.speed)
        self.x_pos += self.speed



# Runs the game
new_game = Game('b2.png',SCREEN_TITLE,SCREEN_WIDTH,SCREEN_HEIGHT)
new_game.gameloop(1)

