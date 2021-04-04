import pygame
from pygame import mixer

import random
import math

# initialize the pygame
pygame.init()

# Key values
W_KEY = 119
A_KEY = 97
S_KEY = 115
D_KEY = 100
SPACE_KEY = 32
ENTER_KEY = 13

# create the screen
size = width, height = 800, 600
screen = pygame.display.set_mode(size)

# background
background = pygame.image.load("background.jpg")

#Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Logo
pygame.display.set_caption("Space Invadors")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# PLayer
playerImg = pygame.image.load('ship.png')
playerX = width / 2
playerY = height * 0.8

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

testX = 10
testY = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    over_text = font.render('Score: '+str(score)+"   GameOver",True,(255,255,255))
    screen.blit(over_text,(200,250))

def show_score(x, y):
    scoreBoard = font.render("Score :" + str(score), True, (255, 255, 255))
    screen.blit(scoreBoard, (x, y))


for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, width - enemyImg[i].get_width()))
    enemyY.append(random.randint(0, 0.3 * height))
    enemyX_change.append(0.3)
    enemyY_change.append(0.03)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = playerX + playerImg.get_width() / 2
bulletY = playerY
bulletX_change = 0
bulletY_change = 0.8
bullet_state = "ready"


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(img, x, y):
    screen.blit(img, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y))


def is_collistion(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
    return distance < 27


score = 0
# Game Loop
running = True
while running:
    screen.fill((135, 206, 250))

    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        speed = 0.4
        xChange = yChange = 0
        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                xChange = -speed
            if event.key == pygame.K_RIGHT:
                xChange = speed
            if event.key == pygame.K_UP:
                yChange = -speed
            if event.key == pygame.K_DOWN:
                yChange = speed

            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX + 15
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                xChange = yChange = 0

    # Player Movement
    playerX += xChange
    playerY += yChange

    # restricting boundary
    if playerX < 0:
        playerX = 0
    if playerX > width - playerImg.get_width():
        playerX = width - playerImg.get_width()
    if playerY < 20:
        playerY = 20
    if playerY > height - playerImg.get_height():
        playerY = height - playerImg.get_height()
    player(playerX, playerY)

    # Enemy Movement
    for i in range(num_of_enemies):

        #GameOver
        if enemyY[i]>500:
            for j in range(num_of_enemies):
                enemyY[j]=20000

            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change[i]

        if enemyX[i] < 0:
            enemyX_change[i] = 0.3
        if enemyX[i] > width - enemyImg[i].get_width():
            enemyX_change[i] = -0.3

        enemy(enemyImg[i], enemyX[i], enemyY[i])

        collision = is_collistion(enemyX[i] + enemyImg[i].get_width() / 2, enemyY[i] + enemyImg[i].get_height() / 2,
                                  bulletX,
                                  bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = -10
            bullet_state = "ready"
            score += 1
            print(score)
            enemyX[i] = random.randint(0, width - enemyImg[i].get_width())
            enemyY[i] = random.randint(0, 0.3 * height)

    # bullet movement
    if bullet_state == "fire" and bulletY > 0:
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY < 0:
        bullet_state = 'ready'

    show_score(testX, testY)

    pygame.display.update()
