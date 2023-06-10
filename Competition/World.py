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


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, type, flipped):
        super(Wall, self).__init__()
        if type == "Side":
            self.original_image = pygame.image.load("Wall.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
            self.original_image = pygame.transform.flip(self.original_image, True, False)
        elif type == "Side 2":
            self.original_image = pygame.image.load("Wall.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
        elif type == "Floor":
            self.original_image = pygame.image.load("Ground.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
        elif type == "Platform":
            self.original_image = pygame.image.load("Platform.png")
            self.original_image = pygame.transform.scale(self.original_image, (320, 64))
        elif type == "Pillar Side":
            self.original_image = pygame.image.load("Pillar_side.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
            if flipped: self.original_image = pygame.transform.flip(self.original_image, True, False)
        elif type == "Pillar Top":
            self.original_image = pygame.image.load("Pillar_top.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
            if flipped: self.original_image = pygame.transform.flip(self.original_image, True, False)
        elif type == "Grassy Side":
            self.original_image = pygame.image.load("Grassy_side.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
            if flipped: self.original_image = pygame.transform.flip(self.original_image, True, False)
        elif type == "Pillar Center":
            self.original_image = pygame.image.load("Pillar_center.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
        elif type == "Pillar Top Center":
            self.original_image = pygame.image.load("Pillar_top_center.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
        elif type == "Big Tree":
            self.original_image = pygame.image.load("Tree_big.png")
            self.original_image = pygame.transform.scale(self.original_image, (192, 192))
        elif type == "Platform Side":
            self.original_image = pygame.image.load("Platform_side.png")
            self.original_image = pygame.transform.scale(self.original_image, (64, 64))
            if flipped: self.original_image = pygame.transform.flip(self.original_image, True, False)
        self.image = self.original_image
        self.rect = self.image.get_rect().move(x, y)

def instantiateFood():
    xPos = random.randint(200, 1200)
    yPos = random.randint(200, 600)
    foodId = random.randint(44, 57)
    food = Food(xPos, yPos, foodId)
    # screen.blit(food.image, food.rect)
    return food

def run():
    import Main
    SCREEN_WIDTH = Main.SCREEN_WIDTH
    SCREEN_HEIGHT = Main.SCREEN_HEIGHT
    # Left pillar
    for i in range(2):
        decorations.append(Wall(SCREEN_WIDTH-1408, SCREEN_HEIGHT-192 + i * 64, "Pillar Side", False))
        decorations.append(Wall(SCREEN_WIDTH-1344, SCREEN_HEIGHT-192 + i * 64, "Pillar Side", True))
    walls.append(Wall(SCREEN_WIDTH-1408, SCREEN_HEIGHT-256, "Pillar Top", False))
    decorations.append(Wall(SCREEN_WIDTH-1472, SCREEN_HEIGHT-256, "Grassy Side", False))
    walls.append(Wall(SCREEN_WIDTH-1344, SCREEN_HEIGHT-256, "Pillar Top", True))
    decorations.append(Wall(SCREEN_WIDTH-1280, SCREEN_HEIGHT-256, "Grassy Side", True))
    for i in range(30): # Floor
        walls.append(Wall(i*64, SCREEN_HEIGHT-64, "Floor", False))
    # Platforms
    walls.append(Wall(SCREEN_WIDTH-1032, SCREEN_HEIGHT-384, "Platform", False))
    walls.append(Wall(SCREEN_WIDTH-648, SCREEN_HEIGHT-704, "Platform", False))
    walls.append(Wall(SCREEN_WIDTH-1480, SCREEN_HEIGHT-640, "Platform", False))
    for x in range(17):
        walls.append(Wall(0, x*64, "Side", False))
    for y in range(11):
        walls.append(Wall(SCREEN_WIDTH-64, y*64, "Side 2", False))
    for i in range(2):
        decorations.append(Wall(SCREEN_WIDTH-576, SCREEN_HEIGHT-128 - i * 64, "Pillar Side", False))
        decorations.append(Wall(SCREEN_WIDTH-512, SCREEN_HEIGHT-128 - i * 64, "Pillar Center", False))
        decorations.append(Wall(SCREEN_WIDTH-448, SCREEN_HEIGHT-128 - i * 64, "Pillar Center", False))
        decorations.append(Wall(SCREEN_WIDTH-384, SCREEN_HEIGHT-128 - i * 64, "Pillar Center", False))
        decorations.append(Wall(SCREEN_WIDTH-320, SCREEN_HEIGHT-128 - i * 64, "Pillar Center", False))
    for i in range(4):
        walls.append(Wall(SCREEN_WIDTH-512 + 64 * i, SCREEN_HEIGHT-256, "Pillar Top Center", False))
    walls.append(Wall(SCREEN_WIDTH-576, SCREEN_HEIGHT-256, "Pillar Top", False))
    decorations.append(Wall(SCREEN_WIDTH-640, SCREEN_HEIGHT-256, "Grassy Side", False))
    for z in range(5):
        walls.append(Wall(SCREEN_WIDTH-256, SCREEN_HEIGHT-64 - z*64, "Pillar Side", False))
        decorations.append(Wall(SCREEN_WIDTH-192, SCREEN_HEIGHT-64 - z * 64, "Pillar Center", False))
        decorations.append(Wall(SCREEN_WIDTH-128, SCREEN_HEIGHT-64 - z * 64, "Pillar Center", False))
        decorations.append(Wall(SCREEN_WIDTH-64, SCREEN_HEIGHT-64 - z * 64, "Pillar Center", False))
    for i in range(3):
        walls.append(Wall(SCREEN_WIDTH-192 + 64*i, SCREEN_HEIGHT-384, "Pillar Top Center", False))
    walls.append(Wall(SCREEN_WIDTH-256, SCREEN_HEIGHT-384, "Pillar Top", False))
    decorations.append(Wall(SCREEN_WIDTH-320, SCREEN_HEIGHT-384, "Grassy Side", False))
    decorations.append(Wall(896, SCREEN_HEIGHT-256, "Big Tree", False))

    walls.append(Wall(SCREEN_WIDTH-960, SCREEN_HEIGHT-784, "Platform Side", False))
    walls.append(Wall(SCREEN_WIDTH - 896, SCREEN_HEIGHT - 784, "Platform Side", True))
    decorations.append(Wall(SCREEN_WIDTH - 1024, SCREEN_HEIGHT - 784, "Grassy Side", False))
    decorations.append(Wall(SCREEN_WIDTH - 832, SCREEN_HEIGHT - 784, "Grassy Side", True))