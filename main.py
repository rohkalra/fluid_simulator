from typing import Union
import pygame

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CELL_SIZE = 10
NUM_ROWS = SCREEN_HEIGHT // CELL_SIZE
NUM_COLS = SCREEN_WIDTH // CELL_SIZE
LINE_THICKNESS = 2
COLOR_WHITE = 0xFFFFFFFF
COLOR_BLACK = 0x00000000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

Point = pygame.math.Vector2


def draw_gridlines(surface: pygame.Surface):
    for row in range(NUM_ROWS):
        pixels_down = row * CELL_SIZE
        pygame.draw.line(
            surface,
            COLOR_BLACK,
            (0, pixels_down),
            (SCREEN_WIDTH, pixels_down),
            LINE_THICKNESS,
        )
    for col in range(NUM_COLS):
        pygame.draw.line(
            surface,
            COLOR_BLACK,
            (col * CELL_SIZE, 0),
            (col * CELL_SIZE, SCREEN_HEIGHT),
            LINE_THICKNESS,
        )


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(0xFFFFFFFF)
    draw_gridlines(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
