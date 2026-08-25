import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 650
FPS = 60

# Colors (RGB)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 223, 0)
RED = (231, 76, 60)
BLUE = (52, 152, 219)
BLACK = (0, 0, 0)

# Setup Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Infinite Runner - Subway Style")
clock = pygame.time.Clock()

# Lanes configuration (3 lanes like Subway Surfers)
LANES = [125, 250, 375]
lane_index = 1  # Start in the middle lane

# Player Properties
player_width = 40
player_height = 60
player_y = SCREEN_HEIGHT - 120

# Game Variables
game_speed = 5
score = 0
obstacles = []
coins = []
font = pygame.font.SysFont(None, 36)

# Spawn Timers
SPAWN_OBSTACLE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_OBSTACLE, 1200)  # Spawn obstacle every 1.2 seconds

SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_COIN, 800)  # Spawn coin every 0.8 seconds

running = True
game_over = False

while running:
    screen.fill(GRAY)
    
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and lane_index > 0:
                    lane_index -= 1
                if event.key == pygame.K_RIGHT and lane_index < 2:
                    lane_index += 1
                    
            if event.type == SPAWN_OBSTACLE:
                obs_lane = random.randint(0, 2)
                obstacles.append({"lane": obs_lane, "y": -100})
                
            if event.type == SPAWN_COIN:
                coin_lane = random.randint(0, 2)
                coins.append({"lane": coin_lane, "y": -100})
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # Reset Game
                game_over = False
                obstacles.clear()
                coins.clear()
                score = 0
                game_speed = 5
                lane_index = 1

    if not game_over:
        # Increase speed progressively
        game_speed += 0.001
        score += 1

        # Draw Lanes (Dividers)
        pygame.draw.line(screen, WHITE, (187, 0), (187, SCREEN_HEIGHT), 3)
        pygame.draw.line(screen, WHITE, (312, 0), (312, SCREEN_HEIGHT), 3)

        # Update and Draw Obstacles
        for obs in obstacles[:]:
            obs["y"] += game_speed
            obs_x = LANES[obs["lane"]] - player_width // 2
            obs_rect = pygame.Rect(obs_x, obs["y"], player_width, player_height)
            
            pygame.draw.rect(screen, RED, obs_rect)
            
            # Remove off-screen obstacles
            if obs["y"] > SCREEN_HEIGHT:
                obstacles.remove(obs)

        # Update and Draw Coins
        for coin in coins[:]:
            coin["y"] += game_speed
            coin_x = LANES[coin["lane"]]
            coin_rect = pygame.Rect(coin_x - 15, coin["y"], 30, 30)
            
            pygame.draw.circle(screen, YELLOW, (coin_x, int(coin["y"] + 15)), 15)
            
            # Remove off-screen coins
            if coin["y"] > SCREEN_HEIGHT:
                coins.remove(coin)

        # Draw Player
        player_x = LANES[lane_index] - player_width // 2
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        pygame.draw.rect(screen, BLUE, player_rect)

        # Collision Detection with Obstacles
        for obs in obstacles:
            obs_x = LANES[obs["lane"]] - player_width // 2
            obs_rect = pygame.Rect(obs_x, obs["y"], player_width, player_height)
            if player_rect.colliderect(obs_rect):
                game_over = True

        # Collision Detection with Coins
        for coin in coins[:]:
            coin_x = LANES[coin["lane"]]
            coin_rect = pygame.Rect(coin_x - 15, coin["y"], 30, 30)
            if player_rect.colliderect(coin_rect):
                coins.remove(coin)
                score += 50  # Bonus score for collecting coins

        # Render Score
        score_surface = font.render(f"Score: {int(score)}", True, WHITE)
        screen.blit(score_surface, (20, 20))

    else:
        # Game Over Screen
        game_over_surface = font.render("GAME OVER - Press 'R' to Restart", True, WHITE)
        screen.blit(game_over_surface, (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()