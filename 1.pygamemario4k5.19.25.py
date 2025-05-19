import pygame

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)    # Background
BLUE = (0, 0, 255)   # Platforms
RED = (255, 0, 0)    # Player
BROWN = (139, 69, 19) # Enemies
GREEN = (0, 255, 0)  # Power-ups
LIGHT_BLUE = (173, 216, 230)  # Menu background

# Window and level size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
LEVEL_WIDTH = 1600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("NSMB 2006-Inspired Pygame Platformer")

# Player properties
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 32
PLAYER_GRAVITY = 0.5
PLAYER_JUMP_STRENGTH = 10
PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = 0.2
PLAYER_MAX_SPEED = 5

# Enemy properties
ENEMY_WIDTH = 32
ENEMY_HEIGHT = 32
ENEMY_SPEED = 2

# Power-up properties
POWERUP_WIDTH = 32
POWERUP_HEIGHT = 32

# Platform properties
PLATFORM_HEIGHT = 16

# Define level elements
platforms = [
    # Ground
    (0, 550, LEVEL_WIDTH, 50),
    # Floating platforms
    (200, 400, 200, PLATFORM_HEIGHT),
    (600, 300, 200, PLATFORM_HEIGHT),
    (1000, 450, 150, PLATFORM_HEIGHT),
    (1200, 350, 100, PLATFORM_HEIGHT),
]

enemies = [
    # [x, y, direction] (1 for right, -1 for left)
    [300, 550 - ENEMY_HEIGHT, 1],
    [700, 550 - ENEMY_HEIGHT, -1],
]

powerups = [
    # [x, y]
    [400, 400 - POWERUP_HEIGHT],
]

# Player initial state
player_x = 100
player_y = 550 - PLAYER_HEIGHT
player_vx = 0
player_vy = 0
player_size = 1  # 1 for small, 2 for large
on_ground = False

# Camera offset
camera_offset = 0

# Game state
state = "menu"

# Menu elements
font_title = pygame.font.SysFont("Arial", 48)
title_text = font_title.render("NSMB Pygame Edition", True, BLACK)
title_pos = (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 100)

font_button = pygame.font.SysFont("Arial", 32)
button_text = font_button.render("Start Game", True, BLACK)
button_rect = pygame.Rect(200, 400, 400, 100)
button_text_pos = (button_rect.centerx - button_text.get_width() // 2, button_rect.centery - button_text.get_height() // 2)

# Game loop setup
running = True
clock = pygame.time.Clock()

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif state == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                state = "game"

    if state == "menu":
        # Draw menu
        screen.fill(LIGHT_BLUE)
        screen.blit(title_text, title_pos)
        pygame.draw.rect(screen, BLUE, button_rect)
        screen.blit(button_text, button_text_pos)
    elif state == "game":
        # Get keys pressed
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_LEFT]:
            player_vx -= PLAYER_ACCELERATION
        elif keys[pygame.K_RIGHT]:
            player_vx += PLAYER_ACCELERATION
        else:
            # Apply friction
            if player_vx > 0:
                player_vx -= PLAYER_FRICTION
                if player_vx < 0:
                    player_vx = 0
            elif player_vx < 0:
                player_vx += PLAYER_FRICTION
                if player_vx > 0:
                    player_vx = 0

        # Vertical movement
        if keys[pygame.K_UP] and on_ground:
            player_vy = -PLAYER_JUMP_STRENGTH
            on_ground = False

        # Apply gravity
        player_vy += PLAYER_GRAVITY

        # Update player position
        player_x += player_vx
        player_y += player_vy

        # Check for collision with platforms
        for platform in platforms:
            if (player_x + PLAYER_WIDTH > platform[0] and player_x < platform[0] + platform[2] and
                player_y + PLAYER_HEIGHT > platform[1] and player_y + PLAYER_HEIGHT < platform[1] + platform[3]):
                if player_vy > 0:
                    player_y = platform[1] - PLAYER_HEIGHT
                    player_vy = 0
                    on_ground = True
                elif player_vy < 0:
                    player_vy = 0

        # Check for collision with enemies
        for enemy in enemies:
            if (player_x + PLAYER_WIDTH > enemy[0] and player_x < enemy[0] + ENEMY_WIDTH and
                player_y + PLAYER_HEIGHT > enemy[1] and player_y < enemy[1] + ENEMY_HEIGHT):
                player_vy = -PLAYER_JUMP_STRENGTH
                on_ground = False

        # Check for collision with power-ups
        for powerup in powerups:
            if (player_x + PLAYER_WIDTH > powerup[0] and player_x < powerup[0] + POWERUP_WIDTH and
                player_y + PLAYER_HEIGHT > powerup[1] and player_y < powerup[1] + POWERUP_HEIGHT):
                powerups.remove(powerup)

        # Update camera
        camera_offset = player_x - WINDOW_WIDTH // 2

        # Draw game
        screen.fill(BLACK)
        for platform in platforms:
            pygame.draw.rect(screen, BLUE, platform)
        for enemy in enemies:
            pygame.draw.rect(screen, BROWN, (enemy[0] - camera_offset, enemy[1], ENEMY_WIDTH, ENEMY_HEIGHT))
        for powerup in powerups:
            pygame.draw.rect(screen, GREEN, (powerup[0] - camera_offset, powerup[1], POWERUP_WIDTH, POWERUP_HEIGHT))
        pygame.draw.rect(screen, RED, (player_x - camera_offset, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

    pygame.display.update()
    clock.tick(60)

pygame.quit() 
