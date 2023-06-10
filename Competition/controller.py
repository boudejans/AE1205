import random
import copy
import numpy as np
import pygame
import main
import world

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Constants
density = 1.225
g0 = 30
timeBetweenMutations = 4000
timeSinceLastMutation = 0

font = pygame.font.Font(None, 50)

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
        # Calculate the forces and new velocity
        f_y = (g0 * self.mass) * dt
        f_x = x * dt
        newX = self.pos_x
        newY = self.pos_y
        self.velocityVector += [f_x / self.mass, f_y / self.mass]
        rect_list = [b.rect for b in walls]
        newX += x * dt
        newY += self.velocityVector.y * dt

        # Create a new rect object with the change in position. If the new rect does not collide with walls, move player
        newRect = self.rect
        newRect.center = (newX, self.rect.y)
        if newRect.collidelist(rect_list) == -1:
            self.rect = newRect
            self.pos_x = newX
        newRect.center = (self.rect.x, newY)
        if newRect.collidelist(rect_list) == -1:
            self.rect = newRect
            self.pos_y = newY
        elif self.velocityVector.y <= 0:  # If the player is moving upwards, move through the platforms
            self.velocityVector.y -= 1.5
            self.pos_y = newY
            self.rect = newRect
        elif rect_list[newRect.collidelist(rect_list)].y >= self.rect.y:  # Player above object, so ground
            self.velocityVector.y = 0
            self.jumpCount = 0
        elif rect_list[newRect.collidelist(rect_list)].y <= self.rect.y:  # Player below object, so a wall
            self.pos_y = newY
            self.rect = newRect

        self.rect.center = (self.pos_x, self.pos_y)

    def update(self, pressed_keys):
        self.jumpTimer -= dt
        if pressed_keys[K_UP]:
            if self.jumpTimer < 0 and self.jumpCount < 2:
                self.jumpCount += 1
                self.jumpTimer = 3
                self.velocityVector.y = 0
                self.velocityVector.y -= 100
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


# Class object for the AI
class Bot(pygame.sprite.Sprite):
    def __init__(self, shadowBot = False):
        super(Bot, self).__init__()
        # Check if the AI is a shadow bot (a bot just for training which is not visible)
        if not shadowBot:
            self.original_image = pygame.image.load("enemy.png")
            self.original_image = pygame.transform.scale(self.original_image, (30, 30))
            self.image = self.original_image
            self.shadow = False
        else:
            self.original_image = pygame.image.load("Empty.png")
            self.original_image = pygame.transform.scale(self.original_image, (30, 30))
            self.image = self.original_image
            self.shadow = True
        self.rect = self.image.get_rect().move(600, 600)
        # Constants
        self.pos = [1800, 300]
        self.velocity = 0.0001
        self.maxVelocity = 200
        self.velocityVector = pygame.math.Vector2(0, 0)
        self.mass = 1
        self.jumpTimer = 3
        self.jumpCount = 0
        self.pos_x = self.pos[0]
        self.pos_y = self.pos[1]

    # Calculate the forces, new velocity and update the position of the bot
    def moveBot(self, x, y):
        f_y = (g0 * self.mass) * dt
        f_x = x * dt
        newX = self.pos_x
        newY = self.pos_y
        self.velocityVector += [f_x / self.mass, f_y / self.mass]
        if x > self.maxVelocity:
            x = self.maxVelocity
        elif x < -self.maxVelocity:
            x = -self.maxVelocity
        newX += x * dt
        newY += self.velocityVector.y * dt
        self.jumpTimer -= dt
        if y > random.uniform(0.5, 2):
            if self.jumpTimer < 0 and self.jumpCount < 1:
                self.jumpCount += 1
                self.jumpTimer = 3
                self.velocityVector.y -= 100
        if y > random.uniform(1.5, 5):
            if self.jumpTimer < 0 and self.jumpCount == 1:
                self.jumpCount += 1
                self.jumpTimer = 3
                self.velocityVector.y -= 100

        # Check if the new position of the bot will collide with any wall
        rect_list = [b.rect for b in walls]
        newRect = self.rect
        newRect.center = (newX, self.rect.y)
        if newRect.collidelist(rect_list) == -1:
            self.rect = newRect
            self.pos_x = newX
        newRect.center = (self.rect.x, newY)
        if newRect.collidelist(rect_list) == -1:
            self.rect = newRect
            self.pos_y = newY
        elif self.velocityVector.y <= 0:
            self.velocityVector.y -= 1.5
            self.pos_y = newY
            self.rect = newRect
        elif rect_list[newRect.collidelist(rect_list)].y >= self.rect.y:  # Bot above object, so ground
            self.velocityVector.y = 0
            self.jumpCount = 0
        elif rect_list[newRect.collidelist(rect_list)].y <= self.rect.y:  # Bot below object, so a wall
            self.pos_y = newY
            self.rect = newRect

        # An invisible border at the top of the level to prevent the bot from leaving
        if self.pos_y < 10:
            self.pos_y = 10
            self.jumpTimer = 3
            self.velocityVector.y = 20
        self.rect.center = (self.pos_x, self.pos_y)

    # Give the bot the inputs and calculate its outputs to move the bot
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

        self.moveBot(outputs[0], outputs[1])

