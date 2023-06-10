import pygame
import math
import numpy
import random

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
g0 = 30

popSize = (20, 2)
weights = numpy.random.uniform(-1, 1, size=popSize)
bots = []

walls = []

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super(Wall, self).__init__()
        if type == "Side":
            self.original_image = pygame.image.load("Tile_2.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 128))
            self.original_image = pygame.transform.flip(self.original_image, True, False)
        elif type == "Side 2":
            self.original_image = pygame.image.load("Tile_2.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 128))
        elif type == "Floor":
            self.original_image = pygame.image.load("Tile_1.png")
            self.original_image = pygame.transform.scale(self.original_image, (128, 70))
        self.image = self.original_image
        self.rect = self.image.get_rect().move(x, y)

class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Food, self).__init__()
        self.original_image = pygame.image.load("apple.png").convert()
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.image = self.original_image
        self.rect = self.image.get_rect().move(x, y)

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Door, self).__init__()
        self.original_image = pygame.image.load("door.png").convert()
        self.original_image = pygame.transform.scale(self.original_image, (120, 80))
        self.image = self.original_image
        self.rect = self.image.get_rect().move(x, y)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.original_image = pygame.image.load("ghost.jpg").convert()
        self.original_image = pygame.transform.scale(self.original_image, (30, 30))
        self.image = self.original_image
        self.bot = False
        self.rect = self.image.get_rect().move(800, 100)
        self.pos = [800, 100]
        self.velocityVector = pygame.math.Vector2(0,0)
        self.velocity = 0.02
        self.mass = 1
        self.jump = False
        self.jumpTimer = 2
        self.jumpCount = 0
        self.pos_x = self.pos[0]
        self.pos_y = self.pos[1]

    def movePlayer(self, x, y):
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
            self.movePlayer(-40, 0)
        elif pressed_keys[K_RIGHT]:
            self.movePlayer(40, 0)
        else:
            self.movePlayer(0,0)


class Bot(pygame.sprite.Sprite):
    def __init__(self, shadowBot = False):
        super(Bot, self).__init__()
        if not shadowBot:
            self.original_image = pygame.image.load("ghost.jpg").convert()
            self.original_image = pygame.transform.scale(self.original_image, (30, 30))
            self.image = self.original_image
        else:
            self.original_image = pygame.image.load("apple.png").convert()
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
            if self.rect.top > rect_list[newRect.collidelist(rect_list)].bottom:
                self.pos_y = newY
                self.rect = newRect
        else:
            self.velocityVector.y = 0
            self.jumpCount = 0

        self.rect.center = (self.pos_x, self.pos_y)

    def botUpdate(self, x, y):
        inputs = []
        hiddenLayer = []
        hiddenLayer.append(x)
        hiddenLayer.append(y)
        outputs = [0] * 2
        inputs.append(self.pos_x - door.rect.centerx)
        inputs.append(self.pos_y - door.rect.centery)
        outputs[0] = inputs[0] * x / 10
        outputs[1] = inputs[1] * y / 50
        # inputs.append(self.pos_x - player.pos_x)
        # inputs.append(self.pos_y - player.pos_y)
        # inputs.append(player.pos_x)
        # inputs.append(player.pos_y)
        # outputs = [0] * 2

        # for input in inputs:
        #     hiddenLayer[0] *= inputs[inputs.index(input)]
        #     hiddenLayer[1] *= inputs[inputs.index(input)]

        self.movePlayer(outputs[0], outputs[1])


def mutate(receivedWeights, largeMutation):
    newWeights = receivedWeights
    maxMutation = 1
    if largeMutation:
        maxMutation = 2
    i = 0
    for indvWeight in newWeights:
        newWeights[i] += random.uniform(-maxMutation + generation/100, maxMutation - generation/100)
        i += 1
    return newWeights

def instantiateFood():
    xPos = random.randint(600, 800)
    yPos = random.randint(200, 420)
    food = Food(xPos, yPos)
    # screen.blit(food.image, food.rect)
    return food

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

score = 0

