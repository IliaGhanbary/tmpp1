import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('space shooter')
icon = pygame.image.load('1.png')
pygame.display.set_icon(icon)

font = pygame.font.SysFont('Arial', 32, 'bold')
game_over_font = pygame.font.SysFont('Arial', 64, 'bold')

def reset_game():
    global spaceshipx, spaceshipy, bulletx, bullety, bullet_state, alienx, alieny, changealien, score, game_over, moving_left, moving_right
    spaceshipx = 370
    spaceshipy = 540
    bulletx = 0
    bullety = 540
    bullet_state = "ready"
    alienx = []
    alieny = []
    changealien = []
    for i in range(6):
        alienx.append(random.randint(0,736))
        alieny.append(random.randint(0,200))
        changealien.append(2 * random.randint(2,4))
    score = 0
    game_over = False
    moving_left = False
    moving_right = False

reset_game()

background = pygame.image.load("3.jpg")
background = pygame.transform.scale(background, (800, 600))
spaceship = pygame.image.load("1.png")
spaceship = pygame.transform.scale(spaceship,(64,64))
bullet = pygame.image.load("4.png")
bullet = pygame.transform.scale(bullet,(45,45))
alien = pygame.image.load("2.png")
alien = pygame.transform.scale(alien,(64,64))

clock = pygame.time.Clock()
move_speed = 6
game_on = True

while game_on:
    dt = clock.tick(60) / 1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()
            if not game_over:
                if event.key == pygame.K_LEFT:
                    moving_left = True
                if event.key == pygame.K_RIGHT:
                    moving_right = True
                if event.key == pygame.K_SPACE and bullet_state == "ready":
                    bulletx = spaceshipx + 15
                    bullet_state = "fire"
                
        if event.type == pygame.KEYUP and not game_over:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
    
    if not game_over:
        movement = 0
        if moving_left:
            movement -= move_speed
        if moving_right:
            movement += move_speed
            
        spaceshipx += movement * dt * 60
        
        if bullet_state == "fire":
            bullety -= 20 * dt * 60
            if bullety <= 0:
                bullety = 540
                bullet_state = "ready"
        
        if spaceshipx <= 0:
            spaceshipx = 0
        if spaceshipx >= 736:
            spaceshipx = 736

        for i in range(6):
            alienx[i] += changealien[i] * dt * 60
            if alienx[i] <= 0:
                alienx[i] = 0
                alieny[i] += 15
                changealien[i] *= -1
            if alienx[i] >= 736:
                alienx[i] = 736
                alieny[i] += 15
                changealien[i] *= -1    

            xca = alienx[i] + 32
            yca = alieny[i] + 32
            xb = bulletx + 15
            yb = bullety

            if (((xca - xb)**2 + (yca - yb)**2)**0.5 <= 32 and bullet_state == "fire"):
                alienx[i] = random.randint(0,736)
                alieny[i] = random.randint(0,100)
                bullet_state = "ready"
                bullety = 540
                score += 1

            spaceship_center_x = spaceshipx + 32
            spaceship_center_y = spaceshipy + 32
            if (((xca - spaceship_center_x)**2 + (yca - spaceship_center_y)**2)**0.5 <= 32 or alieny[i] >= 500):
                game_over = True

    screen.blit(background, (0, 0))
    
    if not game_over:
        for i in range(6):
            screen.blit(alien, (alienx[i], alieny[i]))
        if bullet_state == "fire":
            screen.blit(bullet, (bulletx, bullety))
        screen.blit(spaceship, (spaceshipx, spaceshipy))
    else:
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        screen.blit(game_over_text, (250, 250))
        screen.blit(restart_text, (280, 350))

    scoreimg = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(scoreimg, (10, 10))

    pygame.display.update()

pygame.quit()