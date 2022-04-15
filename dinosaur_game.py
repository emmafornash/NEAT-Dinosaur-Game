import pygame, neat, time, os, random
pygame.font.init()

WIN_WIDTH = 600
WIN_HEIGHT = 150

class Dinosaur:

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Cactus:

    def __init__(self, x):
        self.x = x

def draw_window(win):
    pygame.display.update()
