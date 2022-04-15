import pygame, neat, time, os, random
pygame.font.init()

WIN_WIDTH = 600
WIN_HEIGHT = 150

DINOSAUR_STANDING_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "dinosaur", "standing", "dinosaur1.png"))),
                            pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "dinosaur", "standing", "dinosaur2.png")))]
DINOSAUR_DOWN_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "dinosaur", "down", "dinosaur_down1.png"))),
                        pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "dinosaur", "down", "dinosaur_down2.png")))]
BIG_CACTUS_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "cactus", "big", "big_cactus1.png"))),
                    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "cactus", "big", "big_cactus2.png"))),
                    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "cactus", "big", "big_cactus3.png")))]
SMALL_CACTUS_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "cactus", "small", "small_cactus1.png"))),
                        pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "cactus", "small", "small_cactus2.png"))),
                        pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "cactus", "small", "small_cactus3.png")))]
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird", "bird1.png"))),
                pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird", "bird2.png")))]
CLOUD_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "misc", "cloud.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "misc", "base.png")))

class Dinosaur:

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Cactus:

    def __init__(self, x):
        self.x = x

def draw_window(win):
    pygame.display.update()
