import pygame
import math
import numpy
import random
import Main
import World
import copy

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

density = 1.225
g0 = 30

popSize = (10, 2)
weights = numpy.random.uniform(-1, 0.2, size=popSize)
bots = []

walls = []

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.original_image = pygame.image.load("player.png")
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

    def movePlayer(self, x, y):
        f_y = (g0 * self.mass) * dt
        f_x = x * dt
        newX = self.pos_x
        newY = self.pos_y
        self.velocityVector += [f_x / self.mass, f_y / self.mass]
        rect_list = [b.rect for b in walls]
        newX += x * dt
        newY += self.velocityVector.y * dt
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
        elif pressed_keys[K_DOWN]:
             self.movePlayer(0, -10)
        else:
            self.movePlayer(0,0)


class Bot(pygame.sprite.Sprite):
    def __init__(self, shadowBot = False):
        super(Bot, self).__init__()
        if not shadowBot:
            self.original_image = pygame.image.load("enemy.png")
            self.original_image = pygame.transform.scale(self.original_image, (30, 30))
            self.image = self.original_image
        else:
            self.original_image = pygame.image.load("Empty.png")
            self.original_image = pygame.transform.scale(self.original_image, (30, 30))
            self.image = self.original_image
        self.rect = self.image.get_rect().move(600, 600)
        self.angle = 0
        self.rotSpeed = 2.5
        self.pos = [1400, 200]
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
        f_y = (g0 * self.mass) * dt
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
            self.jumpTimer = 3
            self.velocityVector.y = 50
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


def mutate(receivedWeights, largeMutation):
    newWeights = copy.deepcopy(receivedWeights)
    maxMutation = 0.2
    if largeMutation:
        maxMutation = 0.8
    for i, indvWeight in enumerate(newWeights):
        newWeights[i] += random.uniform(-maxMutation + generation/100, maxMutation - generation/100)
    return newWeights


player = Player()
score = 0
weights = numpy.random.uniform(0, 1, size=popSize)

for generation in range(50):
    walls = Main.walls
    decorations = Main.decorations
    screen = Main.screen
    rect_list = [b.rect for b in walls]
    food = World.instantiateFood()
    while food.rect.collidelist(rect_list) != -1:
        food.kill()
        food = World.instantiateFood()
    bots = []
    for instance in weights:
        if numpy.where(weights == instance)[0][0] == 0:
            bot = Bot(False)
        else:
            bot = Bot(True)
            bot.shadow = True
        # bot.bot = True
        bots.append(bot)

    fitness = [0] * 10

    running = True
    clock = pygame.time.Clock()
    # dt = clock.tick(60)/1000
    dt = 0.1
    startTime = pygame.time.get_ticks()

    while running:
        screen.fill((111, 177, 250))
        for wall in walls:
            screen.blit(wall.image, wall.rect)
        for decoration in decorations:
            screen.blit(decoration.image, decoration.rect)
        screen.blit(food.image, food.rect)
        for bot in bots:
            botWeights = weights[bots.index(bot)]
            bot.botUpdate(botWeights[0], botWeights[1])
            screen.blit(bot.image, bot.rect)
            fitness[bots.index(bot)] += 1 / ((pygame.math.Vector2(player.pos_x, player.pos_y).distance_to((bot.pos_x, bot.pos_y))) ** 2) / 1000
            if not bot.shadow:
                if bot.rect.colliderect(player.rect):
                    player.kill()
                    screen.blit(player.image, player.rect)
                    pygame.display.flip()
                    pygame.quit()
                    # exit()
        # if pygame.time.get_ticks() - startTime >= (10000 + generation*200):
        if score >= 5:
            score = 0
            highestFitness = 0
            bestGenes = []
            bestBot = 0
            for bot in bots:
                fitness[bots.index(bot)] += 1/((pygame.math.Vector2(player.pos_x, player.pos_y).distance_to((bot.pos_x, bot.pos_y)))**2)
                botFitness = fitness[bots.index(bot)]
                if botFitness > highestFitness:
                    bestBot = bots.index(bot)
                    highestFitness = fitness[bots.index(bot)]
                    bestGenes = copy.deepcopy(weights[bestBot])
            for i, weight in enumerate(weights):
                weights[i] = copy.deepcopy(mutate(bestGenes, True))
            break

        if (pygame.time.get_ticks() - startTime) % 3000 <= 20:
            print("Huh: " + str(pygame.time.get_ticks() - startTime))
            highestFitness = 0
            bestBot = 0
            for bot in bots:
                fitness[bots.index(bot)] += 1/((pygame.math.Vector2(player.pos_x, player.pos_y).distance_to((bot.pos_x, bot.pos_y)))**2)
                botFitness = fitness[bots.index(bot)]
                if botFitness > highestFitness:
                    bestBot = bots.index(bot)
                    highestFitness = fitness[bots.index(bot)]
            i = 0
            for weight in weights:
                weights[i] = mutate(weights[bestBot], False)
                i += 1

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        if player.rect.colliderect(food.rect):
            score += 1
            food.kill()
            food = World.instantiateFood()
            while food.rect.collidelist(rect_list) != -1:
                food.kill()
                food = World.instantiateFood()

        screen.blit(player.image, player.rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    exit()

            elif event.type == QUIT:
                running = False
                exit()
