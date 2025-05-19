import pygame
import asyncio
import platform

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

# Define level elements as Rects for platforms
platforms = [
    pygame.Rect(0, 550, LEVEL_WIDTH, 50),          # Ground
    pygame.Rect(200, 400, 200, PLATFORM_HEIGHT),   # Floating platforms
    pygame.Rect(600, 300, 200, PLATFORM_HEIGHT),
    pygame.Rect(1000, 450, 150, PLATFORM_HEIGHT),
    pygame.Rect(1200, 350, 100, PLATFORM_HEIGHT),
]

enemies = [
    [300, 550 - ENEMY_HEIGHT, 1],  # [x, y, direction] (1 for right, -1 for left)
    [700, 550 - ENEMY_HEIGHT, -1],
]

powerups = [
    [400, 400 - POWERUP_HEIGHT],  # [x, y]
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
button_text_pos = (button_rect.centerx - button_text.get_width() // 2, 
                  button_rect.centery - button_text.get_height() // 2)

# Game loop setup
running = True
clock = pygame.time.Clock()
FPS = 60

def setup():
    global running, player_x, player_y, player_vx, player_vy, player_size, on_ground, camera_offset, state, enemies, powerups
    # Reset game state
    player_x = 100
    player_y = 550 - PLAYER_HEIGHT
    player_vx = 0
    player_vy = 0
    player_size = 1
    on_ground = False
    camera_offset = 0
    state = "menu"
    enemies = [
        [300, 550 - ENEMY_HEIGHT, 1],
        [700, 550 - ENEMY_HEIGHT, -1],
    ]
    powerups = [
        [400, 400 - POWERUP_HEIGHT],
    ]
    running = True

def update_loop():
    global running, state, player_x, player_y, player_vx, player_vy, player_size, on_ground, camera_offset

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

        # Cap horizontal speed
        player_vx = max(-PLAYER_MAX_SPEED, min(PLAYER_MAX_SPEED, player_vx))

        # Jumping
        if keys[pygame.K_UP] and on_ground:
            player_vy = -PLAYER_JUMP_STRENGTH
            on_ground = False

        # Calculate current player size
        current_player_width = PLAYER_WIDTH * player_size
        current_player_height = PLAYER_HEIGHT * player_size

        # Update horizontal position
        player_x += player_vx

        # Prevent going outside level
        if player_x < 0:
            player_x = 0
            player_vx = 0
        elif player_x > LEVEL_WIDTH - current_player_width:
            player_x = LEVEL_WIDTH - current_player_width
            player_vx = 0

        # Update vertical position
        player_y += player_vy

        # Create player rect
        player_rect = pygame.Rect(player_x, player_y, current_player_width, current_player_height)

        # Check for vertical collisions with platforms
        on_ground = False
        for platform in platforms:
            if player_rect.colliderect(platform) and player_vy > 0:
                player_y = platform.top - current_player_height
                player_vy = 0
                on_ground = True

        # Apply gravity if not on ground
        if not on_ground:
            player_vy += PLAYER_GRAVITY

        # Enemy movement
        for enemy in enemies:
            enemy[0] += ENEMY_SPEED * enemy[2]
            if enemy[0] <= 0 or enemy[0] >= LEVEL_WIDTH - ENEMY_WIDTH:
                enemy[2] *= -1

        # Enemy collision
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], ENEMY_WIDTH, ENEMY_HEIGHT)
            if player_rect.colliderect(enemy_rect):
                if player_rect.bottom <= enemy_rect.centery:
                    # Jump on enemy
                    enemies.remove(enemy)
                    player_vy = -PLAYER_JUMP_STRENGTH / 2  # Small bounce
                else:
                    # Take damage
                    if player_size > 1:
                        player_size = 1
                    else:
                        running = False  # Game over

        # Power-up collection
        for powerup in powerups[:]:
            powerup_rect = pygame.Rect(powerup[0], powerup[1], POWERUP_WIDTH, POWERUP_HEIGHT)
            if player_rect.colliderect(powerup_rect):
                player_size = 2
                powerups.remove(powerup)

        # Update camera
        camera_offset = max(0, min(player_x - WINDOW_WIDTH // 2, LEVEL_WIDTH - WINDOW_WIDTH))

        # Draw everything
        screen.fill(BLACK)
        for platform in platforms:
            pygame.draw.rect(screen, BLUE, (platform.x - camera_offset, platform.y, platform.width, platform.height))
        for enemy in enemies:
            pygame.draw.rect(screen, BROWN, (enemy[0] - camera_offset, enemy[1], ENEMY_WIDTH, ENEMY_HEIGHT))
        for powerup in powerups:
            pygame.draw.rect(screen, GREEN, (powerup[0] - camera_offset, powerup[1], POWERUP_WIDTH, POWERUP_HEIGHT))
        pygame.draw.rect(screen, RED, (player_x - camera_offset, player_y, current_player_width, current_player_height))

    pygame.display.update()
    clock.tick(FPS)

async def main():
    setup()
    while running:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())

pygame.quit()
