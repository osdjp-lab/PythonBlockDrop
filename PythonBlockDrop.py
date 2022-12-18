import pygame
import random

# Global constants

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
BOARD_WIDTH = 300
BOARD_HEIGHT = 600
FIELD_WIDTH = 30
FIELD_HEIGHT = 20

TOP_LEFT_X = (WINDOW_WIDTH - BOARD_WIDTH) // 2
TOP_LEFT_Y = WINDOW_HEIGHT - BOARD_HEIGHT


class Block:
    """
    Representation of a single tetris block.
    
    Attributes:
        B1...B7 (list of lists of strings): Absolute definitions of each kind
                                            of tetris block and their
                                            alternative rotations.
        BLOCKS (list of objects B1...B7): List of all absolute block
                                          definitions.
        BLOCK_COLORS (list of 3 element tuples): List of RGB colors that can be
                                                 assigned to any given block.
        x (int): Position of block along the x axis.
        y (int): Position of block along the y axis.
        piece (list of lists of strings): A single object from BLOCKS.
        color (3 element tuple): A single object from BLOCK_COLORS.
        rotation (int): Index of element in piece.

    """

    B1 = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

    B2 = [['.....',
        '.....',
        '.00..',
        '..00.',
        '.....'],
        ['.....',
        '..0..',
        '.00..',
        '.0...',
        '.....']]

    B3 = [['..0..',
        '..0..',
        '..0..',
        '..0..',
        '.....'],
        ['.....',
        '0000.',
        '.....',
        '.....',
        '.....']]

    B4 = [['.....',
        '.....',
        '.00..',
        '.00..',
        '.....']]

    B5 = [['.....',
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

    B6 = [['.....',
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

    B7 = [['.....',
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

    BLOCKS = [B1, B2, B3, B4, B5, B6, B7]

    BLOCK_COLORS = [(255, 165, 0), (128, 0, 128), (255, 255, 0), (0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255)]

    def __init__(self):
        self.x = 5
        self.y = 0
        self.piece = random.choice(self.BLOCKS)
        self.color = self.BLOCK_COLORS[self.BLOCKS.index(self.piece)]
        self.rotation = 0

    def get_relative_positions(self):
        """
        Convert absolute block definition to position relative block
        definition.
        
        Returns:
            List of positions taken by the given block after translating
            them relative to its base coordinates.
        
        """
        positions = []

        format = self.piece[self.rotation % len(self.piece)]

        for i, line in enumerate(format):
            row = line
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((self.x + j, self.y + i))

        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)

        return positions


class Board:
    """
    Representation of the game board.
    
    Attributes:
        grid (list of lists of 3 element tuples): The board.
        filled_positions (dictionary): Positions taken by blocks and their associated color.
        next_block (boolean): Flag indicating whether to switch to next block.
        current_block (Block): Block currently in motion.
        nr_blocks (int): Number of blocks spawned.
    
    """

    def __init__(self):
        self.grid = []
        self.filled_positions = {}
        self.next_block = False
        self.current_block = Block()
        self.nr_blocks = 1

    def zero_out_grid(self):
        """Assign zero tuples to all positions."""
        self.grid = [[(0,0,0) for x in range(10)] for x in range(20)]

    def add_filled_positions_to_grid(self):
        """Add filled_positions to grid."""
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (j,i) in self.filled_positions:
                    block_color = self.filled_positions[(j,i)]
                    self.grid[i][j] = block_color

    def recreate_grid(self):
        """Clear current grid and fill taken positions."""
        self.zero_out_grid()
        self.add_filled_positions_to_grid()

    def is_valid(self):
        """Check if current_block positions are valid.
        
        Returns:
            True if all positions taken by the current_block are valid.
            False if at least one field is not valid.
        
        """
        valid_pos = [[(j, i) for j in range(10) if self.grid[i][j] == (0,0,0)] for i in range(20)]

        valid_pos = [j for sub in valid_pos for j in sub]

        block_pos = self.current_block.get_relative_positions()

        for pos in block_pos:
            if pos not in valid_pos:
                if pos[1] > -1:
                    return False
        return True

    def clear_any_filled_rows(self):
        """Clear any filled rows."""
        inc = 0
        for i in range(len(self.grid)-1, -1, -1):
            row = self.grid[i]
            if (0, 0, 0) not in row:
                inc += 1
                ind = i
                for j in range(len(row)):
                    try:
                        del self.filled_positions[(j, i)]
                    except:
                        continue

        if inc > 0:
            for key in sorted(list(self.filled_positions), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    self.filled_positions[newKey] = self.filled_positions.pop(key)

    def is_game_over(self):
         """Check if game over condition has been met.
         
         Returns:
             True if game is over.
             False if game is not over.
         
         """
         for pos in self.filled_positions:
             x, y = pos
             if y < 1:
                 return True
         return False

    def block_motion(self, fall_time):
        """Move current_block downwards at a predefined rate.
        
        Returns:
            int: The current fall_time if threshold has not been reached or zero
                 if it has.
        
        """
        fall_time_interval = 300

        if fall_time >= fall_time_interval:
            fall_time = 0
            self.current_block.y += 1
            if not self.is_valid() and self.current_block.y > 0:
                self.current_block.y -= 1
                self.next_block = True
        return fall_time

    def add_current_block_to_grid(self):
        """Add current_block to grid."""
        piece_pos = self.current_block.get_relative_positions()
        for i in range(len(piece_pos)):
            x, y = piece_pos[i]
            if y > -1:
                self.grid[y][x] = self.current_block.color

    def end_current_block_motion(self):
        """
        Shift focus to next block.
        
        Add positions taken by current_block to filled_positions.
        Regenerate current_block.
        
        """
        piece_pos = self.current_block.get_relative_positions()
        if self.next_block:
            for pos in piece_pos:
                p = (pos[0], pos[1])
                self.filled_positions[p] = self.current_block.color
            self.current_block = Block()
            self.nr_blocks += 1
            self.next_block = False
            self.clear_any_filled_rows()


class BoardView:
    """
    Visualization of Board.

    Args:
        surface (pygame.Surface): Display surface.
        board (Board): Object of type Board.
    
    Attributes:
        surface (pygame.Surface): Display surface.
        board (Board): Object of type Board.
    
    """

    def __init__(self, surface, board):
        self.surface = surface
        self.board = board

    def draw_text(self, text, size, color, position):
        """
        Draw text of specified size and color onto surface.
        
        Args:
            text (string): String to be displayed.
            size (int): Size of text.
            color (3 element tuple): Color of text.
            position (tuple): Coordinates at which to place label.
        
        """
        font = pygame.font.SysFont('comicsans', size, bold=True)
        label = font.render(text, 1, color)
        self.surface.blit(label, (position[0] - (label.get_width() / 2), position[1] - label.get_height() / 2))

    def draw_grid(self, row, col):
        """
        Draw grid onto surface.
        
        Args:
            row (int): Number of rows.
            col (int): Number of columns.

        """
        sx = TOP_LEFT_X
        sy = TOP_LEFT_Y
        for i in range(row):
            pygame.draw.line(self.surface, (128,128,128), (sx, sy + i*30), (sx + BOARD_WIDTH, sy + i * 30))  # horizontal lines
            for j in range(col):
                pygame.draw.line(self.surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + BOARD_HEIGHT))  # vertical lines

    def draw_window(self):
        """Draw window and contents."""
        surface_color = pygame.colordict.THECOLORS.get("black")
        self.surface.fill(surface_color)

        for i in range(len(self.board.grid)):
            for j in range(len(self.board.grid[i])):
                pygame.draw.rect(self.surface, self.board.grid[i][j], (TOP_LEFT_X + j * 30, TOP_LEFT_Y + i * 30, 30, 30), 0)

        self.draw_grid(20, 10)

        pygame.draw.rect(self.surface, (255, 0, 0), (TOP_LEFT_X, TOP_LEFT_Y, BOARD_WIDTH, BOARD_HEIGHT), 5)


class PythonBlockDrop:
    """Tetris game."""

    def __init__(self):
        pygame.font.init()
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.board = Board()
        self.boardview = BoardView(self.surface, self.board)
        self.menu_loop()

    def game_event_handler(self, run):
        """Handle in game events.
        
        Args:
            run (boolean): Loop control flag.

        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.board.current_block.x -= 1
                    if not self.board.is_valid():
                        self.board.current_block.x += 1
                elif event.key == pygame.K_RIGHT:
                    self.board.current_block.x += 1
                    if not self.board.is_valid():
                        self.board.current_block.x -= 1
                elif event.key == pygame.K_UP:
                    self.board.current_block.rotation = self.board.current_block.rotation + 1 % len(self.board.current_block.piece)
                    if not self.board.is_valid():
                        self.board.current_block.rotation = self.board.current_block.rotation - 1 % len(self.board.current_block.piece)
                elif event.key == pygame.K_DOWN:
                    self.board.current_block.y += 2
                    if not self.board.is_valid():
                        self.board.current_block.y -= 2
        return run

    def game_loop(self):
        """PythonBlockDrop game loop."""
        run = True
        clock = pygame.time.Clock()
        fall_time = 0

        while run:
            fall_time += clock.get_rawtime()
            clock.tick()


            # schedule changes by shifting them to grid

            self.board.recreate_grid()
            fall_time = self.board.block_motion(fall_time)
            run = self.game_event_handler(run)
            self.board.add_current_block_to_grid()
            self.board.end_current_block_motion()

            # push changes applied to grid to display

            self.boardview.draw_window()
            pygame.display.update()
            run = not self.board.is_game_over()
        text_position = (TOP_LEFT_X + BOARD_WIDTH / 2,
                        TOP_LEFT_Y + BOARD_HEIGHT / 2)
        self.boardview.draw_text("You Lost", 40, (255,255,255), text_position)
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
            

    def menu_loop(self):
        """PythonBlockDrop menu loop."""
        run = True
        while run:
            self.surface.fill((0,0,0))
            text_position = (TOP_LEFT_X + BOARD_WIDTH / 2,
                             TOP_LEFT_Y + BOARD_HEIGHT / 2)
            self.boardview.draw_text('Press any key to begin.', 60, (255, 255, 255), text_position)
            pygame.display.update()
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    self.game_loop()

        pygame.display.update()
        pygame.time.delay(2000)

                
            
        pygame.quit()

if __name__ == "__main__":
    PythonBlockDrop()
