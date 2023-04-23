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
pixelsPerMeter = 7.2

density = 1.225
g0 = 9.81*7.2
pressure = 101325
temperature = 288.15


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__()
        self.original_image = pygame.image.load("plane.png").convert()
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.image = self.original_image
        self.rect = self.image.get_rect().move(100, 100)
        self.angle = 0
        self.velocity_angle = 0
        self.rotSpeedBase = 0.8
        self.pos = [50, 50]
        self.pos_x = self.pos[0]
        self.pos_y = self.pos[1]
        self.mass = 1000
        self.thrust = 0
        self.acceleration = 2000
        self.maxThrust = 80000
        self.velocity_x = 0
        self.velocity_y = 0
        self.x_heading = math.sin(math.radians(self.angle))
        self.y_heading = math.cos(math.radians(self.angle))
        self.velocity = 0

    def accelerate(self, acceleration):
        x = self.x_heading * acceleration
        y = self.y_heading * acceleration
        # print(str(x) + " " + str(y))
        self.velocity_y += y
        self.velocity_x += x


    def turn(self):
        self.x_heading = math.sin(math.radians(self.angle))
        self.y_heading = math.cos(math.radians(self.angle))
        if self.y_heading < 0:
            self.velocity_y = self.velocity * self.y_heading
        else:
            self.velocity_y = -self.velocity * self.y_heading
        self.velocity_x = -self.velocity * self.x_heading

        print(self.y_heading)

    def update(self, pressed_keys):
        self.rotSpeed = self.rotSpeedBase + self.rotSpeedBase * self.velocity / 700

        if pressed_keys[K_UP]:
            self.thrust += self.acceleration
        if pressed_keys[K_DOWN]:
            self.thrust -= self.acceleration

        if self.thrust > self.maxThrust:
            self.thrust = self.maxThrust
        elif self.thrust < 0:
            self.thrust = 0

        y_acc = (((self.mass * g0) - (self.y_heading * self.thrust)) / self.mass) * dt
        self.velocity_y += y_acc

        x_acc = -self.x_heading * self.thrust / self.mass * dt
        self.velocity_x += x_acc

        self.velocity = math.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)

        self.pos_x += self.velocity_x * dt
        self.pos_y += self.velocity_y * dt
        self.rect.center = (self.pos_x, self.pos_y)

        if pressed_keys[K_LEFT]:
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.angle += self.rotSpeed
            x, y = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.turn()
            # self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.angle -= self.rotSpeed
            x, y = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.turn()


pygame.init()

# font = pygame.font.Font('freesansbold.ttf', 32)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player()

running = True

while running:
    screen.fill((0, 0, 0))

    clock = pygame.time.Clock()
    dt = clock.tick(60)/1000
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    font = pygame.font.Font(None, 30)
    text = font.render(str(round(player.velocity, 2)) + " m/s", True, (255, 255, 255))
    text2 = font.render(str(round(player.thrust, 2)) + " N", True, (255, 255, 255))
    screen.blit(text, [10,10])
    screen.blit(text2, [10, 50])

    screen.blit(player.image, player.rect)

    pygame.display.flip()
