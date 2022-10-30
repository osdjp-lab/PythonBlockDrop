import pygame

# Global constants

window_width = 800
window_height = 750


def draw_window(surface):
    """Draw the game window.

    Args:
        surface (pygame.Surface): Display surface.
    
    """
    surface_fill_color = pygame.colordict.THECOLORS.get("black")
    surface.fill(surface_fill_color)


def main():
    """The main function of the PythonBlockDrop game."""
    pygame.font.init()
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Tetris')
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
        draw_window(window)


if __name__ == "__main__":
    main()
