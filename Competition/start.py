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
g0 = 9.81

popSize = (10, 2)
weights = numpy.random.uniform(0, 1, size=popSize)
bots = []


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Food, self).__init__()
        self.original_image = pygame.image.load("apple.png").convert()
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.image = self.original_image
        self.rect = self.image.get_rect().move(x, y)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.original_image = pygame.image.load("ghost.jpg").convert()
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.image = self.original_image
        self.bot = False
        self.rect = self.image.get_rect().move(100, 100)
        self.angle = 0
        self.rotSpeed = 2.5
        self.pos = [100, 100]
        self.velocity = 0.2
        self.botVelocity = 0.0005
        self.pos_x = self.pos[0]
        self.pos_y = self.pos[1]

    def movePlayer(self, x, y):
        if self.bot:
            self.pos_x += self.botVelocity * x * dt
            self.pos_y += self.botVelocity * y * dt
        else:
            self.pos_x += self.velocity * x * dt
            self.pos_y += self.velocity * y * dt

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.movePlayer(0, -1)
        if pressed_keys[K_DOWN]:
            self.movePlayer(0, 1)

        if pressed_keys[K_LEFT]:
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            x, y = self.rect.center
            self.movePlayer(-1, 0)
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
        if pressed_keys[K_RIGHT]:
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.movePlayer(1, 0)
            x, y = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

        self.rect.center = (self.pos_x, self.pos_y)

class Bot(pygame.sprite.Sprite):
    def __init__(self):
        super(Bot, self).__init__()
        self.original_image = pygame.image.load("ghost.jpg").convert()
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.image = self.original_image
        self.rect = self.image.get_rect().move(600, 600)
        self.angle = 0
        self.rotSpeed = 2.5
        self.pos = [600, 600]
        self.velocity = 0.0006
        self.minVelocity = 0.0003
        self.pos_x = self.pos[0]
        self.pos_y = self.pos[1]

    def movePlayer(self, x, y):
        self.pos_x += self.velocity * x * dt
        self.pos_y += self.velocity * y * dt

    def botUpdate(self, x, y):
        inputs = []
        hiddenLayer = []
        hiddenLayer.append(x)
        hiddenLayer.append(y)
        outputs = [0] * 2
        inputs.append(self.pos_x - player.pos_x)
        inputs.append(self.pos_y - player.pos_y)
        outputs[0] += inputs[0] * x
        outputs[1] += inputs[1] * y
        # inputs.append(self.pos_x - player.pos_x)
        # inputs.append(self.pos_y - player.pos_y)
        # inputs.append(player.pos_x)
        # inputs.append(player.pos_y)
        # outputs = [0] * 2

        # for input in inputs:
        #     hiddenLayer[0] *= inputs[inputs.index(input)]
        #     hiddenLayer[1] *= inputs[inputs.index(input)]

        self.movePlayer(outputs[0], outputs[1])
        self.rect.center = (self.pos_x, self.pos_y)


def mutate(receivedWeights):
    for indvWeight in receivedWeights:
        receivedWeights[numpy.where(receivedWeights == indvWeight)] += random.uniform(-0.3 + generation/100, 0.3 - generation/100)
    return receivedWeights

def instantiateFood():
    xPos = random.randint(0, 1400)
    yPos = random.randint(0, 720)
    food = Food(xPos, yPos)
    # screen.blit(food.image, food.rect)
    return food

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player()

score = 0

weights = numpy.random.uniform(0, 1, size=popSize)

for generation in range(50):
    food = instantiateFood()
    bots = []
    for instance in weights:
        bot = Bot()
        # bot.bot = True
        bots.append(bot)

    fitness = [0] * 10

    running = True
    clock = pygame.time.Clock()
    dt = clock.tick(60)
    startTime = pygame.time.get_ticks()

    while running:
        screen.fill((0, 0, 0))
        screen.blit(food.image, food.rect)
        for bot in bots:
            botWeights = weights[bots.index(bot)]
            bot.botUpdate(botWeights[0], botWeights[1])
            screen.blit(bot.image, bot.rect)
            if bot.rect.colliderect(player.rect):
                player.kill()
                screen.blit(player.image, player.rect)
                pygame.display.flip()
                pygame.quit()
                # exit()
            # fitness[bots.index(bot)] = 1/(abs(player.pos_x - bot.pos_x) + abs(player.pos_y - bot.pos_y))

        if pygame.time.get_ticks() - startTime >= (3000 + generation*200):
            highestFitness = 0
            bestBot = 0
            for bot in bots:
                fitness[bots.index(bot)] = 1/((pygame.math.Vector2(player.pos_x, player.pos_y).distance_to((bot.pos_x, bot.pos_y)))**2)
                botFitness = fitness[bots.index(bot)]
                if botFitness > highestFitness:
                    bestBot = bots.index(bot)
                    highestFitness = fitness[bots.index(bot)]
            for weight in weights:
                weights[numpy.argwhere(weights == weight)[0]] = mutate(weights[bestBot])
            break

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        if player.rect.colliderect(food.rect):
            score += 1
            food.kill()
            food = instantiateFood()

        screen.blit(player.image, player.rect)

        font = pygame.font.Font(None, 30)
        text = font.render(str(weights), True, (255, 255, 255))
        text2 = font.render(str(score), True, (255, 255, 255))
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
