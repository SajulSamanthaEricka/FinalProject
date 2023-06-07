import pygame
import random

# Initialize pygame
pygame.init()

# Set up the game window
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Star Fire Skies: Jet's Asteroid Encounter")

# Load background image
background_image = pygame.image.load("./assets/background.jpg")

# Load sound effects
explosion_sound = pygame.mixer.Sound("./sounds/explosion.mp3")
shoot_sound = pygame.mixer.Sound("./sounds/shoot.mp3")
game_over_sound = pygame.mixer.Sound("./sounds/game over.mp3")

# Load background music
pygame.mixer.music.load("./sounds/background.mp3")
pygame.mixer.music.play(-1)  # Play the background music in a loop

# Load explosion image
explosion_image = pygame.image.load("./assets/explosion.png")

# Set up the player's jet
jet_image = pygame.image.load("./assets/jet.png")
jet_width, jet_height = 64, 64
jet_x = (screen_width - jet_width) // 2
jet_y = screen_height - jet_height - 10
jet_speed = 5

# Set up the bullet (star)
bullet_image = pygame.image.load("./assets/star.png")
bullet_width, bullet_height = 32, 32
bullet_x, bullet_y = 0, 0
bullet_speed = 10
bullet_state = "ready"  # "ready" means the bullet is ready to be fired, "fire" means the bullet is currently moving

# Set up the asteroid
asteroid_image = pygame.image.load("./assets/asteroid.png")
asteroid_width, asteroid_height = 64, 64
asteroid_x = random.randint(0, screen_width - asteroid_width)
asteroid_y = random.randint(50, 200)
asteroid_speed = random.uniform(1, 3)

# Set up the score
score = 0
font = pygame.font.Font("./FreeSans/FreeSansBold.ttf", 32)
text_x, text_y = 10, 10

# Set up game over text
game_over_font = pygame.font.Font("./FreeSans/FreeSansBold.ttf", 64)

# Game loop
running = True
game_over = False

while running:
    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the background
    screen.blit(background_image, (0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                jet_x -= jet_speed
            if event.key == pygame.K_RIGHT:
                jet_x += jet_speed
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = jet_x + jet_width // 2 - bullet_width // 2
                    bullet_y = jet_y
                    bullet_state = "fire"
                    shoot_sound.play()

    # Update the position of the jet
    jet_x = max(0, min(screen_width - jet_width, jet_x))

    # Draw the jet
    screen.blit(jet_image, (jet_x, jet_y))

    # Update the position of the bullet
    if bullet_state == "fire":
        bullet_y -= bullet_speed
        if bullet_y < 0:
            bullet_state = "ready"

        # Draw the bullet
    if bullet_state == "fire":
        screen.blit(bullet_image, (bullet_x, bullet_y))

    # Update the position of the asteroid
    asteroid_y += asteroid_speed
    if asteroid_y > screen_height:
        asteroid_x = random.randint(0, screen_width - asteroid_width)
        asteroid_y = random.randint(50, 200)
        asteroid_speed = random.uniform(1, 3)

    # Check for collision between bullet and asteroid
    if bullet_state == "fire":
        if bullet_x < asteroid_x + asteroid_width and bullet_x + bullet_width > asteroid_x:
            if bullet_y < asteroid_y + asteroid_height and bullet_y + bullet_height > asteroid_y:
                # Collision occurred
                bullet_state = "ready"
                explosion_sound.play()
                score += 10
                asteroid_x = random.randint(0, screen_width - asteroid_width)
                asteroid_y = random.randint(50, 200)
                asteroid_speed = random.uniform(1, 3)
                # Set the position of the explosion
                explosion_x = asteroid_x
                explosion_y = asteroid_y
                # Draw the explosion image
                screen.blit(explosion_image, (explosion_x, explosion_y))
                # Update the position of the explosion
                explosion_x += asteroid_width / 2 - explosion_image.get_width() / 2
                explosion_y += asteroid_height / 2 - explosion_image.get_width() / 2

    # Check for collision between asteroid and jet
    if jet_x < asteroid_x + asteroid_width and jet_x + jet_width > asteroid_x:
        if jet_y < asteroid_y + asteroid_height and jet_y + jet_height > asteroid_y:
            # Collision occurred
            game_over = True
            game_over_sound.play()

    # Draw the asteroid
    screen.blit(asteroid_image, (asteroid_x, asteroid_y))

    # Draw the score
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (text_x, text_y))

    # Game over logic
    if game_over:
        game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(2000)  # Wait for 2 seconds before quitting the game
        running = False

    # Update the display
    pygame.display.update()

# Quit the game
pygame.quit()
