import random
import pygame
from tkinter import *
from tkinter import messagebox
pygame.init()

#Setups Window and Run Status
xLimit = 1000
yLimit = 600
win = pygame.display.set_mode((xLimit, yLimit))
pygame.display.set_caption("First Game")
running = True

#Loads in game images
idleAnimation = []
runningAnimation = []
coinAnimation = []
enemyWalkingAnimation = []
enemyHurtAnimation = []
jumpingAnimation = [pygame.image.load("jumpingAnimation\j0.png"), pygame.image.load("jumpingAnimation\j1.png")]
background = pygame.image.load("Background.png")
buzzsawImage = pygame.image.load("Saw.png")

for i in range(1, 16):
    enemyHurtAnimation.append(pygame.image.load("enemyHit\HIT_Snail_00" + str(i) + "0.png"))

for i in range(0, 8):
    enemyWalkingAnimation.append(pygame.image.load("enemyWalking\MOVE_Snail_00" + str(i) + "0.png"))

for i in range(0, 15):
    coinAnimation.append(pygame.image.load("coinAnimation\\" + str(i) + ".png"))

for i in range(0, 11):
    idleAnimation.append(pygame.image.load("characterIdleAnimation\\" + str(i) + ".png"))

for i in range(0, 17):
    runningAnimation.append(pygame.image.load("runningAnimation\\" + str(i) + ".png"))

