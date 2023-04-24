import pygame
import math

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 720

density = 1.225
g0 = 9.81

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__()
        self.original_image = pygame.image.load("plane.png").convert()
        self.original_image = pygame.transform.scale(self.original_image, (50,50))
        self.image = self.original_image
        self.rect = self.image.get_rect().move(100,100)
        self.angle = 0
        self.rotSpeed = 2.5
        self.pos = [50,50]
        self.pos_x = self.pos[0]
        self.pos_y = self.pos[1]

    def velocity(self, velocity):

        x = math.sin(math.radians(self.angle)) * velocity
        y = math.cos(math.radians(self.angle)) * velocity
        # print(str(x) + " " + str(y))
        return [x,y]

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.pos_x -= self.velocity(0.4)[0] * dt
            self.pos_y -= self.velocity(0.4)[1] * dt
        if pressed_keys[K_DOWN]:
            self.pos_x += self.velocity(0.4)[0] * dt
            self.pos_y += self.velocity(0.4)[1] * dt

        if pressed_keys[K_LEFT]:
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.angle += self.rotSpeed
            x,y = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = (x,y)
            # self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.angle -= self.rotSpeed
            x, y = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

        self.rect.center = (self.pos_x, self.pos_y)


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player()

running = True
clock = pygame.time.Clock()
dt = clock.tick(60)
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    screen.fill((0, 0, 0))

    screen.blit(player.image, player.rect)

    pygame.display.flip()