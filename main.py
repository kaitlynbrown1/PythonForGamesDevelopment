import pygame
import sys
import os
import random

# Initialize Pygame
pygame.init()

# Constants - shouldn't be changed
WIDTH = 800
HEIGHT = 600
PLAYER_SPEED = 5
BACKGROUND_SPEED = 2
FPS = 60
BULLET_SPEED = 7

# Create a Pygame window and set its dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the window title
pygame.display.set_caption("Space Attack")

# Clock
clock = pygame.time.Clock()

# Background
background = pygame.image.load(os.path.join("assets", "images", "space_bg.png")).convert()
background_rect_one = background.get_rect()
background_rect_one.x = 0 # set the x-axis to 0
background_rect_two = background.get_rect()
background_rect_two.x = WIDTH

# Player
player = pygame.image.load(os.path.join("assets", "images", "spaceship_pl.png")).convert_alpha()
player_rect = player.get_rect() # takes player and puts a rectangle around it
player_rect.midleft = (25, HEIGHT // 2) # 25 in from the left, height divided by 2, double slash = whole number

# Bulltes
bullet = pygame.image.load(os.path.join("assets", "images", "bullet.png")).convert_alpha()
bullet_cooldown = 800
last_bullet_time = 0
bullets = []

# Lives
heart = pygame.image.load(os.path.join("assets", "images", "heart.png")).convert_alpha()
heart_rect = heart.get_rect()
heart_rect.bottomleft = (25, 575)
lives = 3

# Score
spaceship = pygame.image.load(os.path.join("assets", "images", "spaceship.png")).convert_alpha()
spaceship_rect = spaceship.get_rect()
spaceship_rect.topleft = (25, 25)
score = 0
info_font = pygame.font.Font(os.path.join("assets", "fonts", "LuckiestGuy-Regular.ttf"), 32)

# Enemies
enemy_one = pygame.image.load(os.path.join("assets", "images", "spaceship_en_one.png")).convert_alpha() # use alpha if the background is transparent
enemy_two = pygame.image.load(os.path.join("assets", "images", "spaceship_en_two.png")).convert_alpha()
enemy_three = pygame.image.load(os.path.join("assets", "images", "spaceship_en_three.png")).convert_alpha()
enemy_four = pygame.image.load(os.path.join("assets", "images", "spaceship_en_four.png")).convert_alpha()
enemy_five = pygame.image.load(os.path.join("assets", "images", "spaceship_en_five.png")).convert_alpha()
enemy_images = [enemy_one, enemy_two, enemy_three, enemy_four, enemy_five]
enemy_speed = 5
spawn_enemy = 3000
last_enemy_time = 0
enemies = []

# Title Screen
title_font = pygame.font.Font(os.path.join("assets", "fonts", "LuckiestGuy-Regular.ttf"), 72)
inst_font = pygame.font.Font(os.path.join("assets", "fonts", "LuckiestGuy-Regular.ttf"), 32)
title_text = "SPACE ATTACK"
inst_text = "Press ENTER to blast off!"
title_text = title_font.render(title_text, True, "white")
title_rect = title_text.get_rect()
title_rect.center = (WIDTH // 2, 120)
inst_text = inst_font.render(inst_text, True, "white")
inst_rect = inst_text.get_rect()
inst_rect.center = (WIDTH // 2, 480)
title_image = player
title_image_rect = player.get_rect()
title_image_rect.center = (WIDTH // 2, HEIGHT // 2)

# Main game loop
game_over = True
running = True
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Game logic
        # Get Time
        current_time = pygame.time.get_ticks() # retrieve the current time and put it into the time variable, miliseconds
        # Background Scroll
        if background_rect_one.x <= -WIDTH:
            background_rect_one.x = WIDTH
        if background_rect_two.x <= -WIDTH:
            background_rect_two.x = WIDTH
        background_rect_one.x -= BACKGROUND_SPEED
        background_rect_two.x -= BACKGROUND_SPEED

        # Move Player
        # Up
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= PLAYER_SPEED
        # Down
        if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect.y += PLAYER_SPEED

        # Create Bullets
        if keys[pygame.K_SPACE] and current_time - last_bullet_time > bullet_cooldown:
            bullet_image = bullet
            bullet_rect = bullet_image.get_rect()
            bullet_rect.center = player_rect.center
            bullets.append((bullet_image, bullet_rect))
            last_bullet_time = current_time

        # MOVE Bullets
        for bullet_image, bullet_rect in bullets:
            bullet_rect.x += BULLET_SPEED
        bullets = [(bullet_image, bullet_rect) for bullet_image, bulley_rect in bullets if bullet_rect.right < WIDTH]

        # Move Enemies
        for enemy_image, enemy_rect in enemies:
            enemy_rect.x -= enemy_speed
        enemies = [(enemy_image, enemy_rect) for enemy_image, enemy_rect in enemies if enemy_rect.right > 0]

        # Collision Detection
        for enemy_image, enemy_rect in enemies:
            if player_rect.colliderect(enemy_rect):
                lives -= 1
                enemies.remove((enemy_image, enemy_rect))
            for bullet_image, bullet_rect in bullets:
                if bullet_rect.colliderect(enemy_rect) and enemy_rect.right < WIDTH:
                    enemies.remove((enemy_image, enemy_rect))
                    bullets.remove((bullet_image, bullet_rect))
                    score += 1
                    print(score)

        # Spawn Enemies
        if current_time - last_enemy_time > spawn_enemy:
            enemy_image = random.choice(enemy_images)
            enemy_rect = enemy_image.get_rect()
            enemy_rect.x = (WIDTH + enemy_rect.width)
            lane = random.randint(1, 3)
            if lane == 1:
                enemy_rect.y = 0
            if lane == 2:
                enemy_rect.y = (HEIGHT // 2 - (enemy_rect.height // 2))
            if lane == 3:
                enemy_rect.y = (HEIGHT - enemy_rect.height)
            enemies.append((enemy_image, enemy_rect)) # append = add something to a list
            last_enemy_time = current_time

        # Score and Lives
        score_text = info_font.render(f"{score}", True, "white") # f - formated string, pass variable in {}, the value held goes directly into the string    
        if score > 5:
            spawn_enemy = 2500
        if score > 10:
            spawn_enemy = 2000
        if score > 15:
            spawn_enemy = 1500
        if score > 20:
            spawn_enemy = 1000
        
       # if score % 5 == 0:
       #     spawn_enemy -= 500 


        lives_text = info_font.render(f"{lives}", True, "white")
        if lives < 1:
            game_over = True

        # Draw surfaces - reads it from the top down, draws in layers
        screen.blit(background, background_rect_one)
        screen.blit(background, background_rect_two)
        screen.blit(player, player_rect)
        for enemy_image, enemy_rect in enemies:
            screen.blit(enemy_image, enemy_rect)
        for bullet_image, bullet_rect in bullets:
            screen.blit(bullet_image, bullet_rect)
        screen.blit(spaceship, spaceship_rect)
        screen.blit(score_text, (80, 40))
        screen.blit(heart, heart_rect)
        screen.blit(lives_text, (80, 540))
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game_over = False
            enemies.clear()
            bullets.clear()
            player_rect.midleft = (25, HEIGHT // 2)
            lives = 3
            score = 0
        screen.fill("black")
        screen.blit(title_text, title_rect)
        screen.blit(inst_text, inst_rect)
        screen.blit(title_image, title_image_rect)

    # Update dispay
    pygame.display.update()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()

