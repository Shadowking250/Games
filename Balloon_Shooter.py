import pygame
import sys
import random
from math import *
import time

pygame.init()

width = 1820
height = 980

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("CopyAssignment - Balloon Shooter Game")
clock = pygame.time.Clock()

margin = 100
lowerBound = 100

score = 0
level = 1
target_balloons = 10  # Balloons to burst to pass the level
target_color = None
penalty = -2

# Define balloon colors
gray = (128, 128, 128)
Pink = (255, 192, 203)
Black = (0, 0, 0)
white = (230, 230, 230)
lightBlue = (4, 27, 96)
red = (231, 76, 60)
lightGreen = (25, 111, 61)
darkGray = (40, 55, 71)
darkBlue = (64, 178, 239)
green = (35, 155, 86)
yellow = (244, 208, 63)
blue = (46, 134, 193)
purple = (155, 89, 182)
orange = (243, 156, 18)

all_colors = [red, green, purple, orange, yellow, blue, Pink]

font = pygame.font.SysFont("Arial", 25)

class Balloon:
    def __init__(self, speed):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound
        self.angle = 90
        self.speed = -speed
        self.proPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice(all_colors)
        
    def move(self):
        direct = random.choice(self.proPool)
        if direct == -1:
            self.angle += -10
        elif direct == 0:
            self.angle += 0
        else:
            self.angle += 10

        self.y += self.speed * sin(radians(self.angle))
        self.x += self.speed * cos(radians(self.angle))

        if (self.x + self.a > width) or (self.x < 0):
            if self.y > height / 5:
                self.x -= self.speed * cos(radians(self.angle))
            else:
                self.reset()
        if self.y + self.b < 0 or self.y > height + 30:
            self.reset()
            
    def show(self):
        pygame.draw.line(display, darkBlue, (self.x + self.a / 2, self.y + self.b), 
                         (self.x + self.a / 2, self.y + self.b + self.length))
        pygame.draw.ellipse(display, self.color, (self.x, self.y, self.a, self.b))
        pygame.draw.ellipse(display, self.color, (self.x + self.a / 2 - 5, self.y + self.b - 3, 10, 10))
            
    def burst(self):
        global score
        pos = pygame.mouse.get_pos()
        if isonBalloon(self.x, self.y, self.a, self.b, pos):
            if self.color == target_color:  # Correct color burst
                score += 1
            else:  # Wrong color burst
                score += penalty
            self.reset()
                
    def reset(self):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound 
        self.angle = 90
        self.speed -= 0.002
        self.proPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice(all_colors)

balloons = []
noBalloon = 10
for i in range(noBalloon):
    obj = Balloon(random.choice([1, 1, 2, 2, 2, 2, 3, 3, 3, 4]))
    balloons.append(obj)

def isonBalloon(x, y, a, b, pos):
    if (x < pos[0] < x + a) and (y < pos[1] < y + b):
        return True
    return False
    
def pointer():
    pos = pygame.mouse.get_pos()
    r = 25
    l = 20
    color = Black
    for i in range(noBalloon):
        if isonBalloon(balloons[i].x, balloons[i].y, balloons[i].a, balloons[i].b, pos):
            color = red
    pygame.draw.ellipse(display, color, (pos[0] - r/2, pos[1] - r/2, r, r), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] - l/2), (pos[0], pos[1] - l), 4)
    pygame.draw.line(display, color, (pos[0] + l/2, pos[1]), (pos[0] + l, pos[1]), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] + l/2), (pos[0], pos[1] + l), 4)
    pygame.draw.line(display, color, (pos[0] - l/2, pos[1]), (pos[0] - l, pos[1]), 4)

def lowerPlatform():
    pygame.draw.rect(display, darkGray, (0, height - lowerBound, width, lowerBound))

def showScore():
    scoreText = font.render("Balloons Bursted: " + str(score), True, white)
    display.blit(scoreText, (150, height - lowerBound + 20))  # Adjusted vertical position for clarity

def showLevel():
    levelText = font.render("Level: " + str(level), True, white)
    display.blit(levelText, (width // 2 - 50, height - lowerBound + 50))

def showTargetColor():
    targetColorText = font.render("Shoot Only: ", True, white)
    pygame.draw.rect(display, target_color, (width // 2 + 120, height - lowerBound + 80, 50, 30))
    display.blit(targetColorText, (width // 2, height - lowerBound + 80))

def showTargetBalloonCount():
    targetBalloonText = font.render(f"Target Balloons: {score}/{target_balloons}", True, white)
    display.blit(targetBalloonText, (width // 2 - 50, 50))  # Displayed at the top of the screen

def showTimer(time_left):
    timerText = font.render("Time Left: " + str(time_left) + "s", True, white)
    display.blit(timerText, (width - 250, height - lowerBound + 100))  # Adjusted vertical position for clarity

def levelIntroScreen():
    display.fill(gray)
    introText = font.render(f"Level {level}", True, white)
    targetBalloonText = font.render(f"Target Balloons: {target_balloons}", True, white)
    targetColorText = font.render("Shoot Only This Color:", True, white)
    pygame.draw.rect(display, target_color, (width // 2 + 120, height // 2 - 50, 100, 100))

    display.blit(introText, (width // 2 - 50, height // 2 - 200))
    display.blit(targetBalloonText, (width // 2 - 100, height // 2 - 100))
    display.blit(targetColorText, (width // 2 - 150, height // 2))

    pygame.display.update()
    pygame.time.wait(3000)  # Pause for 3 seconds before the level starts

def close():
    pygame.quit()
    sys.exit()

def nextLevel():
    global level, target_balloons, target_color, score
    level += 1
    target_balloons += 5  # Increase the target number of balloons with each level
    score = 0  # Reset the score for each level
    if level == 2:
        target_color = random.choice([red, blue])
    elif level == 3:
        target_color = random.choice([yellow, green])
    elif level == 4:
        target_color = purple
    else:
        target_color = random.choice(all_colors)

def game():
    global score
    loop = True
    time_limit = 60  # 60 seconds for each level
    start_ticks = pygame.time.get_ticks()  # Timer

    levelIntroScreen()  # Show level intro before starting

    while loop:
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000  # Calculate time passed
        time_left = time_limit - seconds

        if time_left <= 0 or score >= target_balloons:
            break  # End level if time runs out or target is reached

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    score = 0
                    game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(noBalloon):
                    balloons[i].burst()

        display.fill(gray)

        for i in range(noBalloon):
            balloons[i].show()

        pointer()

        for i in range(noBalloon):
            balloons[i].move()

        lowerPlatform()
        showScore()
        showLevel()
        showTargetColor()
        showTargetBalloonCount()
        showTimer(time_left)

        pygame.display.update()
        clock.tick(60)

    # End of the level
    if score >= target_balloons:
        nextLevel()  # Move to the next level
        game()  # Restart the game with the new level
    else:
        # Game Over screen
        display.fill(Black)
        gameOverText = font.render("Game Over", True, white)
        finalScoreText = font.render("Balloons Bursted: " + str(score), True, white)
        display.blit(gameOverText, (width // 2 - 100, height // 2 - 50))
        display.blit(finalScoreText, (width // 2 - 150, height // 2 + 20))
        pygame.display.update()
        pygame.time.wait(3000)
        close()

# Start the game
target_color = random.choice(all_colors)  # Initialize the first target color
game()


