import pygame
import random
import math

# Initialize the game
pygame.init()

# Create 800 By 600 screen
# Width = 800
# Height = 600
screen = pygame.display.set_mode((800, 600))


# Caption and Icon
pygame.display.set_caption('Space Invaders')

# Get Icon and Set Icon
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Set Background Image
background = pygame.image.load("background.png")


# Set Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

# Set Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)



# Set bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready" # Ready State means the bullet is not visible

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# Gameover
over_font = pygame.font.Font("freesansbold.ttf", 64)

def game_over():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def show_score(x, y):
    score = font.render(f"Score: {str(score_value)}", True, (255,255,255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY, 2))
    return distance <= 27

# Game Loop
running = True
while running:
    # screen.fill method is used to change the background color of a screen, it accepts Tuple
    # RGB
    screen.fill((0,0,0))

    screen.blit(background, (0,0))

    # pygame.event.get() returns events from the queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check whether a key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            # Check whether the space bar is pressed
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletY -= bulletY_change
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                

        # Check whether the key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    playerX += playerX_change

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        enemyX[i] += enemyX_change[i]

         

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    

    # bullet movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"


    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()
