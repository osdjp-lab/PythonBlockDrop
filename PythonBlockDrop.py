import pygame
import random

# Global constants

window_width = 800
window_height = 750
top_left_x = (window_width - 300) // 2
top_left_y = window_height - 600

# Blocks

# defining blocks

block1 = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

block2 = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

block3 = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

block4 = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

block5 = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

block6 = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

block7 = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

blocks = [block1, block2,block3, block4, block5, block6, block7]
block_colors = [(255, 165, 0), (128, 0, 128), (255, 255, 0), (0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255)]


def game_grid(pos={}):
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in pos:
                c = pos[(j, i)]
                grid[i][j] = c
    return grid


class Block(object):
    rows = 20
    columns = 10

    def __init__(self, column, row, block):
        self.x = column
        self.y = row
        self.block = block
        self.color = block_colors[blocks.index(block)]
        self.rotation = 0  # 0,1,2,3


def get_block():
    global blocks, block_colors
    return Block(5, 0, random.choice(blocks))


def get_pos(block):
    positions = []
    format = block.block[block.rotation % len(block.block)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((block.x + j, block.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(block, grid):
    valid_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    valid_pos = [j for sub in valid_pos for j in sub]
    block_pos = get_pos(block)

    for pos in block_pos:
        if pos not in valid_pos:
            if pos[1] > -1:
                return False
    return True


def draw_window(surface):
    """Draw the game window.

    Args:
        surface (pygame.Surface): Display surface.
    
    """
    surface_color = pygame.colordict.THECOLORS.get("black")
    surface.fill(surface_color)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(
                surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)

    for i in range(20):
        pygame.draw.line(surface, (128, 128, 128), (top_left_x, top_left_y + i*30),
                         (top_left_x + 300, top_left_y + i * 30))  # horizontal lines
        for j in range(10):
            pygame.draw.line(surface, (128, 128, 128), (top_left_x + j * 30, top_left_y),
                             (top_left_x + j * 30, top_left_y + 600))  # vertical lines
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x,top_left_y, 300, 600), 5)


def play():
    global grid
    run = True
    block = get_block()
    next_block = False
    positions = {}

    while run:
        grid = game_grid(positions)
        if block.y > 0:
            block.y -= 1
            next_block = True

        block.y += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            block.y -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    block.x -= 1
                    # if not valid_space(block, grid):
                    #     block.x += 1

                elif event.key == pygame.K_RIGHT:
                    block.x += 1
                    # if not valid_space(block, grid):
                    #     block.x -= 1

        block_pos = get_pos(block)

        # add piece to the grid for drawing
        for i in range(len(block_pos)):
            x, y = block_pos[i]
            if y > -1:
                grid[y][x] = block.color

        if next_block:
            for pos in block_pos:
                p = (pos[0], pos[1])
                positions[p] = block.color
            block = get_block()
            next_block = False

        pygame.display.update()

def main():
    """The main function of the PythonBlockDrop game."""
    pygame.font.init()
    pygame.display.set_caption('Tetris')
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                main()

window = pygame.display.set_mode((window_width, window_height))
draw_window(window)


if __name__ == "__main__":
    main()
