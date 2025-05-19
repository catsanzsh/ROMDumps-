import pygame

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)    # Background
BLUE = (0, 0, 255)   # Platforms
RED = (255, 0, 0)    # Player
BROWN = (139, 69, 19) # Enemies
GREEN = (0, 255, 0)  # Power-ups

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

# Game loop setup
running = True
clock = pygame.time.Clock()

# Main game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    # Cap horizontal speed
    if player_vx > PLAYER_MAX_SPEED:
        player_vx = PLAYER_MAX_SPEED
    elif player_vx < -PLAYER_MAX_SPEED:
        player_vx = -PLAYER_MAX_SPEED

    # Jumping
    if keys[pygame.K_UP] and on_ground:
        player_vy = -PLAYER_JUMP_STRENGTH
        on_ground = False

    # Apply gravity
    player_vy += PLAYER_GRAVITY

    # Update player position
    player_x += player_vx
    player_y += player_vy

    # Adjust player size
    current_player_width = PLAYER_WIDTH * player_size
    current_player_height = PLAYER_HEIGHT * player_size

    # Collision with platforms
    player_rect = pygame.Rect(player_x, player_y, current_player_width, current_player_height)
    on_ground = False
    for plat in platforms:
        plat_rect = pygame.Rect(plat)
        if player_rect.colliderect(plat_rect):
            # Land on platform if falling
            if player_vy > 0 and player_y + current_player_height - player_vy <= plat_rect.top:
                player_y = plat_rect.top - current_player_height
                player_vy = 0
                on_ground = True

    # Prevent falling below ground
    if player_y > 550 - current_player_height:
        player_y = 550 - current_player_height
        player_vy = 0
        on_ground = True

    # Enemy movement and collision
    for enemy in enemies[:]:  # Copy list to modify during iteration
        enemy[0] += ENEMY_SPEED * enemy[2]
        if enemy[0] <= 0 or enemy[0] >= LEVEL_WIDTH - ENEMY_WIDTH:
            enemy[2] *= -1
        enemy_rect = pygame.Rect(enemy[0], enemy[1], ENEMY_WIDTH, ENEMY_HEIGHT)
        if player_rect.colliderect(enemy_rect):
            if player_vy > 0 and player_y + current_player_height - player_vy <= enemy[1]:
                enemies.remove(enemy)  # Defeat enemy
            else:
                if player_size > 1:
                    player_size = 1  # Shrink
                else:
                    running = False  # Game over

    # Power-up collection
    for powerup in powerups[:]:
        powerup_rect = pygame.Rect(powerup[0], powerup[1], POWERUP_WIDTH, POWERUP_HEIGHT)
        if player_rect.colliderect(powerup_rect):
            player_size = 2
            powerups.remove(powerup)

    # Update camera
    if player_x > camera_offset + 400:
        camera_offset = player_x - 400
    elif player_x < camera_offset + 100:
        camera_offset = player_x - 100
    camera_offset = max(0, min(camera_offset, LEVEL_WIDTH - WINDOW_WIDTH))

    # Draw everything
    screen.fill(BLACK)

    # Draw platforms
    for plat in platforms:
        pygame.draw.rect(screen, BLUE, (plat[0] - camera_offset, plat[1], plat[2], plat[3]))

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, BROWN, (enemy[0] - camera_offset, enemy[1], ENEMY_WIDTH, ENEMY_HEIGHT))

    # Draw power-ups
    for powerup in powerups:
        pygame.draw.rect(screen, GREEN, (powerup[0] - camera_offset, powerup[1], POWERUP_WIDTH, POWERUP_HEIGHT))

    # Draw player
    pygame.draw.rect(screen, RED, (player_x - camera_offset, player_y, current_player_width, current_player_height))

    # Update display
    pygame.display.flip()

    # Cap frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
