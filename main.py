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
g0 = 9.81 * 7.2
pressure = 101325
temperature = 288.15


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__()
        self.original_image = pygame.image.load("plane.png").convert()
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.angle = 0.01
        self.image = pygame.transform.rotate(self.original_image, -90)
        self.rect = self.image.get_rect().move(100, 100)
        self.velocity_angle = 0
        self.rotSpeedBase = 0.2
        self.pos = [50, 50]
        self.pos_x = self.pos[0]
        self.pos_y = self.pos[1]
        self.mass = 1000
        self.thrust = 0
        self.acceleration = 2000
        self.maxThrust = 40000
        self.velocity_x = 0
        self.velocity_y = 0
        self.x_heading = math.sin(math.radians(self.angle))
        self.y_heading = math.cos(math.radians(self.angle))
        self.velocity = 0
        self.accelerationVector = pygame.math.Vector2(0, 0)
        self.velocityVector = pygame.math.Vector2(0, 0)
        self.liftCoefficient = 0.15
        self.dragCoefficient = 0.08
        self.surfaceArea = 10

    def accelerate(self, acceleration):
        x = self.x_heading * acceleration
        y = self.y_heading * acceleration
        # print(str(x) + " " + str(y))
        self.velocity_y += y
        self.velocity_x += x

    def turn(self):
        self.accelerationVector.rotate_ip(self.rotSpeed)
        self.velocityVector.rotate_ip(-self.rotSpeed)
        # self.velocityVector.x = self.velocityVector.x / math.cos(math.radians(self.rotSpeed))
        # self.velocityVector.y = self.velocityVector.y / math.cos(math.radians(self.rotSpeed))
        # self.x_heading = math.sin(math.radians(self.angle))
        # self.y_heading = math.cos(math.radians(self.angle))
        # if self.y_heading < 0:
        #     self.velocity_y = self.velocity * self.y_heading
        # else:
        #     self.velocity_y = -self.velocity * self.y_heading
        # self.velocity_x = -self.velocity * self.x_heading
        #
        # print(self.y_heading)

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.thrust += self.acceleration
        if pressed_keys[K_DOWN]:
            self.thrust -= self.acceleration

        if self.thrust > self.maxThrust:
            self.thrust = self.maxThrust
        elif self.thrust < 0:
            self.thrust = 0

        # accY = ((math.cos(math.radians(self.angle)) * g0 * self.mass - 0*0.5*density*self.velocity_x**2*self.surfaceArea*self.liftCoefficient) / self.mass) * dt
        # accX = ((math.cos(math.radians(90-self.angle)) * g0 * self.mass + self.thrust) / self.mass) * dt
        accY = ((g0 * self.mass) * math.cos(math.radians(self.angle)) - 0.5*density*self.velocity_x**2*self.surfaceArea*self.liftCoefficient) / self.mass * dt
        accX = ((g0 * self.mass) * math.cos(math.radians(90-self.angle)) - self.thrust + 0.5*density*self.velocity_x**2*self.surfaceArea*self.dragCoefficient) / self.mass * dt
        self.accelerationVector = pygame.math.Vector2(accX, accY)
        print("Acc X: " + str(accX))
        print("Acc Y: " + str(accY))
        print("dV X: " + str((accX*math.cos(math.radians(self.angle)) + accY*math.sin(math.radians(self.angle)))))
        print("dV Y: " + str((accX*math.sin(math.radians(self.angle)) + accY*math.cos(math.radians(self.angle)))))

        # self.velocityVector += self.accelerationVector
        self.velocityVector.x -= (accX*math.cos(math.radians(self.angle)) + accY*math.sin(math.radians(self.angle)))
        self.velocityVector.y += (accX*math.sin(math.radians(self.angle)) + accY*math.cos(math.radians(self.angle)))

        # self.velocityVector.y += g0 * dtn
        # self.velocityVector.y -= math.sin(math.radians(self.angle)) * self.thrust / self.mass * dt
        # self.velocityVector.x += math.cos(math.radians(self.angle)) * self.thrust / self.mass * dt

        if self.velocityVector.x > 500:
            self.velocityVector.x = 500
        elif self.velocityVector.x < -500:
            self.velocityVector.x = -500
        if self.velocityVector.y > 500:
            self.velocityVector.y = 500
        elif self.velocityVector.y < -500:
            self.velocityVector.y = -500


        if self.pos_x > SCREEN_WIDTH:
            self.pos_x = 0
        elif self.pos_x < 0:
            self.pos_x = SCREEN_WIDTH
        if self.pos_y > SCREEN_HEIGHT:
            self.pos_y = 0
        elif self.pos_y < 0:
            self.pos_y = SCREEN_HEIGHT

        self.rect.center = (self.pos_x, self.pos_y)

        if pressed_keys[K_LEFT]:
            self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
            self.rotSpeed = self.rotSpeedBase + self.rotSpeedBase * self.velocity / 40
            self.angle += self.rotSpeed
            x, y = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.turn()
            # self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
            self.rotSpeed = -self.rotSpeedBase - self.rotSpeedBase * self.velocity / 40
            # self.angle -= self.rotSpeed
            self.angle += self.rotSpeed
            x, y = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.turn()

        self.velocity_x = self.velocityVector.x
        self.velocity_y = self.velocityVector.y

        self.velocity = math.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)

        self.pos_x += self.velocity_x * dt
        self.pos_y += self.velocity_y * dt


pygame.init()

# font = pygame.font.Font('freesansbold.ttf', 32)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player()

running = True

while running:
    screen.fill((0, 0, 0))

    clock = pygame.time.Clock()
    dt = clock.tick(60) / 1000
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
    text3 = font.render(str(round(player.angle, 2)) + " deg", True, (255, 255, 255))
    text4 = font.render(str(round(player.velocityVector.x, 2)) + " - " + str(round(player.velocityVector.y, 2)), True, (255, 255, 255))
    text5 = font.render(str(round(player.accelerationVector.x, 2)) + " - " + str(round(player.accelerationVector.y, 2)), True, (255, 255, 255))
    screen.blit(text, [10, 10])
    screen.blit(text2, [10, 50])
    screen.blit(text3, [10, 90])
    screen.blit(text4, [10, 130])
    screen.blit(text5, [10, 180])

    screen.blit(player.image, player.rect)

    pygame.display.flip()
