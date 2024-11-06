import pygame
import sys
import math
import random

# Initialize pygame modules
pygame.init()

# Screen dimensions and settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height)) #creates a window or screen
pygame.display.set_caption("Pac-Man Game") #window tittle

# Colors
background_color = (0,0,0) #Black
pacman_color = (255, 255, 0) #Yellow
ghost_color = (255, 0, 0) #Red
wall_color = (0, 0, 255) #Blue
dot_color = (0, 255, 255) #White

# Pac-Man settings
pacman_radius = 20
pacman_x, pacman_y = 80, 100   # Initial position
pacman_speed = 10
mouth_angle = 0 # For opening and closing the mouth
mouth_opening = 15 # Angle of mouth opening

# Ghost settings
ghost_radius = 20
# initializes a list named ghosts. Each element of this list will represent a ghost in the game.
ghosts = [
#randomly generates the coordinates of the pacman to ensure movement
    {"x": random.randint(200, width - 100), "y": random.randint(100, height - 100), "speed_x": -3, "speed_y": 3},
    {"x": random.randint(200, width - 100), "y": random.randint(100, height - 100), "speed_x": 5, "speed_y": -2},
    {"x": random.randint(200, width - 100), "y": random.randint(100, height - 100), "speed_x": 4, "speed_y": 4}
]
# Wall dimensions with an opening
walls = [
    pygame.Rect(100, 100, 250, 10),  # Top left section of top wall
    pygame.Rect(450, 100, 250, 10),  # Top right section of top wall (gap in the middle)
    pygame.Rect(100, 490, 600, 10),  # Bottom horizontal wall
    pygame.Rect(100, 100, 10, 400),  # Left vertical wall
    pygame.Rect(690, 100, 10, 400)   # Right vertical wall
]

# Dot coordinates List Comprehension: The code uses a list comprehension to create a list of coordinates,
# each representing a dot's position. List comprehensions are a concise way to create lists in Python.
dots = [(200 + i * 50, 300) for i in range(10)]
score = 0

#Sets up the font used to display the score and game-over message on the screen.
# Fonts
font = pygame.font.Font(None, 36)

#Draws Pac-Man with a "mouth" based on the current angle (mouth_angle).
#This creates the effect of Pac-Man’s chomping by dynamically adjusting the opening angle.
def draw_pacman(x, y, radius, angle):
    start_angle = math.radians(angle)
    end_angle = 2 * math.pi - start_angle
    pygame.draw.circle(screen, pacman_color, (int(x), int(y)), radius)

    #Draws the mouth as a triangle (wedge) that overlays part of the circle.
    pygame.draw.polygon(screen, background_color, [
        (x, y),
        (x + radius * math.cos(start_angle), y - radius * math.sin(start_angle)),
        (x + radius * math.cos(end_angle), y - radius * math.sin(end_angle))
    ])

# Game loop
clock = pygame.time.Clock()
game_over = False
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Only proceed if game is not over
    if not game_over:
        # Movement controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pacman_x -= pacman_speed
        if keys[pygame.K_RIGHT]:
            pacman_x += pacman_speed
        if keys[pygame.K_UP]:
            pacman_y -= pacman_speed
        if keys[pygame.K_DOWN]:
            pacman_y += pacman_speed

        # Check wall collisions for Pac-Man
        pacman_rect = pygame.Rect(pacman_x - pacman_radius, pacman_y - pacman_radius,
                                  pacman_radius * 2, pacman_radius * 2)
        for wall in walls:
            if pacman_rect.colliderect(wall):
                # Move Pac-Man back if he collides with a wall
                if keys[pygame.K_LEFT]:
                    pacman_x += pacman_speed
                if keys[pygame.K_RIGHT]:
                    pacman_x -= pacman_speed
                if keys[pygame.K_UP]:
                    pacman_y += pacman_speed
                if keys[pygame.K_DOWN]:
                    pacman_y -= pacman_speed

        #Alternates the angle of Pac-Man's mouth for a chomping effect using a timer by pygame's internal clock
        mouth_angle = mouth_opening if (pygame.time.get_ticks() // 100) % 2 == 0 else 0

        # Move ghosts
        for ghost in ghosts:
            ghost["x"] += ghost["speed_x"]
            ghost["y"] += ghost["speed_y"]
            # Reverse direction if a ghost hits a wall
            if ghost["x" ] - ghost_radius < 100 or ghost["x"] + ghost_radius > 700:
                ghost["speed_x"] = -ghost["speed_x"]
            if ghost["y"] - ghost_radius < 100 or ghost["y"] + ghost_radius > 500:
                ghost["speed_y"] = -ghost["speed_y"]

            # Check for collision with Pac-Man (Game Over Condition)
            if math.hypot(pacman_x - ghost["x"], pacman_y - ghost["y"]) < pacman_radius + ghost_radius:
                game_over = True

        # Clear screen
        screen.fill(background_color)

        # Draw walls with an opening in the top wall
        for wall in walls:
            pygame.draw.rect(screen, wall_color, wall)

        # Draw dots and remove them if Pac-Man "eats" them
        new_dots = []
        for dot_x, dot_y in dots:
            if math.hypot(pacman_x - dot_x, pacman_y - dot_y) < pacman_radius:
                score += 10  # Increase score
                continue  # Pac-Man eats the score multiplier ball
            pygame.draw.circle(screen, dot_color, (dot_x, dot_y), 5)
            new_dots.append((dot_x, dot_y))
        dots = new_dots

        # Draw Pac-Man
        draw_pacman(pacman_x, pacman_y, pacman_radius, mouth_angle)

        # Draw ghosts
        for ghost in ghosts:
            pygame.draw.circle(screen, ghost_color, (int(ghost["x"]), int(ghost["y"])), ghost_radius)

        # Display score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Check if all dots are eaten (Winning Condition)
        if not dots:
            game_over = True

    else:
        # Display game over message
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        screen.blit(game_over_text, (width // 2 - 80, height // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    # Update display
    pygame.display.flip()
    clock.tick(30)  # Limit the frame rat
