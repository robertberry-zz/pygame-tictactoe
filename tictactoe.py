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

from utils import *

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
            raise KeyError, "(%d, %d) not in grid" % (x, y)
        
        return (10 + 100 * x, 10 + 100 * y)

    def translate_coords(self, x, y):
        """Given screen coordinates returns the corresponding coordinates in
        the grid. Used for placing pieces when the user clicks on the screen.
        >>> translate_coords(9, 14)
        (0, 0)
        """
        return (x / 100, y / 100)

    def insert(self, x, y, piece):
        """Inserts a piece into the grid at the given co-ordinates."""
        piece.rect.topleft = self.get_top_left(x, y)
        self.group.add(piece)
        self.data[x][y] = piece

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        self.group.draw(screen)

    def get(self, x, y):
        return self.data[x][y]

    def get_lines(self):
        """Returns lines, which if filled with pieces of one type indicate a
        winning state.
        """
        horizontals = [[(x, y) for y in range(3)] \
                       for x in range(3)]
        verticals = [[(x, y) for x in range(3)] \
                     for y in range(3)]
        diagonals = [[(i, i) for i in range(3)],
                     [(i, 2-i) for i in range(3)]]
        return horizontals + verticals + diagonals

    def get_spaces(self):
        """Returns a list of all the spaces in the grid."""
        return [(x, y) for y in range(3) for x in range(3)]

    def no_moves_left(self):
        """Returns if there are no more available moves."""
        return all(self.get(*coord) for coord in self.get_spaces())

    def is_end_game(self):
        """Returns whether game at end state (i.e. someone has won or the
        players have drawn because there are no more available moves).
        """
        return self.no_moves_left() or self.get_winner()

    def get_winner(self):
        for line in self.get_lines():
            noughts = 0
            crosses = 0
            for coord in line:
                if isinstance(self.get(*coord), Nought):
                    noughts += 1
                elif isinstance(self.get(*coord), Cross):
                    crosses += 1
            if noughts == 3:
                return Nought
            elif crosses == 3:
                return Cross
        return None

class ComputerBehaviourError(Exception): pass

class Player(object):
    """Represents a human tic tac toe player."""
    def __init__(self, grid, piece):
        self.grid = grid
        self.piece = piece

    def take_move(self, coords):
        """Takes a move given mouse co-ordinates (and assuming the position in
        the grid has not already been occupied.
        """
        coords = self.grid.translate_coords(*coords)
        if self.grid.get(*coords) == None:
            self.grid.insert(coords[0], coords[1], self.piece())
            return True
        return False

class Computer(object):
    """Represents a computer player for tic tac toe."""
    def __init__(self, grid, piece):
        self.grid = grid
        self.piece = piece

    def take_move(self):
        move = self.get_next_move()
        self.grid.insert(move[0], move[1], self.piece())

    def get_next_move(self):
        """Uses the grid to figure out the next move the computer wants to
        make.
        """
        enemy_piece = Cross if self.piece is Nought else Nought

        def count_pieces(line):
            pieces = (self.grid.get(*coord) for coord in line)
            mine, enemies, spaces = 0, 0, 0
            
            for piece in pieces:
                if isinstance(piece, self.piece):
                    mine += 1
                elif isinstance(piece, enemy_piece):
                    enemies += 1
                else:
                    spaces += 1
            return mine, enemies, spaces

        def first_empty_space(line):
            for coord in line:
                if self.grid.get(*coord) == None:
                    return coord
            return None

        def win_game(mine, enemies, spaces):
            return mine == 2 and spaces == 1

        def prevent_losing_game(mine, enemies, spaces):
            return enemies == 2 and spaces == 1

        def attempt_winning_position(mine, enemies, spaces):
            return mine == 1 and spaces == 2

        behaviours = (win_game,
                      prevent_losing_game)
        
        lines = self.grid.get_lines()

        for behaviour in behaviours:
            for line in lines:
                if behaviour(*count_pieces(line)):
                    return first_empty_space(line)

        # score square based on how many empty squares exist in lines in which
        # the co-ordinate is placed
        def score_square(coord):
            related_lines = [line for line in lines if coord in line]
            empty_spaces = 0
            for line in related_lines:
                empty_spaces += count_if(lambda pos: pos != coord and \
                                         self.grid.get(*pos) is None, line)
            return empty_spaces

        empty_squares = [x for x in self.grid.get_spaces() \
                         if self.grid.get(*x) == None]

        return argmax(empty_squares, score_square)

def quit_on_quit_event(event):
    if event.type == QUIT or \
           (event.type == KEYDOWN and event.key == K_ESCAPE):
        exit(0)

def play(screen, player_piece=Nought):
    """Plays a game!"""
    clock = pygame.time.Clock()

    cpu_piece = Nought if player_piece is Cross else Cross

    grid = Grid()
    cpu = Computer(grid, cpu_piece)
    player = Player(grid, player_piece)

    turn = Cross

    while True:
        if grid.is_end_game():
            return grid.get_winner()
        
        if cpu.piece == turn:
            cpu.take_move()
            turn = player.piece

        for event in pygame.event.get():
            quit_on_quit_event(event)
            if event.type == MOUSEBUTTONDOWN:
                if player.take_move(event.pos):
                    turn = cpu.piece

        grid.draw(screen)
        pygame.display.flip()

        clock.tick(MAXIMUM_FPS)

# Not great that I have another game loop here - should probably set up some
# kind of state machine to deal with different scenarios like the game over
# screen
def play_again(screen, state):
    """Tells the user whether they won and asks them if they want to play
    again.
    """
    font = pygame.font.Font(None, 36)

    lines = ["You %s!" % state,
             "Click to play again",
             "(ESC to exit)"]

    top = 5

    for line in lines:
        text = font.render(line, 1,
                           (10, 10, 255))
        textpos = text.get_rect(centerx=150, top=top)
        screen.blit(text, textpos)
        top += 40
        
    pygame.display.flip()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            quit_on_quit_event(event)
            if event.type == MOUSEBUTTONDOWN:
                return True
        clock.tick(MAXIMUM_FPS)
        
def main():
    pygame.init()
    screen = pygame.display.set_mode([300, 300])
    pygame.display.set_caption(CAPTION)
    player = Nought

    while True:
        cpu = Nought if player is Cross else Cross
        winner = play(screen, player)

        if winner == player:
            state = "won"
        elif winner == cpu:
            state = "lost"
        else:
            state = "drew"

        if not play_again(screen, state):
            return
        player, cpu = cpu, player

if __name__ == "__main__": main()
