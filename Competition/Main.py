import pygame
import World

# Init pygame and the screen
pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# running = False
# while not running:
import mainMenu

# mainMenu.running = True
# Create the world and receive the walls and decorations
World.run()
walls = World.walls
decorations = World.decorations

# Run the player and enemy controller
def start():
    import Controller
# Controller.play()

