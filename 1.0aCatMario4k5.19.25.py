import pygame

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)  # Empty space
BLUE = (0, 0, 255)  # Walls
RED = (255, 0, 0)   # Player

# Set tile size and grid dimensions
TILE_SIZE = 32
GRID_WIDTH = 10
GRID_HEIGHT = 10
WINDOW_WIDTH = TILE_SIZE * GRID_WIDTH
WINDOW_HEIGHT = TILE_SIZE * GRID_HEIGHT

# Create the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("NSMB-Inspired Pygame Game")

# Hardcoded level data (simulating nsmb.txt content)
level_data = [
    "##########",
    "#        #",
    "#  @     #",
    "#        #",
    "#        #",
    "#        #",
    "#        #",
    "#        #",
    "#        #",
    "##########"
]

# Parse level data into a 2D list
grid = [list(row) for row in level_data]

# Find player's starting position
player_pos = None
for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        if cell == '@':
            player_pos = [x, y]
            grid[y][x] = ' '  # Replace player symbol with empty space
            break
    if player_pos:
        break

# Game loop setup
running = True
clock = pygame.time.Clock()

# Main game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Move player based on arrow keys with collision checking
            if event.key == pygame.K_LEFT and player_pos[0] > 0:
                if grid[player_pos[1]][player_pos[0] - 1] != '#':
                    player_pos[0] -= 1
            elif event.key == pygame.K_RIGHT and player_pos[0] < GRID_WIDTH - 1:
                if grid[player_pos[1]][player_pos[0] + 1] != '#':
                    player_pos[0] += 1
            elif event.key == pygame.K_UP and player_pos[1] > 0:
                if grid[player_pos[1] - 1][player_pos[0]] != '#':
                    player_pos[1] -= 1
            elif event.key == pygame.K_DOWN and player_pos[1] < GRID_HEIGHT - 1:
                if grid[player_pos[1] + 1][player_pos[0]] != '#':
                    player_pos[1] += 1

    # Draw the game
    screen.fill(BLACK)  # Fill background with empty space color

    # Draw walls
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '#':
                pygame.draw.rect(screen, BLUE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw player
    player_x = player_pos[0] * TILE_SIZE + TILE_SIZE // 2
    player_y = player_pos[1] * TILE_SIZE + TILE_SIZE // 2
    pygame.draw.circle(screen, RED, (player_x, player_y), TILE_SIZE // 2)

    # Update display
    pygame.display.flip()

    # Cap frame rate at 60 FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()
