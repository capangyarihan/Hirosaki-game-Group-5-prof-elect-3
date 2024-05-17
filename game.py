import pygame
import math
import random

import onlyButton

from pygame import mixer

pygame.init()

#-------------------------------GAME WINDOW------------------------------------------------------
screen = pygame.display.set_mode((800, 500))

#------BACKGROUND-----
background = pygame.image.load("Hirosaki files/bground.jpg")

#------BACKGROUND MUSIC-----
mixer.music.load('Hirosaki files/Battotai_mix.wav')
mixer.music.play(-1)

#------TITLE-----------
pygame.display.set_caption("HIROSAKI")
icon = pygame.image.load("Hirosaki files/HIROSAKI_2.jpg")
pygame.display.set_icon(icon)

#--------Player------------------
playerImg = pygame.image.load('Hirosaki files/B-29_player.png')
playerImg = pygame.transform.scale(playerImg, (120, 90))
playerX = 370
playerY = 400
playerX_change = 0

#----------------------------------------------Enemy--------------------------------------------------
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

def spawn_enemies(num_of_enemies):
    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('Hirosaki files/enemy-japan.png'))
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 50))
        enemyX_change.append(0.2)
        enemyY_change.append(40)

spawn_enemies(num_of_enemies)

#-------------------BULLET------------------------------------------------------------------
bulletImg = pygame.image.load('Hirosaki files/bullet4.png')
bulletImg = pygame.transform.scale(bulletImg, (50, 70))
bulletX = 0
bulletY = 400
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

#-------------------------SCORES & ROUNDS------------------------------------
score_value = 0
round_number = 1
next_round_score = 20
font = pygame.font.Font('freesansbold.ttf', 30)
textX = 10
textY = 10

#-----------------------------GAME OVER TEXT----------------------------------
over_font = pygame.font.Font('freesansbold.ttf', 64)


#------------------------PAUSE/RESUME/QUIT buttons----------------------
pauseImg = pygame.image.load("PAUSE1.png").convert_alpha()
playImg = pygame.image.load("RESUME3.png").convert_alpha()
playImg = pygame.transform.scale(playImg, (290, 100))
quitImg = pygame.image.load("QUITGAME.png").convert_alpha()

pauseButton = onlyButton.Button(720, 10, pauseImg, 0.5)
playButton = onlyButton.Button(250, 135, playImg, 1)
quitButton = onlyButton.Button(280,250, quitImg,1)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))

def show_round(x, y):
    round_text = font.render("Round: " + str(round_number), True, (0, 0, 0))
    screen.blit(round_text, (x, y + 40))

def game_over():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 230))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 40, y - 40))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 34:
        return True

def next_round():
    global round_number, next_round_score, num_of_enemies
    round_number += 1
    next_round_score += round_number * 5
    num_of_enemies += 2
    spawn_enemies(num_of_enemies)

#-----------------------------------------------GAME LOOP-----------------------------------------------------------------------
run = True
#-----------------------PAUSE ito----------------------------------------
paused=False
while run:
    
    # bg image
    screen.blit(background, (0, 0))


    #----------------------------------------EVENT HANDLER----------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.4
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('Hirosaki files/lazer_shot.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change
    
    if not paused:

        if playerX <= 0:
            playerX = 0
        elif playerX >= 680:
            playerX = 680

        #----------------------------------------------- ENEMY MOVEMENTS------------------------------------------
        for i in range(num_of_enemies):
            if enemyY[i] > 380:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 0.3
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -0.3
                enemyY[i] += enemyY_change[i]

            # --------------------------------------------Collision-------------------------------------------
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_sound = mixer.Sound('Hirosaki files/enemy_explode.wav')
                explosion_sound.play()

                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                
                if score_value >= next_round_score:
                    next_round()

                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 50)

            enemy(enemyX[i], enemyY[i], i)

        #--------------------------------Bullet movement-------------------------------------------------------
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)
        show_round(textX, textY)

    if not paused:
        if pauseButton.draw(screen):
            paused = True
    
    else:
        if playButton.draw(screen):
            paused = False
        elif quitButton.draw(screen):
            run=False
    

    pygame.display.update()
    
pygame.quit()
