import pygame, neat, time, os, random, math
from time import perf_counter
pygame.font.init()

WIN_WIDTH = 1200
WIN_HEIGHT = 300

# this is a bad way to implement this
GEN = 0

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

STAT_FONT = pygame.font.SysFont("sans-serif", 50)

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
        self.tick_count = 0
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
        collision_floor = 201

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
        # if self.y > collision_floor:
        #     while not(self.y - 1 <= collision_floor):
        #         self.y -= 1
        #     self.y += 1

    def draw(self, win) -> None:
        self.tick_count += 1

        if self.tick_count >= self.ANIMATION_TIME:
            self.img_count = (self.img_count + 1) % len(self.img_set)
            self.img = self.img_set[self.img_count]
            self.tick_count = 0

        if self.img_set == self.STANDING_IMGS:
            win.blit(self.img, (self.x, self.y))
        else:
            win.blit(self.img, (self.x, self.y+33))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Cactus:
    def __init__(self, x) -> None:
        self.x = x
        self.img = BIG_CACTUS_IMGS[random.randrange(0, 3)]
        self.height = WIN_HEIGHT - self.img.get_height()
        self.y = self.height

        self.send_next = False
        self.passed = False

    def move(self, velocity) -> None:
        self.x -= velocity

    def draw(self, win) -> None:
        win.blit(self.img, (self.x, self.height))

    def collide(self, dino) -> bool:
        dino_mask = dino.get_mask()
        cactus_mask = pygame.mask.from_surface(self.img)

        offset = (self.x - dino.x, self.height - round(dino.y))

        collision_point = dino_mask.overlap(cactus_mask, offset)

        return collision_point

class SmallCactus(Cactus):
    def __init__(self, x) -> None:
        self.x = x
        self.img = SMALL_CACTUS_IMGS[random.randrange(0, 3)]
        self.height = WIN_HEIGHT - self.img.get_height()
        self.y = self.height

        self.send_next = False
        self.passed = False

class Bird:
    VEL_OFFSET = 1 + random.randrange(-2, 2)
    IMGS = BIRD_IMGS
    ANIMATION_TIME = 10

    def __init__(self, x) -> None:
        self.x = x
        default_offset = WIN_HEIGHT - BASE_IMG.get_height()
        self.height = BIRD_IMGS[0].get_height()
        self.y = random.choice([default_offset - self.height,
                                default_offset - self.height*1.66,
                                default_offset - self.height*2.33])

        self.tick_count = 0
        self.img_count = 0
        self.img = self.IMGS[self.img_count]

        self.send_next = False
        self.passed = False

    def move(self, velocity) -> None:
        used_velocity = velocity + self.VEL_OFFSET
        self.x -= used_velocity

    def draw(self, win) -> None:
        self.tick_count += 1

        if self.tick_count >= self.ANIMATION_TIME:
            self.img_count = (self.img_count + 1) % len(self.IMGS)
            self.img = self.IMGS[self.img_count]
            self.tick_count = 0

        win.blit(self.img, (self.x, self.y))

    def collide(self, dino) -> bool:
        dino_mask = dino.get_mask()
        bird_mask = pygame.mask.from_surface(self.img)

        offset = (self.x - dino.x, self.y - round(dino.y))

        collision_point = dino_mask.overlap(bird_mask, offset)

        return collision_point

class Base:
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y) -> None:
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self, velocity) -> None:
        self.x1 -= velocity
        self.x2 -= velocity

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win) -> None:
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

class Cloud:
    VEL_OFFSET = 1 + random.randrange(-4, 4)
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

    def move(self, velocity) -> None:
        used_velocity = velocity - self.VEL_OFFSET
        self.x -= used_velocity

    def draw(self, win) -> None:
        win.blit(self.IMG, (self.x, self.y))

def draw_window(win, dinos, base, obstacles, clouds, score, specimen, gen) -> None:
    win.fill((0,0,0))

    for c in clouds:
        c.draw(win)

    base.draw(win)

    for o in obstacles:
        o.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    text = STAT_FONT.render("Specimen: " + str(specimen), 1, (255, 255, 255))
    win.blit(text, (10, 50))

    for d in dinos:
        d.draw(win)

    pygame.display.update()

def main(genomes, config) -> None:
    global GEN
    GEN += 1

    nets = []
    ge = []
    dinos = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        dinos.append(Dinosaur(11, 200))
        g.fitness = 0
        ge.append(g)

    base = Base(WIN_HEIGHT - BASE_IMG.get_height())
    obstacles = [Cactus(1200)]
    clouds = [Cloud(1300)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), vsync=1)
    clock = pygame.time.Clock()

    universal_velocity = 7
    # NOTE: no idea if a velocity this fast is even possible to survive in
    max_universal_velocity = 21
    time_until_max = 120
    per_frame_increase = (max_universal_velocity - universal_velocity) / (60*60*time_until_max)

    score = 0
    run = True
    while run:
        score += 1
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

        if universal_velocity < max_universal_velocity:
            universal_velocity += per_frame_increase

        obs_ind = 0
        if len(dinos) > 0:
            if len(obstacles) > 1 and dinos[0].x > obstacles[0].x + obstacles[0].img.get_width():
                obs_ind = 1
        else:
            run = False
            break

        for x, dino in enumerate(dinos):
            ge[x].fitness += 0.01
            output = nets[x].activate((dino.y, abs(dino.x - obstacles[obs_ind].x),
                                        abs(dino.y - obstacles[obs_ind].y),
                                        obstacles[obs_ind].img.get_width()))

            if output[0] > 0.5:
                dino.jumping = True
            if output[1] > 0.5:
                dino.ducking = True

            dino.move()

        add_ob = False
        give_score = False
        rem = []
        for o in obstacles:
            for x, dino in enumerate(dinos):
                if o.collide(dino):
                    ge[x].fitness -= 7
                    dinos.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if o.x < WIN_WIDTH / 2 and not o.send_next:
                    o.send_next = True
                    add_ob = True

                if o.x < dino.x and not o.passed:
                    o.passed = True
                    give_score = True

            if o.x < 0 - o.img.get_width():
                rem.append(o)

            o.move(universal_velocity)

        if add_ob:
            options = [Cactus(1200), SmallCactus(1200), Bird(1200), Bird(1200)]
            # options = [Bird(1200)]
            obstacles.append(random.choice(options))

        for r in rem:
            obstacles.remove(r)

        if give_score:
            for g in ge:
                g.fitness += 10

        add_cloud = False
        cloud_rem = []
        for c in clouds:
            if c.x < WIN_WIDTH * random.uniform(0.33, 0.75) and not c.send_next:
                c.send_next = True
                add_cloud = True

            if c.x < 0 - c.IMG.get_width():
                cloud_rem.append(c)

            c.move(universal_velocity)

        if add_cloud:
            clouds.append(Cloud(1300))

        for c in cloud_rem:
            clouds.remove(c)

        specimen = len(dinos)
        base.move(universal_velocity)
        draw_window(win, dinos, base, obstacles, clouds, score, specimen, GEN)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    winner = population.run(main,200)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
