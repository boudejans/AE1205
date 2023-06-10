import random

import numpy
import pygame
import numpy as np

pygame.init()
clock = pygame.time.Clock()

# Constants
numberOfRows = 20
numberOfColumns = 10
brickSize = 40
currentTetromino = None
dt = 300
timePassed = 0

grid = np.array([[8] * (numberOfColumns + 2)])
grid = np.append(grid, [[8] + [0] * numberOfColumns + [8]] * numberOfRows, axis=0)
grid = np.append(grid, [[8] * (numberOfColumns + 2)], axis=0)

# All possible bricks and colors
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

# Object for active tetromino
class tetromino():
    def __init__(self, shape):
        super(tetromino, self).__init__()
        self.xPos = 3
        self.yPos = 1
        self.shape = shape

# Draw all stationary blocks
def drawGrid():
    screen.fill("black")
    j = 0
    for row in grid:
        i = 0
        for brick in row:
            if brick != 0:
                pygame.draw.rect(screen, colors[brick], pygame.Rect(i * brickSize, j * brickSize, brickSize - 1, brickSize - 1))
            i += 1
        j += 1

# Draw the active tetromino
def drawCurrent(tetromino):
    rows, columns = tetromino.shape.shape
    for row in range(0, rows):
        for col in range(0, columns):
            if tetromino.shape[row][col] != 0:
                pygame.draw.rect(screen, colors[tetromino.shape[row][col]], pygame.Rect(tetromino.xPos * brickSize + col * brickSize, tetromino.yPos * brickSize + row * brickSize, brickSize - 1, brickSize - 1))

# Check for a collision for a given tetromino in a given direction dx or dy
def checkCollision(tetromino, isCopy, dx = 0, dy = 0):
    rows, cols = tetromino.shape.shape
    # if isCopy and tetromino.xPos * brickSize >= screenWidth - (cols - 1)*brickSize:
    #     return True

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
                    return True
                if grid[tetromino.yPos + row][tetromino.xPos + col + dx] != 0:
                    return True

timePassed = pygame.time.get_ticks()
running = True
while running:
    if currentTetromino == None:
        currentTetromino = tetromino(random.choice(bricks))
    drawGrid()
    drawCurrent(currentTetromino)

    # Handle keypresses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_LEFT:
                if not checkCollision(currentTetromino, False, -1, 0):
                    currentTetromino.xPos -= 1
            elif event.key == pygame.K_RIGHT:
                if not checkCollision(currentTetromino, False, 1, 0):
                    currentTetromino.xPos += 1
            elif event.key == pygame.K_UP:
                tetrominoCopy = currentTetromino
                tetrominoCopy.shape = np.rot90(currentTetromino.shape)
                if checkCollision(tetrominoCopy, True, 0, 0):
                    currentTetromino.shape = np.rot90(currentTetromino.shape)
            elif event.key == pygame.K_DOWN:
                # Teleport down
                falling = True
                while falling:
                    if not checkCollision(currentTetromino, False, 0, 1):
                        currentTetromino.yPos += 1
                    else:
                        rows, columns = currentTetromino.shape.shape
                        for row in range(0, rows):
                            for col in range(0, columns):
                                if currentTetromino.shape[row][col] != 0:
                                    grid[int(currentTetromino.yPos + row)][int(currentTetromino.xPos + col)] = currentTetromino.shape[row][col]
                        currentTetromino = tetromino(random.choice(bricks))
                        falling = False

    # If dt time has passed, drop the current tetromino by one
    if pygame.time.get_ticks() > timePassed + dt:
        if not checkCollision(currentTetromino, False, 0, 1):
            currentTetromino.yPos += 1
        else:
            rows, columns = currentTetromino.shape.shape
            for row in range(0, rows):
                for col in range(0, columns):
                    if currentTetromino.shape[row][col] != 0:
                        grid[int(currentTetromino.yPos + row)][int(currentTetromino.xPos + col)] = currentTetromino.shape[row][col]
            currentTetromino = tetromino(random.choice(bricks))
            if checkCollision(currentTetromino, False):
                running = False
        timePassed = pygame.time.get_ticks()

        # Go through each row to check for a full row
        rowIndex = 0
        newGrid = grid
        for row in grid:
            isFull = True
            if rowIndex == 0 or rowIndex == numberOfRows + 1:
                isFull = False
            for brick in row:
                if brick == 0:
                    isFull = False
            if isFull:
                newGrid = np.delete(newGrid, rowIndex, axis=0)
                newGrid = np.insert(newGrid, 1, np.array([8] + [0] * numberOfColumns + [8]), 0)
                isFull = False
            rowIndex += 1
        grid = newGrid

    pygame.display.flip()

    clock.tick(60)

pygame.quit()