weights = numpy.random.uniform(0, 1, size=popSize)
font = pygame.font.Font(None, 30)
text = font.render(str("Empty"), True, (0, 0, 0))

for generation in range(50):
    player = Player()
    door = Door(100, 180)
    walls = []
    for i in range(11):
        walls.append(Wall(i*128, 650, "Floor"))
    for j in range(4):
        walls.append(Wall(888 + j*128, 450, "Floor"))
    for k in range(4):
        walls.append(Wall(k*128, 250, "Floor"))
    for x in range(10):
        walls.append(Wall(0, x*128, "Side"))
    for y in range(10):
        walls.append(Wall(1336, y*128, "Side 2"))
    for z in range(11):
        walls.append(Wall(z*128, 0, "Floor"))
    food = instantiateFood()
    bots = []
    for instance in weights:
        if numpy.where(weights == instance)[0][0] == 0:
            bot = Bot(False)
        else:
            bot = Bot(True)
            bot.shadow = True
        # bot.bot = True
        bots.append(bot)

    fitness = [0] * 20

    running = True
    clock = pygame.time.Clock()
    # dt = clock.tick(60)/1000
    dt = 0.1
    startTime = pygame.time.get_ticks()
    i = 0
    while running:
        i += 1
        screen.fill((255, 255, 255))
        screen.blit(door.image, door.rect)
        for wall in walls:
            screen.blit(wall.image, wall.rect)
        screen.blit(food.image, food.rect)
        for bot in bots:
            botWeights = weights[bots.index(bot)]
            bot.botUpdate(botWeights[0], botWeights[1])
            screen.blit(bot.image, bot.rect)
            # fitness[bots.index(bot)] = 1 / ((pygame.math.Vector2(player.pos_x, player.pos_y).distance_to((bot.pos_x, bot.pos_y))) ** 2) / 10
            if not bot.shadow:
                if bot.rect.colliderect(player.rect):
                    player.kill()
                    screen.blit(player.image, player.rect)
                    pygame.display.flip()
                    pygame.quit()
                    # exit()
            if bot.rect.colliderect(door.rect):
                bot.kill()
        # if pygame.time.get_ticks() - startTime >= (10000 + generation*200):
        if player.rect.colliderect(door.rect):
            player.kill()
            score = 0
            highestFitness = 0
            bestBot = 0
            for bot in bots:
                fitness[bots.index(bot)] += 1/(pygame.math.Vector2(player.pos_x, player.pos_y).distance_to((door.rect.centerx, door.rect.centery - 20)))*100
                botFitness = fitness[bots.index(bot)]
                if botFitness > highestFitness:
                    text = font.render(str(weights[bots.index(bot)]), True, (0,0,0))
                    bestBot = bots.index(bot)
                    highestFitness = fitness[bots.index(bot)]
            i = 0
            for weight in weights:
                weights[i] = mutate(weights[bestBot], True)
                i += 1
            break

        if i % 100 == 0:
            print("Huh: " + str(pygame.time.get_ticks() - startTime))
            highestFitness = 0
            bestBot = 0
            for bot in bots:
                fitness[bots.index(bot)] += 1/(pygame.math.Vector2(player.pos_x, player.pos_y).distance_to((door.rect.centerx, door.rect.centery - 20)))
                botFitness = fitness[bots.index(bot)]
                if botFitness > highestFitness:
                    text = font.render(str(weights[bots.index(bot)]), True, (0,0,0))
                    bestBot = bots.index(bot)
                    highestFitness = fitness[bots.index(bot)]
            i = 0
            print(highestFitness)
            for weight in weights:
                weights[i] = mutate(weights[bestBot], False)
                i += 1

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        if player.rect.colliderect(food.rect):
            score += 1
            food.kill()
            food = instantiateFood()

        screen.blit(player.image, player.rect)

        text2 = font.render(str(score), True, (0, 0, 0))
        screen.blit(text, [10, 10])
        screen.blit(text2, [10, 30])

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    exit()

            elif event.type == QUIT:
                running = False
                exit()
