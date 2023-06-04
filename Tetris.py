import random

import numpy
import pygame
import numpy as np

pygame.init()
clock = pygame.time.Clock()

numberOfRows = 20
numberOfColumns = 10
brickSize = 40
currentTetromino = None
dt = 150
timePassed = 0
grid = np.array([[8] * (numberOfColumns + 2)])
grid = np.append(grid, [[8] + [0] * numberOfColumns + [8]] * numberOfRows, axis=0)
grid = np.append(grid, [[8] * (numberOfColumns + 2)], axis=0)
# print(grid)
# grid = np.random.randint(0, 8, (numberOfRows, numberOfColumns))
# grid = np.array([[8] * numberOfColumns] + [[8] * numberOfColumns])
bricks = [np.array([[1, 1, 1, 1]]), np.array([[2, 0, 0], [2, 2, 2]]), np.array([[0, 0, 3], [3, 3, 3]]), np.array([[4, 4], [4, 4]]), np.array([[0, 5, 5], [5, 5, 0]]), np.array([[0, 6, 0], [6, 6, 6]]), np.array([[7, 7, 0], [0, 7 ,7]])]

colors = {
    1: "aqua",
    2: "blue",
    3: "orange",
    4: "yellow",
    5: "green",
    6: "purple",
    7: "red",
    8: "grey"
}

screenWidth = brickSize * (numberOfColumns + 2)
screenHeight = brickSize * (numberOfRows + 2)

screen = pygame.display.set_mode((screenWidth, screenHeight))

class tetromino():
    def __init__(self, shape):
        super(tetromino, self).__init__()
        self.xPos = 3
        self.yPos = 1
        self.shape = shape

def drawGrid():
    screen.fill("black")
    # for k in range(0, numberOfColumns + 2):
    #     pygame.draw.rect(screen, colors[8], pygame.Rect(k * brickSize, 0, brickSize - 1, brickSize - 1))
    #     pygame.draw.rect(screen, colors[8], pygame.Rect(k * brickSize, (numberOfRows + 1) * brickSize, brickSize - 1, brickSize - 1))
    # for l in range(1, numberOfRows + 1):
    #     pygame.draw.rect(screen, colors[8], pygame.Rect(0, l * brickSize, brickSize - 1, brickSize - 1))
    #     pygame.draw.rect(screen, colors[8], pygame.Rect((numberOfColumns + 1) * brickSize, l * brickSize, brickSize - 1, brickSize - 1))
    j = 0
    for row in grid:
        i = 0
        for brick in row:
            if brick != 0:
                # pygame.draw.rect(screen, colors[brick], )
                pygame.draw.rect(screen, colors[brick], pygame.Rect(i * brickSize, j * brickSize, brickSize - 1, brickSize - 1))
            i += 1
        j += 1
    # screen.fill("black", (0, 0, 700, 1000))

def drawCurrent(tetromino):
    rows, columns = tetromino.shape.shape
    for row in range(0, rows):
        for col in range(0, columns):
            if tetromino.shape[row][col] != 0:
                pygame.draw.rect(screen, colors[tetromino.shape[row][col]], pygame.Rect(tetromino.xPos * brickSize + col * brickSize, tetromino.yPos * brickSize + row * brickSize, brickSize - 1, brickSize - 1))

def checkCollision(tetromino, dx = 0, dy = 0):
    rows, cols = tetromino.shape.shape
    collision = False
    if dx == -1 and tetromino.xPos == 1:
        return True
    if dx == 1 and tetromino.xPos * brickSize == screenWidth - brickSize - (cols)*brickSize:
        return True
    if dy == 1 and tetromino.yPos * brickSize == screenHeight - brickSize - (rows)*brickSize:
        return True
    for row in range(0, rows):
        for col in range(0, cols):
            if tetromino.shape[row][col] != 0:
                if grid[tetromino.yPos + row + dy][tetromino.xPos + col] != 0:
                    collision = True
                if grid[tetromino.yPos + row][tetromino.xPos + col + dx] != 0:
                    collision = True
    return collision

timePassed = pygame.time.get_ticks()
running = True
while running:
    if currentTetromino == None:
        currentTetromino = tetromino(random.choice(bricks))
    drawGrid()
    drawCurrent(currentTetromino)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not checkCollision(currentTetromino, -1, 0):
                    currentTetromino.xPos -= 1
            elif event.key == pygame.K_RIGHT:
                if not checkCollision(currentTetromino, 1, 0):
                    currentTetromino.xPos += 1
            elif event.key == pygame.K_UP:
                currentTetromino.shape = np.rot90(currentTetromino.shape)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    if pygame.time.get_ticks() > timePassed + dt:
        if not checkCollision(currentTetromino, 0, 1):
            currentTetromino.yPos += 1
        else:
            rows, columns = currentTetromino.shape.shape
            for row in range(0, rows):
                for col in range(0, columns):
                    if currentTetromino.shape[row][col] != 0:
                        grid[int(currentTetromino.yPos + row)][int(currentTetromino.xPos + col)] = currentTetromino.shape[row][col]
            currentTetromino = tetromino(random.choice(bricks))
        timePassed = pygame.time.get_ticks()


        rowIndex = 0
        newGrid = grid
        for row in grid:
            isFull = True
            if rowIndex == 0 or rowIndex == numberOfRows + 1:
                isFull = False
            for brick in row:
                if brick == 0:
                    isFull = False
            # if not isFull:
            #     np.append(newGrid, grid[rowIndex])
            if isFull:
                newGrid = np.delete(newGrid, rowIndex, axis=0)
                newGrid = np.insert(newGrid, 1, np.array([8] + [0] * numberOfColumns + [8]), 0)
                isFull = False
            rowIndex += 1
        grid = newGrid

    pygame.display.flip()

    clock.tick(60)

pygame.quit()