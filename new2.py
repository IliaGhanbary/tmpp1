import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Space Shooter')
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

lose = False

font = pygame.font.SysFont('Arial',  32, 'bold')
score = 0

font2 = pygame.font.SysFont('Arial', 40, 'bold')

clock = pygame.time.Clock()
FPS = 100

background = pygame.image.load("background.png")
backgroung = pygame.transform.scale(background, (800,600))

spaceship = pygame.image.load("spaceship.png")
spaceshipx = 370
changex = 0

bullet = pygame.image.load("bullet.png")
bullety = 540
bulletx = 385
changey = 0

alien = pygame.image.load("alien.png")
alienx = []
alieny = []
changealien = []
sign = [-1,1]
for i in range(6):
    alienx.append(random.randint(0,736))
    alieny.append( random.randint(0,150))
    changealien.append(2 * sign[random.randint(0,1)])

running = True
while running:
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                changex = -3
            if event.key == pygame.K_RIGHT:
                changex = 3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                changex = 0
            if event.key == pygame.K_RIGHT:
                changex = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                changey = -8
        

    spaceshipx += changex
    if(spaceshipx <= 0):
        spaceshipx = 0
    if(spaceshipx >= 736):
        spaceshipx = 736

    bullety += changey
    if(changey == 0):
        bulletx = spaceshipx + 15
    if(bullety < 0):
        bullety = 540
        changey = 0

    for i in range(6):
        alienx[i] += changealien[i]
        if(alienx[i] <= 0):
            alienx[i] = 0
            alieny[i] += 40
            changealien[i] *= -1
        if(alienx[i] >= 736):
            alienx[i] = 736
            alieny[i] += 40
            changealien[i] *= -1


    #collision
    for i in range(6):
        #center of alien
        xca = alienx[i] + 32
        yca = alieny[i] + 32
        #point of bullet
        xb = bulletx + 15
        yb = bullety

        if(((xca - xb) ** 2 + (yca - yb) ** 2)** 0.5 <= 32):
            alienx[i] = random.randint(0,736)
            alieny[i] = random.randint(0,100)
            bulletx = spaceshipx + 15
            bullety = 540
            changey = 0
            score += 1
            
    #game over?
    for i in range(6):
        if(alieny[i] >= 500):
            for j in range(6):
                alieny[j] = 700
                lose = True
                
    
    for i in range(6):
        if(lose == False):
            screen.blit(alien, (alienx[i],alieny[i]))
    screen.blit(bullet, (bulletx, bullety))
    screen.blit(spaceship, (spaceshipx,540))
    
    scoreimg = font.render("Score: " + str(score), True, 'white')
    gameover = font2.render("GAME OVER!", True, 'white')
    if(lose):
        screen.blit(gameover, (300,200))
    screen.blit(scoreimg, (10,10))
    clock.tick(FPS)
    pygame.display.update()