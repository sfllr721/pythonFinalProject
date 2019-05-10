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
        self.midAirModifier = 2
        self.walkCount = 0
        self.idleCount = 0
        self.gauge = 0
        self.health = 100

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
        self.iFrames = 0
    def draw(self, win):
        if (self.walkCount >= 24):
            self.walkCount = 0
        if(self.left):
            win.blit(enemyWalkingAnimation[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        elif(self.right):
            win.blit(pygame.transform.flip(enemyWalkingAnimation[self.walkCount// 3], True, False), (self.x, self.y))
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
def spawnEnemy():
    global startRight
    global lastDirection
    global score
    global enemyVolume
    #Handle Initial Spawn
    #Start Right
    if startRight == 1:
        enemyHandler.append(enemy(10, yLimit - 120, 128, 128, 1, True, False, 100 + 50 * score//500))
        lastDirection = 1
        startRight = 0
        return
    #Start Left
    elif startRight == -1:
        enemyHandler.append(enemy(xLimit - 128, yLimit - 120, 128, 128, -1, False, True, 100 + 50 * score//500))
        lastDirection = -1
        startRight = 0
        return

    #Make a right moving enemy
    if lastDirection == -1 and len(enemyHandler) < enemyVolume:
        enemyHandler.append(enemy(10, yLimit-120, 128, 128, 1, True, False, 100 + 50 * score//500))
        lastDirection = 1
    #Make a left moving enemy
    elif lastDirection == 1 and len(enemyHandler) < enemyVolume:
        enemyHandler.append(enemy(xLimit - 128, yLimit - 120, 128, 128, -1, False, True, 100 + 50 * score//500 ))
        lastDirection = -1

#Main Loop
startRight = -1
lastDirection = 0
if(random.random() > .5 ):
    startRight = 1
mainPlayer = player(0, yLimit - 75, 70, 75, 5)
enemyHandler = []
bullets = []
coins = []
bigBullets = []
#Set counter for enemy spawns
enemyCount = 1
iFrames = 0
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
        if(mainPlayer.gauge == 10):
            bullets.append(projectile(round(mainPlayer.x + mainPlayer.width//2), round(mainPlayer.y + mainPlayer.height//2),5, (255, 0, 0), direction, 100, True))
            mainPlayer.gauge = 0
        elif len(bullets) < 2:
            bullets.append(projectile(round(mainPlayer.x + mainPlayer.width//2), round(mainPlayer.y + mainPlayer.height//2), 5,(255, 0,0), direction, 50, False))
    #Updates actual position of character
    if (pressed_left and mainPlayer.x > 0):
        #Gives more in air control
        if(pressed_up):
            mainPlayer.x -= mainPlayer.velocity * mainPlayer.midAirModifier
        mainPlayer.x -= mainPlayer.velocity
        mainPlayer.right = False
        mainPlayer.left = True
        mainPlayer.wasGoingRight = False
    elif (pressed_right and mainPlayer.x < xLimit - mainPlayer.width):
        #Gives more in air control
        if (pressed_up):
            mainPlayer.x += mainPlayer.velocity * mainPlayer.midAirModifier
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
            mainPlayer.y -= (abs(mainPlayer.jumpCount)* mainPlayer.jumpCount) * .5
            if(mainPlayer.y < 0):
                mainPlayer.y = 0
            mainPlayer.jumpCount -= 1
        else:
            pressed_up = False
            mainPlayer.falling = False
            mainPlayer.jumping = False
            mainPlayer.jumpCount = 12
    for e in enemyHandler:
        if(e.iFrames > 0):
            e.iFrames -= 1
        #Checks if bullets hit
        for b in bullets:
            if(e.x <= b.x <= e.x + 100 and 0 <= b.y <= yLimit and e.iFrames == 0):
                e.health -= b.damage
                e.iFrames = 30
                bullets.pop(bullets.index(b))
        # Player Collided with Snail
        if (e.x <= mainPlayer.x <= e.x + 100 and e.y <= mainPlayer.y <= yLimit and iFrames == 0):
            mainPlayer.health -= 10
            iFrames = 50
    if(score < 100):
        spwnRate = 300
        enemyVolume += 1
    elif(score < 500):
        spwnRate = 200
        enemyVolume += 2
    elif(score < 1000):
        spwnRate = 100
        enemyVolume += 3
    elif(score < 2000):
        spwnRate = 50
        enemyVolume += 4

    #Makes and manages enemies
    if(enemyCount % spwnRate == 0):
        spawnEnemy()
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

    enemyCount += 1
    if(iFrames > 0):
        iFrames -= 1
    redrawFrame()

pygame.quit()