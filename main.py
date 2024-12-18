import pygame
import random
from enum import Enum
from dataclasses import dataclass

pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
CELL_SIZE = 10
NUM_ROWS = SCREEN_HEIGHT // CELL_SIZE
NUM_COLS = SCREEN_WIDTH // CELL_SIZE
LINE_THICKNESS = 2
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_FLUID = (249, 54, 249)


class DrawingMode(Enum):
    SOLID = 1
    FLUID = 2
    DELETION = 3


class DrawingMode:
    SOLID = 1
    FLUID = 2
    DELETION = 3

    modes = {
        SOLID: {"color": COLOR_WHITE, "text": "Mode: Solids"},
        FLUID: {"color": COLOR_FLUID, "text": "Mode: Fluids"},
        DELETION: {"color": COLOR_BLACK, "text": "Mode: Eraser"},
    }

    def __init__(self, mode):
        self.mode = mode
        self.color = self.modes[mode]["color"]
        self.text = self.modes[mode]["text"]


@dataclass
class Cell:
    x: int
    y: int
    state: str


def draw_cell(surface: pygame.Surface, cell: Cell):
    rect = pygame.Rect(cell.x * CELL_SIZE, cell.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    if cell.state == "solid":
        pygame.draw.rect(surface, COLOR_WHITE, rect)
    elif cell.state == "fluid":
        pygame.draw.rect(surface, COLOR_FLUID, rect)


def display_mode_text(surface: pygame.Surface, mode: DrawingMode):
    font = pygame.font.SysFont(None, 36)
    text_surface = font.render(mode.text, True, COLOR_WHITE)
    pygame.draw.rect(surface, COLOR_BLACK, (0, 0, SCREEN_WIDTH, 40))
    surface.blit(text_surface, (10, 10))


def initialize():
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fluid Dynamics Simulator")
    return surface


def simulate_fluids(surface, grid):
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            cell = grid[row][col]
            if cell.state == "fluid":
                if row + 1 < NUM_ROWS and grid[row + 1][col].state == "empty":
                    grid[row + 1][col].state = "fluid"
                    cell.state = "empty"
                    draw_cell(surface, grid[row + 1][col])
                    draw_cell(surface, cell)

                elif (
                    col - 1 >= 0
                    and grid[row][col - 1].state == "empty"
                    and random.random() < 0.1
                ):
                    grid[row][col - 1].state = "fluid"
                    cell.state = "empty"
                    draw_cell(surface, grid[row][col - 1])
                    draw_cell(surface, cell)

                elif (
                    col + 1 < NUM_COLS
                    and grid[row][col + 1].state == "empty"
                    and random.random() < 0.1
                ):
                    grid[row][col + 1].state = "fluid"
                    cell.state = "empty"
                    draw_cell(surface, grid[row][col + 1])
                    draw_cell(surface, cell)


def spread_fluid(surface, grid, x, y, radius=1):
    """Spread fluid in a random pattern around the mouse position (x, y) within the given radius."""
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if dx**2 + dy**2 <= radius**2:
                col, row = (x + dx) % NUM_COLS, (y + dy) % NUM_ROWS
                if grid[row][col].state == "empty" and random.random() < 0.7:
                    grid[row][col].state = "fluid"
                    draw_cell(surface, grid[row][col])


def main_loop(surface):
    clock = pygame.time.Clock()
    running = True
    drawing = False
    mode = DrawingMode(DrawingMode.SOLID)
    grid = [
        [Cell(col, row, "empty") for col in range(NUM_COLS)] for row in range(NUM_ROWS)
    ]

    while running:
        surface.fill(COLOR_BLACK)
        display_mode_text(surface, mode)

        if mode.mode == DrawingMode.FLUID:
            simulate_fluids(surface, grid)

        for row in grid:
            for cell in row:
                if cell.state == "fluid":
                    draw_cell(surface, cell)
                elif cell.state == "solid":
                    draw_cell(surface, cell)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    x, y = event.pos
                    col, row = x // CELL_SIZE, y // CELL_SIZE
                    if mode.mode == DrawingMode.SOLID:
                        grid[row][col].state = "solid"
                    elif mode.mode == DrawingMode.FLUID:
                        spread_fluid(surface, grid, col, row)
                    elif mode.mode == DrawingMode.DELETION:
                        grid[row][col].state = "empty"
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    x, y = event.pos
                    col, row = x // CELL_SIZE, y // CELL_SIZE
                    if mode.mode == DrawingMode.SOLID:
                        grid[row][col].state = "solid"
                    elif mode.mode == DrawingMode.FLUID:
                        spread_fluid(surface, grid, col, row)
                    elif mode.mode == DrawingMode.DELETION:
                        grid[row][col].state = "empty"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if mode.mode == DrawingMode.SOLID:
                        mode = DrawingMode(DrawingMode.FLUID)
                    elif mode.mode == DrawingMode.FLUID:
                        mode = DrawingMode(DrawingMode.DELETION)
                    elif mode.mode == DrawingMode.DELETION:
                        mode = DrawingMode(DrawingMode.SOLID)


def cleanup():
    pygame.quit()


def main():
    screen = initialize()
    try:
        main_loop(screen)
    finally:
        cleanup()


if __name__ == "__main__":
    main()
