import pygame, neat, time, os, random
pygame.font.init()

WIN_WIDTH = 1200
WIN_HEIGHT = 300

DINOSAUR_STANDING_IMGS = [(pygame.image.load(os.path.join("imgs", "dinosaur", "standing", "dinosaur1.png"))),
                            (pygame.image.load(os.path.join("imgs", "dinosaur", "standing", "dinosaur2.png")))]
DINOSAUR_DOWN_IMGS = [(pygame.image.load(os.path.join("imgs", "dinosaur", "down", "dinosaur_down1.png"))),
                        (pygame.image.load(os.path.join("imgs", "dinosaur", "down", "dinosaur_down2.png")))]
BIG_CACTUS_IMGS = [(pygame.image.load(os.path.join("imgs", "cactus", "big", "big_cactus1.png"))),
                    (pygame.image.load(os.path.join("imgs", "cactus", "big", "big_cactus2.png"))),
                    (pygame.image.load(os.path.join("imgs", "cactus", "big", "big_cactus3.png")))]
SMALL_CACTUS_IMGS = [(pygame.image.load(os.path.join("imgs", "cactus", "small", "small_cactus1.png"))),
                        (pygame.image.load(os.path.join("imgs", "cactus", "small", "small_cactus2.png"))),
                        (pygame.image.load(os.path.join("imgs", "cactus", "small", "small_cactus3.png")))]
BIRD_IMGS = [(pygame.image.load(os.path.join("imgs", "bird", "bird1.png"))),
                (pygame.image.load(os.path.join("imgs", "bird", "bird2.png")))]
CLOUD_IMG = (pygame.image.load(os.path.join("imgs", "misc", "cloud.png")))
BASE_IMG = (pygame.image.load(os.path.join("imgs", "misc", "base.png")))

class Dinosaur:
    STANDING_IMGS = DINOSAUR_STANDING_IMGS
    DOWN_IMGS = DINOSAUR_DOWN_IMGS

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Cactus:
    # make velocity global in some way. DO NOT USE GLOBAL
    VEL = 5

    def __init__(self, x) -> None:
        self.x = x
        self.img = BIG_CACTUS_IMGS[random.randrange(0, 3)]
        self.height = WIN_HEIGHT - self.img.get_height()

        self.passed = False

    def move(self) -> None:
        self.x -= self.VEL

    def draw(self, win) -> None:
        win.blit(self.img, (self.x, self.height))

class SmallCactus(Cactus):
    def __init__(self, x) -> None:
        self.x = x
        self.img = SMALL_CACTUS_IMGS[random.randrange(0, 3)]
        self.height = WIN_HEIGHT - self.img.get_height()

        self.passed = False

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y) -> None:
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self) -> None:
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win) -> None:
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def draw_window(win, base, obsticles) -> None:
    win.fill((0,0,0))
    base.draw(win)

    for o in obsticles:
        o.draw(win)

    pygame.display.update()

def main() -> None:
    base = Base(WIN_HEIGHT - BASE_IMG.get_height())
    obsticles = [Cactus(1200)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), vsync=1)
    clock = pygame.time.Clock()

    run = True
    while run:
        print(obsticles)
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        add_ob = False
        rem = []
        for o in obsticles:
            if o.x < WIN_WIDTH / 2 and not o.passed:
                o.passed = True
                add_ob = True

            if o.x < 0 - o.img.get_width():
                rem.append(o)

            o.move()

        if add_ob:
            options = [Cactus(1200), SmallCactus(1200)]
            obsticles.append(random.choice(options))

        for r in rem:
            obsticles.remove(r)

        base.move()
        draw_window(win, base, obsticles)

main()
