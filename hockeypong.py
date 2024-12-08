import pygame
import sys

# Initialize Pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hockey Pong")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Game settings
BAR_WIDTH, BAR_HEIGHT = 10, 100
PUCK_RADIUS = 10
BAR_SPEED = 5
puck_speed_x, puck_speed_y = 4, 4
IA_SPEED = 4  # Speed of the AI paddle
FPS = 60  # Limit FPS to 60

# Horizontal positions for defense and attack bars
PLAYER1_DEFENSE_X = 50  # Defensive bar for player 1, close to the left goal
PLAYER1_ATTACK_X = WIDTH // 2 + 100  # Attack bar for player 1 in the opponent's half
PLAYER2_DEFENSE_X = WIDTH - 50 - BAR_WIDTH  # Defensive bar for player 2, close to the right goal
PLAYER2_ATTACK_X = WIDTH // 2 - 100 - BAR_WIDTH  # Attack bar for player 2 in the opponent's half

# Initial vertical positions (centered)
player1_y_defense = HEIGHT // 2 - BAR_HEIGHT // 2
player1_y_attack = HEIGHT // 2 - BAR_HEIGHT // 2
player2_y_defense = HEIGHT // 2 - BAR_HEIGHT // 2
player2_y_attack = HEIGHT // 2 - BAR_HEIGHT // 2
puck_x, puck_y = WIDTH // 2, HEIGHT // 2

# Track the previous x position of the puck for IA attack behavior
previous_puck_x = puck_x

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player 1 paddle movement (left side)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_z] and player1_y_defense > 0:  # Use 'z' for AZERTY layout
        player1_y_defense -= BAR_SPEED
        player1_y_attack -= BAR_SPEED  # Move attack bar with the same controls
    if keys[pygame.K_s] and player1_y_defense < HEIGHT - BAR_HEIGHT:
        player1_y_defense += BAR_SPEED
        player1_y_attack += BAR_SPEED  # Move attack bar with the same controls

    # AI movement for player 2 (right side)
    # Defense bar follows the puck regardless of its origin
    if player2_y_defense + BAR_HEIGHT // 2 < puck_y and player2_y_defense < HEIGHT - BAR_HEIGHT:
        player2_y_defense += IA_SPEED
    elif player2_y_defense + BAR_HEIGHT // 2 > puck_y and player2_y_defense > 0:
        player2_y_defense -= IA_SPEED

    # Attack bar behavior
    if puck_x < previous_puck_x:  # Puck is coming from player 1's defense
        # Intercept the puck
        if player2_y_attack + BAR_HEIGHT // 2 < puck_y and player2_y_attack < HEIGHT - BAR_HEIGHT:
            player2_y_attack += IA_SPEED
        elif player2_y_attack + BAR_HEIGHT // 2 > puck_y and player2_y_attack > 0:
            player2_y_attack -= IA_SPEED
    elif puck_x > previous_puck_x:  # Puck is coming from the AI's defense
        # Leave the puck alone, do not move the attack bar
        player2_y_attack = player2_y_attack  # This line is just to signify no action.

    previous_puck_x = puck_x  # Update previous puck position

    # Move the puck
    puck_x += puck_speed_x
    puck_y += puck_speed_y

    # Bounce the puck off the top and bottom edges
    if puck_y - PUCK_RADIUS <= 0 or puck_y + PUCK_RADIUS >= HEIGHT:
        puck_speed_y = -puck_speed_y

    # Bounce the puck off the left and right edges (temporary "goals" walls)
    if puck_x - PUCK_RADIUS <= 0 or puck_x + PUCK_RADIUS >= WIDTH:
        puck_speed_x = -puck_speed_x

    # Solid collisions with each bar
    # Player 1 (blue) bars
    if PLAYER1_DEFENSE_X - PUCK_RADIUS <= puck_x <= PLAYER1_DEFENSE_X + BAR_WIDTH + PUCK_RADIUS and \
            player1_y_defense < puck_y < player1_y_defense + BAR_HEIGHT:
        # Push the puck out of the bar
        if puck_speed_x < 0:  # Coming from left
            puck_x = PLAYER1_DEFENSE_X + BAR_WIDTH + PUCK_RADIUS  # Position outside
        else:  # Coming from right
            puck_x = PLAYER1_DEFENSE_X - PUCK_RADIUS  # Position outside
        puck_speed_x = -puck_speed_x  # Reverse direction

    elif PLAYER1_ATTACK_X - PUCK_RADIUS <= puck_x <= PLAYER1_ATTACK_X + BAR_WIDTH + PUCK_RADIUS and \
            player1_y_attack < puck_y < player1_y_attack + BAR_HEIGHT:
        # Push the puck out of the bar
        if puck_speed_x < 0:  # Coming from left
            puck_x = PLAYER1_ATTACK_X + BAR_WIDTH + PUCK_RADIUS  # Position outside
        else:  # Coming from right
            puck_x = PLAYER1_ATTACK_X - PUCK_RADIUS  # Position outside
        puck_speed_x = -puck_speed_x  # Reverse direction

    # Player 2 (red) bars
    if PLAYER2_DEFENSE_X - PUCK_RADIUS <= puck_x <= PLAYER2_DEFENSE_X + BAR_WIDTH + PUCK_RADIUS and \
            player2_y_defense < puck_y < player2_y_defense + BAR_HEIGHT:
        # Push the puck out of the bar
        if puck_speed_x > 0:  # Coming from right
            puck_x = PLAYER2_DEFENSE_X - PUCK_RADIUS  # Position outside
        else:  # Coming from left
            puck_x = PLAYER2_DEFENSE_X + BAR_WIDTH + PUCK_RADIUS  # Position outside
        puck_speed_x = -puck_speed_x  # Reverse direction

    elif PLAYER2_ATTACK_X - PUCK_RADIUS <= puck_x <= PLAYER2_ATTACK_X + BAR_WIDTH + PUCK_RADIUS and \
            player2_y_attack < puck_y < player2_y_attack + BAR_HEIGHT:
        # Push the puck out of the bar
        if puck_speed_x > 0:  # Coming from right
            puck_x = PLAYER2_ATTACK_X - PUCK_RADIUS  # Position outside
        else:  # Coming from left
            puck_x = PLAYER2_ATTACK_X + BAR_WIDTH + PUCK_RADIUS  # Position outside
        puck_speed_x = -puck_speed_x  # Reverse direction

    # Render
    window.fill(BLACK)
    # Draw Team 1 paddles in blue (defense and attack)
    pygame.draw.rect(window, BLUE, (PLAYER1_DEFENSE_X, player1_y_defense, BAR_WIDTH, BAR_HEIGHT))  # Defense
    pygame.draw.rect(window, BLUE, (PLAYER1_ATTACK_X, player1_y_attack, BAR_WIDTH, BAR_HEIGHT))  # Attack
    # Draw Team 2 paddles in red (defense and attack)
    pygame.draw.rect(window, RED, (PLAYER2_DEFENSE_X, player2_y_defense, BAR_WIDTH, BAR_HEIGHT))  # Defense
    pygame.draw.rect(window, RED, (PLAYER2_ATTACK_X, player2_y_attack, BAR_WIDTH, BAR_HEIGHT))  # Attack
    # Draw the puck
    pygame.draw.circle(window, WHITE, (puck_x, puck_y), PUCK_RADIUS)
    # Draw the center line
    pygame.draw.line(window, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 1)

    pygame.display.flip()
    clock.tick(FPS)  # Limit FPS to 60

pygame.quit()
sys.exit()