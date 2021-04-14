import pygame
import pygame_menu

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.velocity = [0, 0]

    def update(self):
        self.rect.move_ip(*self.velocity)

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
HOVER_COLOR = (50, 70, 90)
# Don't define new font objects in your while loop (that's inefficient).
FONT = pygame.font.SysFont ("Times New Norman", 60)
# If the text surfaces and button rects don't change,
# you can define them once outside of the while loop.
text1 = FONT.render("START", True, WHITE)
text2 = FONT.render("OPTIONS", True, WHITE)
text3 = FONT.render("ABOUT", True, WHITE)
text4 = FONT.render("QUIT", True, WHITE)
rect1 = pygame.Rect(300,200,205,80)
rect2 = pygame.Rect(300,300,205,80)
rect3 = pygame.Rect(300,400,205,80)
rect4 = pygame.Rect(300,500,205,80)
# The buttons consist of a text surface, a rect and a color.
buttons = [
    [text1, rect1, BLACK],
    [text2, rect2, BLACK],
    [text3, rect3, BLACK],
    [text4, rect4, BLACK]
    ]

def game_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEMOTION:
                for button in buttons:

                    # button[1] is the rect. Use its collidepoint method with
                    # the `event.pos` (mouse position) to detect collisions.
                    if button[1].collidepoint(event.pos):
                        # Set the button's color to the hover color.
                        button[2] = HOVER_COLOR
                    else:
                        # Otherwise reset the color to black.
                        button[2] = BLACK
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
def game():
    while running:
        dt = clock.tick(FPS) / 1000  # Returns milliseconds between each call to 'tick'. The convert time to seconds.
        screen.fill(BLACK)  # Fill the screen with background color.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.velocity[1] = -200 * dt  # 200 pixels per second
                elif event.key == pygame.K_s:
                    player.velocity[1] = 200 * dt
                elif event.key == pygame.K_a:
                    player.velocity[0] = -200 * dt
                elif event.key == pygame.K_d:
                    player.velocity[0] = 200 * dt
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player.velocity[1] = 0
                elif event.key == pygame.K_a or event.key == pygame.K_d:
                    player.velocity[0] = 0

        player.update()

        screen.blit(player.image, player.rect)
        pygame.display.update()  # Or pygame.display.flip()

        screen.fill((20, 50, 70))

        # Draw the buttons with their current colors at their rects.
        # You can unpack the button lists directly in the head of the loop.
        for text, rect, color in buttons:
            pygame.draw.rect(screen, color, rect)
            screen.blit(text, rect)

        pygame.display.flip()
        clock.tick(15)


game_intro()
pygame.quit()