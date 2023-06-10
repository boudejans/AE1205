import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.original_image = pygame.image.load("Competition/player.png")
        self.original_image = pygame.transform.scale(self.original_image, (30, 30))
        self.image = self.original_image
        self.bot = False
        self.rect = self.image.get_rect().move(100, 100)
        self.pos = [100, 100]
        self.velocityVector = pygame.math.Vector2(0,0)
        self.velocity = 0.02
        self.mass = 1
        self.jump = False
        self.jumpTimer = 2
        self.jumpCount = 0
        self.pos_x = self.pos[0]
        self.pos_y = self.pos[1]

    def movePlayer(self, x, y, ignoreFloor):
        f_y = (g0 * self.mass + y) * dt
        f_x = x * dt
        newX = self.pos_x
        newY = self.pos_y
        self.velocityVector += [f_x/self.mass, f_y/self.mass]
        rect_list = [b.rect for b in walls]
        newX += x * dt
        newY += self.velocityVector.y * dt
        # self.pos_y += self.velocityVector.y * dt
        # self.pos_x += x * dt
        newRect = self.rect
        newRect.center = (newX, self.rect.y)
        if newRect.collidelist(rect_list) == -1:
            self.rect = newRect
            self.pos_x = newX
        newRect.center = (self.rect.x, newY)
        if newRect.collidelist(rect_list) == -1:
            self.rect = newRect
            self.pos_y = newY
        elif self.velocityVector.y < 0:
            self.pos_y = newY
            self.rect = newRect
        else:
            self.velocityVector.y = 0
            self.jumpCount = 0

        # if rect_list[newRect.collidelist(rect_list)].right <= self.rect.left:
        #     self.pos_y = newY
        # if self.rect.center(self.pos_x, self.pos_y):
        self.rect.center = (self.pos_x, self.pos_y)

    def update(self, pressed_keys):
        self.jumpTimer -= dt
        if pressed_keys[K_UP]:
            if self.jumpTimer < 0 and self.jumpCount < 2:
                self.jumpCount += 1
                self.jumpTimer = 3
                self.velocityVector.y = 0
                self.velocityVector.y += -90
                # self.pos_y += self.velocityVector.y * dt
        # if pressed_keys[K_DOWN]:
        #     self.velocityVector.y += 3
        if pressed_keys[K_LEFT]:
            self.movePlayer(-40, 0, False)
        elif pressed_keys[K_RIGHT]:
            self.movePlayer(40, 0, False)
        elif pressed_keys[K_DOWN]:
             self.movePlayer(0, -10, True)
        else:
            self.movePlayer(0,0, False)


class Bot(pygame.sprite.Sprite):
    def __init__(self, shadowBot = False):
        super(Bot, self).__init__()
        if not shadowBot:
            self.original_image = pygame.image.load("Competition/enemy.png")
            self.original_image = pygame.transform.scale(self.original_image, (30, 30))
            self.image = self.original_image
        else:
            self.original_image = pygame.image.load("Competition/Empty.png")
            self.original_image = pygame.transform.scale(self.original_image, (30, 30))
            self.image = self.original_image
        self.rect = self.image.get_rect().move(600, 600)
        self.angle = 0
        self.rotSpeed = 2.5
        self.pos = [600, 600]
        self.velocity = 0.0001
        self.minVelocity = 0.0003
        self.velocityVector = pygame.math.Vector2(0, 0)
        self.mass = 1
        self.jumpTimer = 3
        self.jumpCount = 0
        self.shadow = False
        self.pos_x = self.pos[0]
        self.pos_y = self.pos[1]

    def movePlayer(self, x, y):
        f_y = (g0 * self.mass + y) * dt
        f_x = x * dt
        newX = self.pos_x
        newY = self.pos_y
        self.velocityVector += [f_x / self.mass, f_y / self.mass]
        rect_list = [b.rect for b in walls]
        newX += x * dt
        newY += self.velocityVector.y * dt
        self.jumpTimer -= dt
        if abs(y) > random.uniform(0.5, 2):
            if self.jumpTimer < 0 and self.jumpCount < 1:
                self.jumpCount += 1
                self.jumpTimer = 3
                self.velocityVector.y += -100
        if abs(y) > random.uniform(1.5, 5):
            if self.jumpTimer < 0 and self.jumpCount == 1:
                self.jumpCount += 1
                self.jumpTimer = 3
                self.velocityVector.y += -100

        newRect = self.rect
        newRect.center = (newX, self.rect.y)
        if newRect.collidelist(rect_list) == -1:
            self.rect = newRect
            self.pos_x = newX
        newRect.center = (self.rect.x, newY)
        if newRect.collidelist(rect_list) == -1:
            self.rect = newRect
            self.pos_y = newY
        elif self.velocityVector.y < 0:
            self.pos_y = newY
            self.rect = newRect
        else:
            self.velocityVector.y = 0
            self.jumpCount = 0

        if self.pos_y < 20:
            self.pos_y = 20
            self.velocityVector.y = 20
        self.rect.center = (self.pos_x, self.pos_y)

    def botUpdate(self, x, y):
        inputs = []
        hiddenLayer = []
        hiddenLayer.append(x)
        hiddenLayer.append(y)
        outputs = [0] * 2
        inputs.append(self.pos_x - player.pos_x)
        inputs.append(self.pos_y - player.pos_y)
        outputs[0] = inputs[0] * x / 6
        outputs[1] = inputs[1] * y / 30
        # inputs.append(self.pos_x - player.pos_x)
        # inputs.append(self.pos_y - player.pos_y)
        # inputs.append(player.pos_x)
        # inputs.append(player.pos_y)
        # outputs = [0] * 2

        # for input in inputs:
        #     hiddenLayer[0] *= inputs[inputs.index(input)]
        #     hiddenLayer[1] *= inputs[inputs.index(input)]

        self.movePlayer(outputs[0], outputs[1])
