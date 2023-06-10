import pygame
import world

# Init pygame and the screen
pygame.init()

# Set screen size
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
# Uncomment for fullscreen: (Might mess up screen size)
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN, pygame.RESIZABLE)
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Import and show the main menu
import mainMenu

# Create the world and receive the walls and decorations
world.run()
walls = world.walls
decorations = world.decorations

# Run the player and enemy controller when the play button is pressed
def start():
    import controller