# Mutate a set of weights
def mutate(receivedWeights, largeMutation):
    newWeights = copy.deepcopy(receivedWeights)
    maxMutation = 0.4
    # If the player's score reaches a multiple of 5, mutate the weights a larger amount
    if largeMutation:
        maxMutation = 0.8
    # Mutate each individual weight by a random amount, which decreases with later generations
    for i, indvWeight in enumerate(newWeights):
        newWeights[i] += random.uniform(-maxMutation + generation/50, maxMutation - generation/50)
    return newWeights

# Create an instance of the player
player = Player()

# Get the level objects from the main script
walls = main.walls
decorations = main.decorations
screen = main.screen

# Variables
score = 0  # Score since last mutation
totalScore = 0  # The total score of the player
popSize = (10, 2)  # The population size, number of AI and number of weights
weights = np.random.uniform(-0.5, 0.5, size=popSize)  # Create the list of weights
isDead = False
for generation in range(50):
    # If the player was caught, wait till 'r' is pressed to reset the game or 'esc' to quit the game
    while isDead:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset all game variables and create a new player object
                    score = 0
                    totalScore = 0
                    weights = np.random.uniform(-0.5, 0.5, size=popSize)
                    player = Player()
                    isDead = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()

    # Create a piece of food, makes sure that the food object does not spawn within a wall
    rect_list = [b.rect for b in walls]
    food = world.instantiateFood()
    while food.rect.collidelist(rect_list) != -1:
        food.kill()
        food = world.instantiateFood()

    # Create a bot for all weights, make the first bot a shadow bot
    bots = []
    for i, instance in enumerate(weights):
        if i == 0:
            bot = Bot(False)
        else:
            bot = Bot(True)
        bots.append(bot)
    fitness = [0] * popSize[0]  # A list of fitness, a score for each bot for how well it is performing
    running = True
    clock = pygame.time.Clock()
    dt = 1/clock.tick(60)

    while running:
        # Show the game level
        screen.fill((111, 177, 250))
        for wall in walls:
            screen.blit(wall.image, wall.rect)
        for decoration in decorations:
            screen.blit(decoration.image, decoration.rect)
        screen.blit(food.image, food.rect)

        # Update all bots, add a fitness amount to each of the bots.
        # The smaller the distance to the player, the larger the fitness gained.
        for bot in bots:
            botWeights = weights[bots.index(bot)]
            bot.botUpdate(botWeights[0], botWeights[1])
            screen.blit(bot.image, bot.rect)
            fitness[bots.index(bot)] += 1 / ((pygame.math.Vector2(player.pos_x, player.pos_y).distance_to((bot.pos_x, bot.pos_y))) ** 2) / 200
            # If the actual enemy touches the player, it is game-over
            if not bot.shadow:
                if bot.rect.colliderect(player.rect):
                    # Delete the player, create the game-over screen from the main menu module and display the score
                    player.kill()
                    player = Player()
                    pygame.display.flip()
                    import mainMenu
                    mainMenu.playerDied()
                    text = font.render("Final Score: " + str(totalScore), True, (51, 29, 10))
                    screen.blit(text, (main.SCREEN_WIDTH / 2 - 110, main.SCREEN_HEIGHT / 2 + 100))
                    running = False
                    isDead = True

        # If the player reaches a score of 5, mutate all bot weights and reset the score counter
        if score >= 5:
            score = 0
            highestFitness = 0
            bestGenes = []
            bestBot = 0
            # Go through each bot and add a final fitness amount based on the distance to the player
            for bot in bots:
                fitness[bots.index(bot)] += 1/((pygame.math.Vector2(player.pos_x, player.pos_y).distance_to((bot.pos_x, bot.pos_y)))**2)
                botFitness = fitness[bots.index(bot)]
                # Find the bot with the best genes
                if botFitness > highestFitness:
                    bestBot = bots.index(bot)
                    highestFitness = fitness[bots.index(bot)]
                    bestGenes = copy.deepcopy(weights[bestBot])
            # The new weights become mutated versions of the best weights from the previous generation
            for i, weight in enumerate(weights):
                weights[i] = copy.deepcopy(mutate(bestGenes, True))
            break  # Go to the next generation

        # If timeBetweenMutations has passed, the bots get a small mutation
        if pygame.time.get_ticks() >= timeSinceLastMutation + timeBetweenMutations:
            highestFitness = 0
            bestBot = 0
            for bot in bots:
                fitness[bots.index(bot)] += 1/((pygame.math.Vector2(player.pos_x, player.pos_y).distance_to((bot.pos_x, bot.pos_y)))**2)
                botFitness = fitness[bots.index(bot)]
                if botFitness > highestFitness:
                    bestBot = bots.index(bot)
                    highestFitness = fitness[bots.index(bot)]
            for i, weight in enumerate(weights):
                weights[i] = mutate(weights[bestBot], False)
            timeSinceLastMutation = pygame.time.get_ticks()

        # Update the player based on the key presses
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        # If the player touches a piece of food, score increases by one and a new food object is created
        if player.rect.colliderect(food.rect):
            score += 1
            totalScore += 1
            food.kill()
            food = world.instantiateFood()
            while food.rect.collidelist(rect_list) != -1:
                food.kill()
                food = world.instantiateFood()

        # Show the score and the player itself
        text = font.render("Score: " + str(totalScore), True, (51, 29, 10))
        screen.blit(text, (70, 10))
        screen.blit(player.image, player.rect)
        pygame.display.flip()

        # Check for any quit event
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    exit()

            elif event.type == QUIT:
                running = False
                exit()
