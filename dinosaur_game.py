import pygame, neat, time, os, random, math
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
    ANIMATION_TIME = 10
    GRAVITY = 0.7

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

        self.tick_count = 0
        self.vel = 0
        self.height = self.y

        self.img_set = DINOSAUR_STANDING_IMGS
        self.img_count = 0
        self.img = self.img_set[self.img_count]

        self.jumping = False
        self.ducking = False

    def move(self) -> None:
        if self.ducking:
            vel_modifier = 2
            self.img_set = self.DOWN_IMGS
            self.ducking = False
        else:
            vel_modifier = 1
            self.img_set = self.STANDING_IMGS

        self.vel += self.GRAVITY*vel_modifier

        # NOTE: if any bugs arise, make this variable again dependent on the
        # size of the sprite currently used.
        collision_floor = 200

        if self.y + 1 >= collision_floor and self.jumping:
            self.vel = -15

        # makes sure the dinosaur is exactly lined with the ground
        if self.y + self.vel >= collision_floor:
            while not (self.y + math.copysign(1, self.vel) >= collision_floor):
                self.y += math.copysign(1, self.vel)
            self.vel = 0

        self.y += self.vel
        self.jumping = False

        # makes sure the dinosaur does not go under the ground
        if self.y > collision_floor:
            while not(self.y - 1 <= collision_floor):
                self.y -= 1
            self.y += 1

    def draw(self, win) -> None:
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.img_set[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.img_set[1]
        else:
            self.img = self.img_set[0]
            self.img_count = 0

        if self.img_set == self.STANDING_IMGS:
            win.blit(self.img, (self.x, self.y))
        else:
            win.blit(self.img, (self.x, self.y+33))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Cactus:
    # TODO: make velocity global in some way. DO NOT USE GLOBAL
    VEL = 7

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

class Bird:
    IMGS = BIRD_IMGS
    # NOTE: maybe set this to a custom distribution, i.e. the mean is still 7,
    # but the range can so significantly more negative
    VEL = 7 + random.randrange(-2, 2)
    ANIMATION_TIME = 10

    def __init__(self, x) -> None:
        self.x = x
        default_offset = WIN_HEIGHT - BASE_IMG.get_height()
        self.height = BIRD_IMGS[0].get_height()
        self.y = random.choice([default_offset - self.height,
                                default_offset - self.height*1.66,
                                default_offset - self.height*2.33])

        self.img_count = 0
        self.img = self.IMGS[self.img_count]

        self.passed = False

    def move(self) -> None:
        self.x -= self.VEL

    def draw(self, win) -> None:
        self.img_count += 1

        # NOTE: this may be inefficient, come back later
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        else:
            self.img = self.IMGS[0]
            self.img_count = 0

        win.blit(self.img, (self.x, self.y))

class Base:
    VEL = 7
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

class Cloud:
    VEL = 6 + random.randrange(-4, 4)
    IMG = CLOUD_IMG

    def __init__(self, x) -> None:
        self.x = x
        default_offset = WIN_HEIGHT - 100
        self.height = CLOUD_IMG.get_height()
        self.y = random.choice([default_offset - self.height,
                                default_offset - self.height*2,
                                default_offset - self.height*3,
                                default_offset - self.height*4])

        self.send_next = False

    def move(self) -> None:
        self.x -= self.VEL

    def draw(self, win) -> None:
        win.blit(self.IMG, (self.x, self.y))

def draw_window(win, dino, base, obstacles, clouds) -> None:
    win.fill((0,0,0))

    for c in clouds:
        c.draw(win)

    base.draw(win)

    for o in obstacles:
        o.draw(win)

    dino.draw(win)

    pygame.display.update()

def main() -> None:
    dino = Dinosaur(11, 10)
    base = Base(WIN_HEIGHT - BASE_IMG.get_height())
    obstacles = [Cactus(1200)]
    clouds = [Cloud(1300)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), vsync=1)
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            # debug controls
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_UP:
            #         dino.jumping = True
            #     if event.key == pygame.K_DOWN:
            #         dino.ducking = True
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        dino.move()
        add_ob = False
        rem = []
        for o in obstacles:
            if o.x < WIN_WIDTH / 2 and not o.passed:
                o.passed = True
                add_ob = True

            if o.x < 0 - o.img.get_width():
                rem.append(o)

            o.move()

        if add_ob:
            options = [Cactus(1200), SmallCactus(1200), Bird(1200)]
            # options = [Bird(1200)]
            obstacles.append(random.choice(options))

        for r in rem:
            obstacles.remove(r)

        add_cloud = False
        cloud_rem = []
        for c in clouds:
            if c.x < WIN_WIDTH * random.uniform(0.33, 0.75) and not c.send_next:
                c.send_next = True
                add_cloud = True

            if c.x < 0 - c.IMG.get_width():
                cloud_rem.append(c)

            c.move()

        if add_cloud:
            clouds.append(Cloud(1300))

        for c in cloud_rem:
            clouds.remove(c)

        base.move()
        draw_window(win, dino, base, obstacles, clouds)

main()
