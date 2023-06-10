import pygame
import Main

screen = Main.screen

SCREEN_WIDTH = Main.SCREEN_WIDTH
SCREEN_HEIGHT = Main.SCREEN_HEIGHT

class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, flip):
        super(Cloud, self).__init__()
        self.original_image = pygame.image.load("Cloud.png")
        self.original_image = pygame.transform.scale(self.original_image, (320, 128))
        if flip: self.original_image = pygame.transform.flip(self.original_image, True, False)
        self.image = self.original_image
        self.rect = self.image.get_rect().move(x, y)

class Popup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Popup, self).__init__()
        self.original_image = pygame.image.load("HowToPlay.png")
        self.original_image = pygame.transform.scale(self.original_image, (320, 128))
        self.image = self.original_image
        self.rect = self.image.get_rect().move(x, y)

font = pygame.font.Font(None, 50)
text = font.render(str("Play"), True, (0, 0, 0))
text2 = font.render(str("How to play"), True, (0, 0, 0))

showPopup = False

# running = False
while True:
    mousePosition = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if SCREEN_WIDTH / 2 - 200 <= mousePosition[0] <= SCREEN_WIDTH / 2 + 200 and SCREEN_HEIGHT / 2 - 150 <= mousePosition[1] <= SCREEN_HEIGHT / 2 - 50:
                Main.start()


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

    screen.blit(text, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))
    screen.blit(text2, (SCREEN_WIDTH / 2 - 70, SCREEN_HEIGHT / 2))

    pygame.display.flip()