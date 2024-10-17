import pygame
import sys

import random

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # Add GREEN
BLUE = (0, 0, 255)   # Add BLUE
YELLOW = (255, 255, 0)  # Add YELLOW

def draw_fireworks(screen):
    for _ in range(10):  # You can increase the number of fireworks
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        radius = random.randint(20, 100)
        color = random.choice([RED, GREEN, BLUE, YELLOW])
        pygame.draw.circle(screen, color, (x, y), radius, 3)  # Draw circles for fireworks

# Define simple stick figure dance positions
def draw_dancer(screen, x, y, frame):
    if frame % 2 == 0:
        pygame.draw.line(screen, WHITE, (x, y), (x - 10, y + 30), 5)  # Left leg
        pygame.draw.line(screen, WHITE, (x, y), (x + 10, y + 30), 5)  # Right leg
    else:
        pygame.draw.line(screen, WHITE, (x, y), (x - 15, y + 30), 5)  # Alternate leg positions
        pygame.draw.line(screen, WHITE, (x, y), (x + 15, y + 30), 5)
    
    pygame.draw.circle(screen, WHITE, (x, y - 20), 10)  # Head
    pygame.draw.line(screen, WHITE, (x, y - 10), (x, y), 5)  # Body
    pygame.draw.line(screen, WHITE, (x, y - 10), (x - 20, y - 30), 5)  # Left arm
    pygame.draw.line(screen, WHITE, (x, y - 10), (x + 20, y - 30), 5)  # Right arm

def show_victory_scene(screen):
    clock = pygame.time.Clock()
    frame = 0
    running = True
    while running:
        screen.fill(BLACK)
        draw_fireworks(screen)
        draw_dancer(screen, 300, 400, frame)  # Example dancer position
        draw_dancer(screen, 500, 400, frame)
        
        pygame.display.flip()
        frame += 1
        clock.tick(10)  # Control frame rate
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()



# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Brick Breaker')

# Paddle properties
paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 30, 120, 10)
paddle_speed = 10

# Ball properties
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)
ball_speed_x = 5
ball_speed_y = -5

# Brick properties
bricks = [pygame.Rect(60 + i * 70, 40 + j * 30, 60, 20) for i in range(10) for j in range(5)]

# Game loop
while True:
    screen.fill(BLACK)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed
    
    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    
    # Ball collision with walls
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed_x = -ball_speed_x
    if ball.top <= 0:
        ball_speed_y = -ball_speed_y
    if ball.colliderect(paddle):
        ball_speed_y = -ball_speed_y
    
    # Ball collision with bricks
    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed_y = -ball_speed_y
    
    # Ball goes out of bounds
    if ball.bottom >= HEIGHT:
        print("Game Over")
        pygame.quit()
        sys.exit()
    
    # Check if all bricks are destroyed
    if not bricks:
        show_victory_scene(screen)  # Show the victory scene
        pygame.quit()
        sys.exit()
    
    # Draw paddle, ball, and bricks
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.ellipse(screen, RED, ball)
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)
    
    # Update display
    pygame.display.flip()
    pygame.time.delay(30)