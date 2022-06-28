import pygame
import random
import math

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('arcade-game.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ghost.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 4
bullet_state = "ready"  # you can't see the bullet on the screen

# fire - the bullet is currently moving


# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


def showScore(x, y):
    score = font.render("SCORE: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    # RGB = red green blue
    screen.fill((0, 0, 0))
    # any keystroke pressed on a keyboard is actually an event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keysroke is pressed, check whether its right or left
        if event.type == pygame.KEYDOWN:
            print("a keystroke is pressed")
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
                print("Left arrow is pressed")
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
                print("Right arrow is pressed")
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # Get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                print("Keystroke has been released")
    playerX += playerX_change

    # adding boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    enemyX += enemyX_change

    # enemy movement
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bullet_state = "ready"
            bulletY = 480
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()
