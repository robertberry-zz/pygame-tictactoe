"""
TicTacToe

Author: Robert Berry <rjberry@gmail.com>
Date: 20th September 2011
"""

import os
import sys

import pygame
from pygame.locals import *
from pygame.sprite import Sprite

# Window caption
CAPTION = "Noughts & Crosses"

# Maximum frames per second
MAXIMUM_FPS = 60

def load_image(name, colorkey=None):
    """Loads image from resource directory with the given colour key for
    determining which pixels should be transparent.
    """
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
    """Represents the noughts and crosses grid."""
    
    def __init__(self):
        Sprite.__init__(self)
        self.image, self.rect = load_image('grid.png')
        self.data = [[None for col in range(3)] \
                     for row in range(3)]
        self.group = pygame.sprite.RenderPlain()

    def get_top_left(self, x, y):
        """Returns the pixel co-ordinates of the top left corner of where a
        nought or cross should be drawn for the given grid co-ordinates.
        """
        if not (0 <= x < 3 and 0 <= y < 3):
            raise KeyError
        
        return (10 + 100 * x, 10 + 100 * y)

    def insert(self, x, y, piece):
        """Inserts a piece into the grid at the given co-ordinates."""
        piece.rect.topleft = self.get_top_left(x, y)
        self.group.add(piece)

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        self.group.draw(screen)

    def get_lines(self):
        """Returns lines, which if filled with pieces of one type indicate a
        winning state."""
        horizontals = [[self.data[x][y] for y in range(3)] \
                       for x in range(3)]
        verticals = [[self.data[x][y] for x in range(3)] \
                     for y in range(3)]
        diagonals = [[self.data[i][i] for i in range(3)],
                     [self.data[i][2-i] for i in range(3)]]
        return horizontals + verticals + diagonals

class Computer(object):
    def __init__(self, grid):
        self.grid = grid

    def get_next_move():
        lines = self.grid.get_lines()
        pass

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