#Make the player class with appropriate attributes
class player(object):
    def __init__(self, x, y, width, height, velocity):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.jumping = False
        self.falling = False
        self.right = True
        self.left = False
        self.wasGoingRight = True
        self.isJump = False
        self.jumpCount = 12
        self.walkCount = 0
        self.idleCount = 0
        self.gauge = 0
        self.health = 100
        self.iFrames = 0
        self.bulletDelay = 0

    def draw(self, win):
        #Reset to these with the number of frames you want per animation
        if (mainPlayer.walkCount >= 34):
            mainPlayer.walkCount = 0
        if (mainPlayer.idleCount >= 33):
            mainPlayer.idleCount = 0

            # Walking right
        if mainPlayer.right and not (mainPlayer.jumping or mainPlayer.falling):
            win.blit(runningAnimation[mainPlayer.walkCount // 2], (mainPlayer.x, mainPlayer.y))
            mainPlayer.walkCount += 1
            # Walking left
        if mainPlayer.left and not (mainPlayer.jumping):
            win.blit(pygame.transform.flip(runningAnimation[mainPlayer.walkCount // 2], True, False),
                     (mainPlayer.x, mainPlayer.y))
            mainPlayer.walkCount += 1
            # Idle Animation Right
        if not (mainPlayer.right or mainPlayer.left or mainPlayer.jumping) and mainPlayer.wasGoingRight:
            win.blit(idleAnimation[mainPlayer.idleCount // 4], (mainPlayer.x, mainPlayer.y))
            mainPlayer.idleCount += 1
            # Idle Animation Left
        if not (mainPlayer.right or mainPlayer.jumping or mainPlayer.left) and not mainPlayer.wasGoingRight:
            win.blit(pygame.transform.flip(idleAnimation[mainPlayer.idleCount // 3], True, False),
                     (mainPlayer.x, mainPlayer.y))
            mainPlayer.idleCount += 1
            # Jumping to the right first half
        if (mainPlayer.jumping and mainPlayer.right and not mainPlayer.falling):
            win.blit(jumpingAnimation[0], (mainPlayer.x, mainPlayer.y))
            # Jumping to the right second half
        if (mainPlayer.jumping and mainPlayer.right and mainPlayer.falling):
            win.blit(jumpingAnimation[1], (mainPlayer.x, mainPlayer.y))
            # Jumping to the left first half
        if (mainPlayer.jumping and mainPlayer.left and not mainPlayer.falling):
            win.blit(pygame.transform.flip(jumpingAnimation[0], True, False), (mainPlayer.x, mainPlayer.y))
            # Jumping to the left and second half
        if (mainPlayer.jumping and mainPlayer.left and mainPlayer.falling):
            win.blit(pygame.transform.flip(jumpingAnimation[1], True, False), (mainPlayer.x, mainPlayer.y))
            # Falling Right
        if (mainPlayer.jumping and not mainPlayer.right and not mainPlayer.left and mainPlayer.wasGoingRight):
            win.blit(jumpingAnimation[1], (mainPlayer.x, mainPlayer.y))
            # Falling Left
        if (mainPlayer.jumping and not mainPlayer.left and not mainPlayer.right and not mainPlayer.wasGoingRight):
            win.blit(pygame.transform.flip(jumpingAnimation[1], True, False), (mainPlayer.x, mainPlayer.y))

#Creates the enemy unit
class enemy(object):
    def __init__(self, x, y, width, height, direction, right, left, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = direction
        self.right = right
        self.left = left
        self.velocity = 1 * direction
        self.walkCount = 0
        self.health = health
        self.isHurt = False
        self.frameCount = 24
    def draw(self, win):
        if (self.isHurt):
            self.frameCount = 45
            self.isHurt = False
        if (self.walkCount >= self.frameCount):
            self.walkCount = 0
            self.frameCount = 24

        if(self.left and not (self.frameCount == 45)):
            win.blit(enemyWalkingAnimation[self.walkCount//3], (self.x, self.y))

        elif(self.right and not (self.frameCount == 45)):
            win.blit(pygame.transform.flip(enemyWalkingAnimation[self.walkCount// 3], True, False), (self.x, self.y))

        if(self.frameCount == 45 and self.left):
            win.blit(enemyHurtAnimation[self.walkCount//3], (self.x, self.y))
        if (self.frameCount == 45 and self.right):
            win.blit(pygame.transform.flip(enemyHurtAnimation[self.walkCount // 3], True, False), (self.x, self.y))
        self.walkCount += 1


#Create the projectile class that the character will shoot
class projectile(object):
    def __init__(self, x, y, radius, color, direction, damage, isBig):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.velocity = 30 * direction
        self.damage = damage
        self.isBig = isBig
    def draw(self, win):
        if(self.isBig):
            win.blit(buzzsawImage, (self.x, self.y - 75))
        else:
            pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

#Create Coin Class
class goldCoin():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.spinCount = 0
    def draw(self, win):
        if (self.spinCount >= 45):
            self.spinCount = 0
        win.blit(coinAnimation[self.spinCount//3], (self.x, self.y))
        self.spinCount += 1

#Holds Key Statuses
pressed_down = False
pressed_left = False
pressed_right = False
pressed_up = False
pressed_spaceBar = False

#Clock Setup
clock = pygame.time.Clock()

#Draws everything into the window
def redrawFrame():
    win.blit(background, (0, 0))
    for bullet in bullets:
        bullet.draw(win)
    for e in enemyHandler:
        e.draw(win)
    mainPlayer.draw(win)
    pygame.draw.rect(win, (255,255,255), pygame.Rect(0,0, (mainPlayer.gauge/10) * 300, 25))
    pygame.draw.rect(win, (255,255,255),pygame.Rect(0,0,300,25), 2)
    pygame.draw.rect(win, (255, 255, 255), pygame.Rect(xLimit - 302, 0, 302, 31), 2)
    pygame.draw.rect(win, (255, 0, 0), pygame.Rect(xLimit - (300*(mainPlayer.health/100)), 0, 300, 30))
    for c in coins:
        c.draw(win)
    font = pygame.font.Font(None, 36)
    text = font.render(str(score), 1, (255,255,255))
    textpos = text.get_rect(centerx=background.get_width()/4)
    win.blit(text, textpos)
    pygame.display.update()
#Creates enemies until game ends
class spawnEnemy():
    def __init__(self):
        self.startRight = -1
        if (random.random() > .5):
            self.startRight = 1
        self.lastDirection = 0
    #Handle Initial Spawn
    #Start Right
    def generateEnemy(self):
        if self.startRight == 1:
            enemyHandler.append(enemy(10, yLimit - 120, 128, 128, 1, True, False, 100 + 50 * score//500))
            self.lastDirection = 1
            self.startRight = 0
            return
        #Start Left
        elif self.startRight == -1:
            enemyHandler.append(enemy(xLimit - 128, yLimit - 120, 128, 128, -1, False, True, 100 + 50 * score//500))
            self.lastDirection = -1
            self.startRight = 0
            return
        #Make a right moving enemy
        if self.lastDirection == -1 and len(enemyHandler) < enemyVolume:
            enemyHandler.append(enemy(10, yLimit-120, 128, 128, 1, True, False, 100 + 50 * score//500))
            self.lastDirection = 1
        #Make a left moving enemy
        elif self.lastDirection == 1 and len(enemyHandler) < enemyVolume:
            enemyHandler.append(enemy(xLimit - 128, yLimit - 120, 128, 128, -1, False, True, 100 + 50 * score//500 ))
            self.lastDirection = -1

#Main Loop
mainPlayer = player(0, yLimit - 75, 70, 75, 5)
enemyGenerator = spawnEnemy()
enemyHandler = []
bullets = []
coins = []
bigBullets = []
#Set counter, score, and the number of allowed enemies
enemyCount = 1
score = 0
enemyVolume = 5
while running:
    clock.tick(60)
    #Check to see if Player is still alive
    if(mainPlayer.health == 0):
        Tk().wm_withdraw()  # to hide the main window
        messagebox.showinfo('Game Over', 'Final Score: ' + str(score))
        running = False
    for event in pygame.event.get():
        #Stops the game if the window is closed
        if event.type == pygame.QUIT:
            running = False

        #Checks for keys pressed down and updates key status
        elif event.type == pygame.KEYDOWN:  # check for key presses
            if event.key == pygame.K_LEFT:  # left arrow turns left
                pressed_left = True
            elif event.key == pygame.K_RIGHT:  # right arrow turns right
                pressed_right = True
            elif event.key == pygame.K_UP:  # up arrow goes up
                pressed_up = True
            elif event.key == pygame.K_DOWN:  # down arrow goes down
                pressed_down = True
            elif event.key == pygame.K_SPACE: #space bar has been pressed
                pressed_spaceBar = True

        #Checks if a key has been unpressed and updates status
        elif event.type == pygame.KEYUP:  # check for key releases
            if event.key == pygame.K_LEFT:  # left arrow turns left
                pressed_left = False
            elif event.key == pygame.K_RIGHT:  # right arrow turns right
                pressed_right = False
            elif event.key == pygame.K_DOWN:  # down arrow goes down
                pressed_down = False
            elif event.key == pygame.K_SPACE:
                pressed_spaceBar = False

    for bullet in bullets:
        if(bullet.x < xLimit and bullet.x > 0):
            bullet.x += bullet.velocity
        else:
            #Finds bullet that went off screen and removes it from the array
            bullets.pop(bullets.index(bullet))

    #Generate Coins and check if there is a collision
    for coin in coins:
        if((coin.x - 32 <=mainPlayer.x <= coin.x or coin.x < mainPlayer.x <= coin.x +32) and mainPlayer.y >= yLimit - 100):
            coins.pop(coins.index(coin))
            if (mainPlayer.gauge < 10):
                mainPlayer.gauge += 1
    if(random.random() > .99 and len(coins) <= 3):
        c = goldCoin(random.randint(10, xLimit-100), yLimit - 64)
        coins.append(c)

    #Generate Bullets when Space Bar is pressed
    if(pressed_spaceBar):
        direction = -1
        if mainPlayer.wasGoingRight:
            direction = 1
        #Checks if charge meter is filled to use stronger bullets
        if(mainPlayer.gauge == 10 and mainPlayer.bulletDelay == 0):
            bullets.append(projectile(round(mainPlayer.x + mainPlayer.width//2), round(mainPlayer.y + mainPlayer.height//2),5, (255, 0, 0), direction, 100, True))
            mainPlayer.gauge = 0
            mainPlayer.bulletDelay = 35
        elif mainPlayer.bulletDelay == 0:
            bullets.append(projectile(round(mainPlayer.x + mainPlayer.width//2), round(mainPlayer.y + mainPlayer.height//2), 5,(255, 0,0), direction, 50, False))
            mainPlayer.bulletDelay = 35

    #Updates actual position of character but not jumping
    if (pressed_left and mainPlayer.x > 0):
        mainPlayer.x -= mainPlayer.velocity
        mainPlayer.right = False
        mainPlayer.left = True
        mainPlayer.wasGoingRight = False
    elif (pressed_right and mainPlayer.x < xLimit - mainPlayer.width):
        mainPlayer.x += mainPlayer.velocity
        mainPlayer.right = True
        mainPlayer.left = False
        mainPlayer.wasGoingRight = True
    else:
        mainPlayer.right = False
        mainPlayer.left = False
        mainPlayer.walkCount = 0

    #Controls jumping
    if (pressed_up):
        mainPlayer.walkCount = 0
        #Mimicks quadratic jump arc, as jumpCount goes down speed decreases
        if mainPlayer.jumpCount >= -12:
            mainPlayer.jumping = True
            #Sets the falling frame of the jump animation
            if(mainPlayer.jumpCount < 0):
                mainPlayer.falling = True
            mainPlayer.y -= (abs(mainPlayer.jumpCount)* mainPlayer.jumpCount) * .35
            if(mainPlayer.y < 0):
                mainPlayer.y = 0
            mainPlayer.jumpCount -= 1
        else:
            pressed_up = False
            mainPlayer.falling = False
            mainPlayer.jumping = False
            mainPlayer.jumpCount = 12

    #Deals with collisions of bullets and enemies
    for e in enemyHandler:
        #Checks if bullets hit
        for b in bullets:
            if(e.x <= b.x <= e.x + 100 and 0 <= b.y <= yLimit):
                e.health -= b.damage
                bullets.pop(bullets.index(b))
                e.isHurt = True
        # Player Collided with Snail
        if (e.x <= mainPlayer.x <= e.x + 100 and e.y <= mainPlayer.y <= yLimit and mainPlayer.iFrames == 0):
            mainPlayer.health -= 10
            mainPlayer.iFrames = 50

    #Sets a spawn rate and enemy volume according to the player's score
    if(score < 100):
        spwnRate = 300
    elif(score < 500):
        spwnRate = 200
        enemyVolume = 7
    elif(score < 1000):
        spwnRate = 100
        enemyVolume = 10
    elif(score >= 1000):
        spwnRate = 50
        enemyVolume  = 14
    else:
        spwnRate = 300

    #Makes and manages enemies
    if(enemyCount % spwnRate == 0):
        enemyGenerator.generateEnemy()
    if(enemyCount == 1000):
        enemyCount = 0

    for e in enemyHandler:
        #Remove enemies offscreen
        if(e.x >= xLimit or e.x <= -20):
            enemyHandler.pop(enemyHandler.index(e))
        if e.health <= 0:
            score += 100
            enemyHandler.pop(enemyHandler.index(e))
        #Move enemy accordingly
        e.x += e.velocity

    #Handles all the incrementing tasks
    enemyCount += 1
    if(mainPlayer.iFrames > 0):
        mainPlayer.iFrames -= 1
    if(mainPlayer.bulletDelay > 0):
        mainPlayer.bulletDelay -=1
    redrawFrame()
pygame.quit()