"""
 Pygame base template for opening a window

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/vRB_983kUMc
"""
import pygame
import numpy as np

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 125, 0)
BRIGHT_GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (100, 100, 100)
GRID_H = 500
GRID_W = 500
CELLS_ACROSS = 20
CELLS_DOWN = 20
CELL_W = int(GRID_W / CELLS_ACROSS)
CELL_H = int(GRID_H / CELLS_DOWN)
pygame.init()

# Initial generation of "seed" cell array on grid
prob = .85 # probability of initial grid position being dead
gridA = np.random.rand(CELLS_ACROSS, CELLS_DOWN) > prob

# Set the width and height of the screen [width, height]
size = (GRID_W, GRID_H + 100)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Conway's Game Of Life")

# Loop until the user clicks the close button.
done = False
icon = pygame.image.load('CGOL_Icon.png')
pygame.display.set_icon(icon
                        )
# takes in grid representing current generation of cells and applies game of life rules to each cell
# returns grid representing next generation of cells
def update(grid):
    (height, width) = grid.shape
    next_grid = grid.copy()
    for i in range(height):
        for j in range(width):
            neighbor_count = check_neighbors(grid, i, j)
            if grid[i][j]:
                if (neighbor_count < 2) or (neighbor_count > 3):
                    next_grid[i][j] = False
            elif (not grid[i][j]):
                if neighbor_count == 3:
                    next_grid[i][j] = True
    return next_grid


# returns the number of cells surrounding cell at i, j that are alive
def check_neighbors(grid, i, j):

    (height, width) = grid.shape
    neighbor_count = 0
    # check top
    if i - 1 >= 0 and grid[i - 1][j]:
        neighbor_count += 1
    # check top right
    if (i - 1 >= 0) and (j + 1 < width) and grid[i - 1][j + 1]:
        neighbor_count += 1
    # check right
    if j + 1 < width and grid[i][j + 1]:
        neighbor_count += 1
    # check bottom right
    if (i + 1) < height and (j + 1 < width):
        if grid[i + 1][j + 1]:
            neighbor_count += 1
    # check bottom
    if (i + 1) < height:
        if grid[i + 1][j]:
            neighbor_count += 1
    # check bottom left
    if (i + 1) < height and (j - 1 >= 0):
        if grid[i + 1][j - 1]:
            neighbor_count += 1
    # check left
    if j - 1 >= 0:
        if grid[i][j - 1]:
            neighbor_count += 1
    # check top left
    if (i - 1 >= 0) and (j - 1 >= 0):
        if grid[i - 1][j - 1]:
            neighbor_count += 1

    return neighbor_count


# Used to manage how fast the screen updates
clock = pygame.time.Clock()

click_prev = False


def text_objects(text, font):
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()


def button(msg, x, y, w, h, ic, ac, action=None):
    global click_prev
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))

        if click[0] == 1 and action is not None:
            action()
        else:
            click_prev = False
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    small_text = pygame.font.SysFont("comicsansms", 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)


# boolean of whether time is running or not. flipped by start_stop function called by start stop button
running: bool = True

def printToConsole(input):
    print('You just said' + input)

def start_stop():
    global running
    running = not running


def clear_grid():
    global gridA
    height, width = gridA.shape
    gridA = np.zeros((height, width), dtype=bool)


def flip_cell(row, col):
    global gridA
    cur = gridA[col][row]
    gridA[col][row] = not cur


last = pygame.time.get_ticks()

# cooldown defines milliseconds between cell generations
cooldown = 1000

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game logic should go here

    # button("Clear", 50, 525, 100, 50, green, bright_green, game_loop)
    now = pygame.time.get_ticks()
    if running and now - last >= cooldown:
        last = now
        gridA = update(gridA)

    # --- Screen-clearing code goes here
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)
    for i in range(CELLS_DOWN):
        for j in range(CELLS_ACROSS):
            pygame.draw.rect(screen, GREY, [i * CELL_W, j * CELL_H, CELL_W - 1, CELL_H - 1])

    # logic to allow mouse clicks to toggle alive/dead state of each cell
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    w = CELL_W
    h = CELL_H
    if click[0] == 1:
        if not click_prev:
            click_prev = True
            for row in range(20):
                for col in range(20):
                    x = col * CELL_W
                    y = row * CELL_H
                    if x + w > mouse[0] > x and y + h > mouse[1] > y:
                        flip_cell(row, col)
    else:
        click_prev = False

    # buttons to start/stop game and clear screen
    button("Start/Stop", 50, GRID_H + 25, 100, 50, GREEN, BRIGHT_GREEN, start_stop)
    button("Clear Screen", 250, GRID_H + 25, 150, 50, GREEN, BRIGHT_GREEN, clear_grid)
    # pygame.draw.rect(screen, GREEN, (50, 525, 100, 50))

    # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
    myfont = pygame.font.SysFont("monospace", 15)

    # render text
    # --- Drawing code should go here

    # render all live cells as white squares
    for i in range(20):
        for j in range(20):
            if gridA[i, j]:
                pygame.draw.rect(screen, WHITE, [i * CELL_W, j * CELL_H, CELL_W - 1, CELL_H - 1])

            # add neighbor count on each cell in green
            nc = check_neighbors(gridA, i, j)
            label = myfont.render(str(nc), 1, BRIGHT_GREEN)
            screen.blit(label, (i * 25 + 8, j * 25 + 8))

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()