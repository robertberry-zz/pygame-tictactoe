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

def main():
    pygame.init()
    screen = pygame.display.set_mode([300, 300])
    pygame.display.set_caption(CAPTION)

    background, background_rect = load_image('grid.png')
    screen.blit(background, (0,0))
    pygame.display.flip()

    clock = pygame.time.Clock()

    x = Cross()
    x.rect.topleft = (10, 10)

    sprites = pygame.sprite.RenderPlain((x))

    while True:
        clock.tick(MAXIMUM_FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

        sprites.update()
        screen.blit(background, (0, 0))
        sprites.draw(screen)
        pygame.display.flip()

if __name__ == "__main__": main()
