import pygame, sys



# Pygame setup screen + Variables
pygame.init()
pygame.mixer.init()
SCREEN = pygame.display.set_mode((1280, 720))
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = 'Crossy'
GRAY = (84,84,84)
BLACK = (0,0,0)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Comic Sans MS',65)
Level = 1
clicked = False
counter = 0

# Image Variables
imgs = { 'p1' : {1:'players/p.png', 2:'players/V.png'},'p1b':{1:'players/pp.png', 2:'players/V2.png'},
         'en1': {1:'enemies/e.png'},'en1b': {1:'enemies/ee.png'},
         'en2': {1:'enemies/e2.png'},'en2b': {1:'enemies/ee2.png'},
         'en3': {1:'enemies/e3.png'},'en3b': {1:'enemies/ee3.png'},
         'en4': {1:'enemies/e4.png'},'en4b': {1:'enemies/ee4.png'},
         'tre': {1:'t.png'},'tre2': {1:'k.png'},
         'bckgrnd1' : {1:'backgrounds/b.png', 2:'backgrounds/minea.png'},
         'bckgrnd2' : {1:'backgrounds/b2.png', 2:'backgrounds/mineb.png'}
         }

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

def main_menu():
    main = True
    while main:

        SCREEN.fill((70, 171, 97))
        title = button((70, 171, 97), 540, 50, 220, 100, 'This is a Menu?',size=100)
        title.draw(SCREEN)

        button_1 = button((0,255,0), 520, 200, 260, 100, '1 Player',('Comic Sans MS',60))
        button_2 = button((0,255,0), 520, 350, 260, 100, '2 Player',('Comic Sans MS',60))
        button_3 = button((0,255,0), 540, 500, 220, 100, 'Quit',('Comic Sans MS',60))
        button_1.draw(SCREEN)
        button_2.draw(SCREEN)
        button_3.draw(SCREEN)


        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.isOver(pos):
                    global Level
                    Level = 1
                    new_game.gameloop(1)
                if button_2.isOver(pos):
                    Level = 1
                    new_game2.gameloop(1)
                    main_menu()
                if button_3.isOver(pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if button_1.isOver(pos):
                    button_1.color=(200,0,0)
                else:
                    button_1.color=(0,255,0)

        pygame.display.update()
        clock.tick(30)

def Shop():
    main = True
    while main:

        SCREEN.fill((70, 171, 97))
        title = button((70, 171, 97), 540, 50, 220, 100, 'This is a Menu?',size=100)
        title.draw(SCREEN)

        button_1 = button((0,255,0), 520, 200, 260, 100, 'Player 1',('Comic Sans MS',60))
        button_2 = button((0,255,0), 520, 350, 260, 100, 'Player 2',('Comic Sans MS',60))
        button_3 = button((0,255,0), 540, 500, 220, 100, 'Backgrounds',('Comic Sans MS',60))
        button_1.draw(SCREEN)
        button_2.draw(SCREEN)
        button_3.draw(SCREEN)


        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.isOver(pos):
                    global Level
                    Level = 1
                    new_game.gameloop(1)
                if button_2.isOver(pos):
                    Level = 1
                    new_game2.gameloop(1)
                    main_menu()
                if button_3.isOver(pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if button_1.isOver(pos):
                    button_1.color=(200,0,0)
                else:
                    button_1.color=(0,255,0)

        pygame.display.update()
        clock.tick(30)

# Parent Class that controls the entire game
class Game2:
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
                        new_game2.gameloop(1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_1.isOver(pos):
                        Level = 1
                        new_game2.gameloop(1)
                    if background.isOver(pos):
                        global running
                        running = False
                        play = False
                        main_menu()
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


        player = Player(imgs['p1'][2],imgs['p1b'][2],280,650, 50, 50)
        player2 = Player(imgs['p1'][1],imgs['p1b'][1],875,650, 50, 50)
        enemy1 = Enemy(imgs['en1'][1],imgs['en1b'][1], 20, 560,50,50)
        enemy1.speed *= level_speed
        enemy2 = Enemy(imgs['en2'][1],imgs['en2b'][1], 200, 450, 50, 50)
        enemy2.speed *= level_speed
        enemy3 = Enemy(imgs['en3'][1],imgs['en3b'][1], 400, 330, 50, 50)
        enemy3.speed *= level_speed
        enemy4 = Enemy(imgs['en4'][1],imgs['en4b'][1], 800, 200, 50, 50)
        enemy4.speed *= level_speed
        enemies = [enemy1, enemy2, enemy3,enemy4]

        treasure = GameObject(imgs['tre'][1],imgs['tre'][1],280, 50, 50, 50)
        treasure2 = GameObject(imgs['tre'][1],imgs['tre'][1],875, 50, 50, 50)

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
                    elif event.key == pygame.K_ESCAPE:
                        global play
                        running = False
                        play = False
                        main_menu()

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
                    pygame.mixer.music.load('m.mp3')
                    pygame.mixer.music.play(1)
                    text = font.render('Player 1 Died', True, BLACK)
                    self.SCREEN.blit(text, (420, 200))
                    text2 = font.render('You made it to level: ' + str(Level), True, BLACK)
                    self.SCREEN.blit(text2, (300, 110))
                    Game2.playagain(self)
                    pygame.display.update()
                    clock.tick(0.3)

                if player2.detection(enemy):
                    running = False
                    win = False
                    player2.draw2(self.SCREEN)
                    enemy1.draw2(self.SCREEN)
                    if level_speed > 2:
                        enemy2.draw2(self.SCREEN)
                    if level_speed > 4:
                        enemy3.draw2(self.SCREEN)
                    if level_speed > 6:
                        enemy4.draw2(self.SCREEN)
                    pygame.mixer.music.load('m.mp3')
                    pygame.mixer.music.play(1)
                    text = font.render('Player 2 Died', True, BLACK)
                    self.SCREEN.blit(text, (420, 200))
                    text2 = font.render('You made it to level: ' + str(Level), True, BLACK)
                    self.SCREEN.blit(text2, (300, 110))
                    Game2.playagain(self)
                    pygame.display.update()
                    clock.tick(0.3)

            if player.detection(treasure) and player2.detection(treasure2):
                Level += 1
                print(Level)
                running = False
                win = True
                player.draw(self.SCREEN)
                pygame.display.update()
                clock.tick(3)
            text = font.render('Level ' + str(Level), True, BLACK)
            self.SCREEN.blit(text, (530, 20))
            pygame.display.update()
            clock.tick(self.TICK)

        # For every Level completed the game gets harder
        if win == True:
            self.gameloop(level_speed + 0.5)
        else:
            pass



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
            background = button((86, 91, 94), 430, 50, 440, 500)
            background.draw(self.SCREEN)
            title = button((86, 91, 94), 540, 110, 220, 10, 'You Died!','',90)
            title.draw(self.SCREEN)

            button_1 = button((141, 156, 166), 540, 250, 220, 100, 'Try Again')
            button_2 = button((141, 156, 166), 540, 400, 220, 100, 'Quit')
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
                        global running
                        running = False
                        play = False
                        main_menu()
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

        player = Player('players/V.png','players/V2.png',610,650, 50, 50)
        enemy1 = Enemy('enemies/e.png','enemies/ee.png', 20, 560,50,50)
        enemy1.speed *= level_speed
        enemy2 = Enemy('enemies/e2.png','enemies/ee2.png', 200, 450, 50, 50)
        enemy2.speed *= level_speed
        enemy3 = Enemy('enemies/e3.png','enemies/ee3.png', 400, 330, 50, 50)
        enemy3.speed *= level_speed
        enemy4 = Enemy('enemies/e4.png','enemies/ee4.png', 800, 200, 50, 50)
        enemy4.speed *= level_speed
        enemies = [enemy1, enemy2, enemy3,enemy4]

        treasure = GameObject('k.png','t.png',610, 50, 50, 50)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction = 1
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                    elif event.key == pygame.K_w:
                        direction = 1
                    elif event.key == pygame.K_s:
                        direction = -1
                    elif event.key == pygame.K_ESCAPE:
                        global play
                        running = False
                        play = False
                        main_menu()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        direction = 0

            self.SCREEN.fill(GRAY)
            self.SCREEN.blit(self.image,(0,0))

            treasure.draw(self.SCREEN)
            player.move(direction, self.height)
            player.draw(self.SCREEN)

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


                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('m.mp3')
                    pygame.mixer.music.play(1)
                    Game.playagain(self)
                    text = font.render('You Lose', True, BLACK)
                    self.SCREEN.blit(text, (510, 150))
                    text2 = font.render('You made it to level: ' + str(Level), True, BLACK)
                    self.SCREEN.blit(text2, (320, 300))
                    pygame.display.update()
                    clock.tick(0.3)


            if player.detection(treasure):
                Level += 1
                print(Level)
                running = False
                win = True
                player.draw(self.SCREEN)
                pygame.display.update()
                clock.tick(3)
            text = font.render('Level ' + str(Level), True, BLACK)
            self.SCREEN.blit(text, (30, 20))
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


new_game = Game(imgs['bckgrnd1'][2],SCREEN_TITLE,SCREEN_WIDTH,SCREEN_HEIGHT)
new_game2 = Game2(imgs['bckgrnd2'][2],SCREEN_TITLE,SCREEN_WIDTH,SCREEN_HEIGHT)

main_menu()
