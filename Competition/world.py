import random
import pygame

walls = []
decorations = []


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y, foodId):
        super(Food, self).__init__()
        self.original_image = pygame.image.load("Food/" + str(foodId) + ".png")
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.image = self.original_image
        self.rect = self.image.get_rect().move(x, y)


# Object class for either a collision or decoration object
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, type, flipped):
        super(Object, self).__init__()
        if type == "Side":
            self.original_image = pygame.image.load("Level Assets/Wall.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
            self.original_image = pygame.transform.flip(self.original_image, True, False)
        elif type == "Side 2":
            self.original_image = pygame.image.load("Level Assets/Wall.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
        elif type == "Floor":
            self.original_image = pygame.image.load("Level Assets/Ground.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
        elif type == "Platform":
            self.original_image = pygame.image.load("Level Assets/Platform.png")
            self.original_image = pygame.transform.scale(self.original_image, (320, 64))
        elif type == "Pillar Side":
            self.original_image = pygame.image.load("Level Assets/Pillar_side.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
            if flipped: self.original_image = pygame.transform.flip(self.original_image, True, False)
        elif type == "Pillar Top":
            self.original_image = pygame.image.load("Level Assets/Pillar_top.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
            if flipped: self.original_image = pygame.transform.flip(self.original_image, True, False)
        elif type == "Grassy Side":
            self.original_image = pygame.image.load("Level Assets/Grassy_side.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
            if flipped: self.original_image = pygame.transform.flip(self.original_image, True, False)
        elif type == "Pillar Center":
            self.original_image = pygame.image.load("Level Assets/Pillar_center.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
        elif type == "Pillar Top Center":
            self.original_image = pygame.image.load("Level Assets/Pillar_top_center.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
        elif type == "Platform Side":
            self.original_image = pygame.image.load("Level Assets/Platform_side.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
            if flipped: self.original_image = pygame.transform.flip(self.original_image, True, False)
        elif type == "Platform Center":
            self.original_image = pygame.image.load("Level Assets/Platform_center.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
        elif type == "Big Tree":
            self.original_image = pygame.image.load("Level Assets/Tree_big.png")
            self.original_image = pygame.transform.scale(self.original_image, (192, 192))
        elif type == "Small Tree":
            self.original_image = pygame.image.load("Level Assets/Tree_small.png")
            self.original_image = pygame.transform.scale(self.original_image, (128, 128))
        elif type == "Bush":
            self.original_image = pygame.image.load("Level Assets/Bush.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
        elif type == "Grass":
            self.original_image = pygame.image.load("Level Assets/Grass.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
        elif type == "Flower":
            self.original_image = pygame.image.load("Level Assets/Flower.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
        elif type == "Cloud":
            self.original_image = pygame.image.load("Level Assets/Cloud.png")
            self.original_image = pygame.transform.scale(self.original_image, (320, 128))
            if flipped: self.original_image = pygame.transform.flip(self.original_image, True, False)
        self.image = self.original_image
        self.rect = self.image.get_rect().move(x, y)


# Creates a random food object at a random position in the world
def instantiateFood():
    import main
    xPos = random.randint(64, main.SCREEN_WIDTH - 320)
    yPos = random.randint(192, main.SCREEN_HEIGHT - 64)
    foodId = random.randint(44, 57)
    food = Food(xPos, yPos, foodId)
    return food

# Create the level walls and decorations
def run():
    # Get the screen size from the main script
    import main
    SCREEN_WIDTH = main.SCREEN_WIDTH
    SCREEN_HEIGHT = main.SCREEN_HEIGHT

    # First pillar
    for i in range(4):
        decorations.append(Object(SCREEN_WIDTH - 1856, SCREEN_HEIGHT - 320 + i * 64, "Pillar Center", False))
        decorations.append(Object(SCREEN_WIDTH - 1792, SCREEN_HEIGHT - 320 + i * 64, "Pillar Side", True))
    walls.append(Object(SCREEN_WIDTH - 1856, SCREEN_HEIGHT - 384, "Pillar Top Center", False))
    walls.append(Object(SCREEN_WIDTH - 1792, SCREEN_HEIGHT - 384, "Pillar Top", True))
    decorations.append(Object(SCREEN_WIDTH - 1728, SCREEN_HEIGHT - 384, "Grassy Side", True))

    # Second pillar
    for i in range(2):
        decorations.append(Object(SCREEN_WIDTH-1408, SCREEN_HEIGHT-192 + i * 64, "Pillar Side", False))
        decorations.append(Object(SCREEN_WIDTH-1344, SCREEN_HEIGHT-192 + i * 64, "Pillar Side", True))
    walls.append(Object(SCREEN_WIDTH-1408, SCREEN_HEIGHT-256, "Pillar Top", False))
    decorations.append(Object(SCREEN_WIDTH-1472, SCREEN_HEIGHT-256, "Grassy Side", False))
    walls.append(Object(SCREEN_WIDTH-1344, SCREEN_HEIGHT-256, "Pillar Top", True))
    decorations.append(Object(SCREEN_WIDTH-1280, SCREEN_HEIGHT-256, "Grassy Side", True))

    # Floor
    for i in range(30):
        walls.append(Object(i*64, SCREEN_HEIGHT-64, "Floor", False))

    # 5 Platforms
    walls.append(Object(SCREEN_WIDTH-1032, SCREEN_HEIGHT-384, "Platform Side", False))
    for i in range(3):
        walls.append(Object(SCREEN_WIDTH-968 + 64*i, SCREEN_HEIGHT-384, "Platform Center", False))
    walls.append(Object(SCREEN_WIDTH - 776, SCREEN_HEIGHT - 384, "Platform Side", True))
    decorations.append(Object(SCREEN_WIDTH - 1096, SCREEN_HEIGHT - 384, "Grassy Side", False))
    decorations.append(Object(SCREEN_WIDTH - 712, SCREEN_HEIGHT - 384, "Grassy Side", True))
    walls.append(Object(SCREEN_WIDTH - 648, SCREEN_HEIGHT - 576, "Platform Side", False))
    for i in range(3):
        walls.append(Object(SCREEN_WIDTH - 584 + 64 * i, SCREEN_HEIGHT - 576, "Platform Center", False))
    walls.append(Object(SCREEN_WIDTH - 392, SCREEN_HEIGHT - 576, "Platform Side", True))
    decorations.append(Object(SCREEN_WIDTH - 712, SCREEN_HEIGHT - 576, "Grassy Side", False))
    decorations.append(Object(SCREEN_WIDTH - 328, SCREEN_HEIGHT - 576, "Grassy Side", True))
    walls.append(Object(SCREEN_WIDTH - 1480, SCREEN_HEIGHT - 640, "Platform Side", False))
    for i in range(3):
        walls.append(Object(SCREEN_WIDTH - 1416 + 64 * i, SCREEN_HEIGHT - 640, "Platform Center", False))
    walls.append(Object(SCREEN_WIDTH - 1224, SCREEN_HEIGHT - 640, "Platform Side", True))
    decorations.append(Object(SCREEN_WIDTH - 1544, SCREEN_HEIGHT - 640, "Grassy Side", False))
    decorations.append(Object(SCREEN_WIDTH - 1160, SCREEN_HEIGHT - 640, "Grassy Side", True))
    walls.append(Object(SCREEN_WIDTH - 960, SCREEN_HEIGHT - 784, "Platform Side", False))
    walls.append(Object(SCREEN_WIDTH - 896, SCREEN_HEIGHT - 784, "Platform Side", True))
    decorations.append(Object(SCREEN_WIDTH - 1024, SCREEN_HEIGHT - 784, "Grassy Side", False))
    decorations.append(Object(SCREEN_WIDTH - 832, SCREEN_HEIGHT - 784, "Grassy Side", True))
    walls.append(Object(SCREEN_WIDTH - 1344, SCREEN_HEIGHT - 876, "Platform Side", False))
    walls.append(Object(SCREEN_WIDTH - 1280, SCREEN_HEIGHT - 876, "Platform Side", True))
    decorations.append(Object(SCREEN_WIDTH - 1408, SCREEN_HEIGHT - 876, "Grassy Side", False))
    decorations.append(Object(SCREEN_WIDTH - 1216, SCREEN_HEIGHT - 876, "Grassy Side", True))

    # Left wall
    for x in range(17):
        walls.append(Object(0, x*64, "Side", False))

    # Right wall
    for y in range(11):
        walls.append(Object(SCREEN_WIDTH-64, y*64, "Side 2", False))

    # Right pillar
    for i in range(2):
        decorations.append(Object(SCREEN_WIDTH-576, SCREEN_HEIGHT-128 - i * 64, "Pillar Side", False))
        decorations.append(Object(SCREEN_WIDTH-512, SCREEN_HEIGHT-128 - i * 64, "Pillar Center", False))
        decorations.append(Object(SCREEN_WIDTH-448, SCREEN_HEIGHT-128 - i * 64, "Pillar Center", False))
        decorations.append(Object(SCREEN_WIDTH-384, SCREEN_HEIGHT-128 - i * 64, "Pillar Center", False))
        decorations.append(Object(SCREEN_WIDTH-320, SCREEN_HEIGHT-128 - i * 64, "Pillar Center", False))
    for i in range(4):
        walls.append(Object(SCREEN_WIDTH-512 + 64 * i, SCREEN_HEIGHT-256, "Pillar Top Center", False))
    walls.append(Object(SCREEN_WIDTH-576, SCREEN_HEIGHT-256, "Pillar Top", False))
    decorations.append(Object(SCREEN_WIDTH-640, SCREEN_HEIGHT-256, "Grassy Side", False))
    for z in range(5):
        walls.append(Object(SCREEN_WIDTH-256, SCREEN_HEIGHT-64 - z*64, "Pillar Side", False))
        decorations.append(Object(SCREEN_WIDTH-192, SCREEN_HEIGHT-64 - z * 64, "Pillar Center", False))
        decorations.append(Object(SCREEN_WIDTH-128, SCREEN_HEIGHT-64 - z * 64, "Pillar Center", False))
        decorations.append(Object(SCREEN_WIDTH-64, SCREEN_HEIGHT-64 - z * 64, "Pillar Center", False))
    for i in range(3):
        walls.append(Object(SCREEN_WIDTH-192 + 64*i, SCREEN_HEIGHT-384, "Pillar Top Center", False))
    walls.append(Object(SCREEN_WIDTH-256, SCREEN_HEIGHT-384, "Pillar Top", False))

    # Decorations
    decorations.append(Object(SCREEN_WIDTH-320, SCREEN_HEIGHT-384, "Grassy Side", False))
    decorations.append(Object(896, SCREEN_HEIGHT-256, "Big Tree", False))
    decorations.append(Object(320, SCREEN_HEIGHT - 192, "Small Tree", False))
    decorations.append(Object(192, SCREEN_HEIGHT - 128, "Bush", False))
    decorations.append(Object(SCREEN_WIDTH-512, SCREEN_HEIGHT - 320, "Bush", False))
    decorations.append(Object(SCREEN_WIDTH - 512, SCREEN_HEIGHT - 320, "Bush", False))
    decorations.append(Object(SCREEN_WIDTH - 256, SCREEN_HEIGHT - 448, "Grass", False))
    decorations.append(Object(SCREEN_WIDTH - 192, SCREEN_HEIGHT - 448, "Grass", False))
    decorations.append(Object(SCREEN_WIDTH - 1280, SCREEN_HEIGHT - 940, "Grass", False))
    decorations.append(Object(SCREEN_WIDTH - 960, SCREEN_HEIGHT - 848, "Flower", False))
    decorations.append(Object(SCREEN_WIDTH - 128, SCREEN_HEIGHT - 448, "Flower", False))
    decorations.append(Object(SCREEN_WIDTH - 1800, SCREEN_HEIGHT - 900, "Cloud", False))
    decorations.append(Object(SCREEN_WIDTH - 500, SCREEN_HEIGHT - 800, "Cloud", True))
    decorations.append(Object(SCREEN_WIDTH - 900, SCREEN_HEIGHT - 1000, "Cloud", False))
    decorations.append(Object(SCREEN_WIDTH - 1300, SCREEN_HEIGHT - 800, "Cloud", True))