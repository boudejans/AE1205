import pygame
import main

screen = main.screen

SCREEN_WIDTH = main.SCREEN_WIDTH
SCREEN_HEIGHT = main.SCREEN_HEIGHT

# Cloud object for decoration
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, flip):
        super(Cloud, self).__init__()
        self.original_image = pygame.image.load("Level Assets/Cloud.png")
        self.original_image = pygame.transform.scale(self.original_image, (320, 128))
        if flip: self.original_image = pygame.transform.flip(self.original_image, True, False)
        self.image = self.original_image
        self.rect = self.image.get_rect().move(x, y)

# Popup object for the different messages to be displayed
class Popup(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super(Popup, self).__init__()
        if type == "HowToPlay":
            self.original_image = pygame.image.load("HowToPlay.png")
        elif type == "Credits":
            self.original_image = pygame.image.load("Credits.png")
        elif type == "GameOver":
            self.original_image = pygame.image.load("GameOver.png")
        self.original_image = pygame.transform.scale(self.original_image, (768, 512))
        self.image = self.original_image
        self.rect = self.image.get_rect().move(x - 768/2, y - 512/2)

# Create the text objects to be displayed
font = pygame.font.Font(None, 50)
text = font.render(str("Play"), True, (0, 0, 0))
text2 = font.render(str("How to play"), True, (0, 0, 0))
text3 = font.render(str("Credits"), True, (0, 0, 0))
title = font.render(str("Boulder Bot"), True, (0, 0, 0))
popup = None

# This is called when the player was caught and shows the game over popup
def playerDied():
    popup = Popup(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, "GameOver")
    screen.blit(popup.image, popup.rect)

while True:
    mousePosition = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # If esc is pressed, either close the popup or quit the game
                if popup != None:
                    popup.kill()
                    popup = None
                else:
                    pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:  # Check if a popup should be closed or if a button is pressed
            if popup != None:
                popup.kill()
                popup = None
            else:
                if SCREEN_WIDTH / 2 - 200 <= mousePosition[0] <= SCREEN_WIDTH / 2 + 200 and SCREEN_HEIGHT / 2 - 150 <= mousePosition[1] <= SCREEN_HEIGHT / 2 - 50:
                    main.start()
                if SCREEN_WIDTH / 2 - 200 <= mousePosition[0] <= SCREEN_WIDTH / 2 + 200 and SCREEN_HEIGHT / 2 - 50 <= mousePosition[1] <= SCREEN_HEIGHT / 2 + 50:
                    popup = Popup(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, "HowToPlay")
                if SCREEN_WIDTH / 2 - 200 <= mousePosition[0] <= SCREEN_WIDTH / 2 + 200 and SCREEN_HEIGHT / 10 * 9 - 50 <= mousePosition[1] <= SCREEN_HEIGHT / 10 * 9 + 50:
                    popup = Popup(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, "Credits")

    # Create the main menu background
    screen.fill((111, 177, 250))
    clouds = []
    clouds.append(Cloud(200, 300, False))
    clouds.append(Cloud(800, 500, False))
    clouds.append(Cloud(400, 800, True))
    clouds.append(Cloud(1500, 600, True))
    clouds.append(Cloud(900, 50, False))
    clouds.append(Cloud(1250, 250, True))
    clouds.append(Cloud(1150, 800, False))

    for cloud in clouds:
        screen.blit(cloud.image, cloud.rect)

    # Show the title and button texts
    screen.blit(text, (SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2 - 100))
    screen.blit(text2, (SCREEN_WIDTH / 2 - 110, SCREEN_HEIGHT / 2))
    screen.blit(text3, (SCREEN_WIDTH / 2 - 70, SCREEN_HEIGHT / 10 * 9))
    screen.blit(title, (SCREEN_WIDTH / 2 - 120, SCREEN_HEIGHT / 10 * 3))

    if popup != None:
        screen.blit(popup.image, popup.rect)

    pygame.display.flip()