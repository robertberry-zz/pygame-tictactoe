import os
import sys

import pygame
from pygame.locals import *
from pygame.sprite import Sprite

CAPTION = "Noughts & Crosses"
MAXIMUM_FPS = 60

def load_image(name, colorkey=None):
    fullname = os.path.join('res', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print "Cannot load image: ", name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class Cross(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image, self.rect = load_image('cross.png')

class Nought(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image, self.rect = load_image('nought.png')

class Grid(Sprite):
    ROWS = 3
    COLS = 3
    
    def __init__(self):
        Sprite.__init__(self)
        self.image, self.rect = load_image('grid.png')
        self.data = [[None for col in range(self.COLS)] \
                     for row in range(self.ROWS)]
        self.group = pygame.sprite.RenderPlain()

    def get_top_left(self, x, y):
        if not (0 <= x < self.COLS and 0 <= y < self.ROWS):
            raise KeyError
        
        return (10 + 100 * x, 10 + 100 * y)

    def insert(self, x, y, piece):
        piece.rect.topleft = self.get_top_left(x, y)
        self.group.add(piece)

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        self.group.draw(screen)

def main():
    pygame.init()
    screen = pygame.display.set_mode([300, 300])
    pygame.display.set_caption(CAPTION)

    clock = pygame.time.Clock()

    x = Cross()
    grid = Grid()
    grid.insert(0, 0, x)
    grid.insert(0, 1, Nought())

    while True:
        clock.tick(MAXIMUM_FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

        grid.draw(screen)
        pygame.display.flip()

if __name__ == "__main__": main()
