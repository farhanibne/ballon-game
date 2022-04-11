import pygame
import sys
import random
from math import *

pygame.init()

width = 500
height = 500

display = pygame.display.set_mode((width, height))
pygame.display.set_caption(" Balloon Shooter Game -- DZ")
clock = pygame.time.Clock()

margin = 100
lowerBound = 100

score = 0


white = (230, 230, 230)
lightBlue = (174, 214, 241)
red = (231, 76, 60)
lightGreen = (25, 111, 61)
darkGray = (40, 55, 71)
skyBlue = (135,206,235)
darkBlue = (21, 67, 96)
green = (35, 155, 86)
yellow = (244, 208, 63)
blue = (46, 134, 193)
purple = (155, 89, 182)
orange = (243, 156, 18)
black = (0, 0, 0)

font = pygame.font.SysFont("Arial", 25)


class Balloon:
    def __init__(self, speed):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound
        self.angle = 90
        self.speed = -speed
        self.probPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice([red, green, purple, orange, yellow, blue])

    
    def move(self):
        direct = random.choice(self.probPool)

        if direct == -1:
            self.angle += -10
        elif direct == 0:
            self.angle += 0
        else:
            self.angle += 10

        self.y += self.speed*sin(radians(self.angle))
        self.x += self.speed*cos(radians(self.angle))

        if (self.x + self.a > width) or (self.x < 0):
            if self.y > height/5:
                self.x -= self.speed*cos(radians(self.angle)) 
            else:
                self.reset()
        if self.y + self.b < 0 or self.y > height + 30:
            self.reset()

    
    def show(self):
        pygame.draw.line(display, darkBlue, (self.x + self.a/2, self.y + self.b), (self.x + self.a/2, self.y + self.b + self.length))
        pygame.draw.ellipse(display, self.color, (self.x, self.y, self.a, self.b))
        pygame.draw.ellipse(display, self.color, (self.x + self.a/2 - 5, self.y + self.b - 3, 10, 10))

    
    def burst(self):
        global score
        pos = pygame.mouse.get_pos()

        if onBalloon(self.x, self.y, self.a, self.b, pos):
            score += 1
            self.reset()

    
    def reset(self):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound 
        self.angle = 90
        self.speed -= 0.002
        self.probPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice([red, green, purple, orange, yellow, blue])

balloons = []
noBalloon = 10
for i in range(noBalloon):
    obj = Balloon(random.choice([1, 1, 2, 2, 2, 2, 3, 3, 3, 4]))
    balloons.append(obj)

def onBalloon(x, y, a, b, pos):
    if (x < pos[0] < x + a) and (y < pos[1] < y + b):
        return True
    else:
        return False


def pointer():
    pos = pygame.mouse.get_pos()
    r = 25
    l = 20
    color = lightGreen
    for i in range(noBalloon):
        if onBalloon(balloons[i].x, balloons[i].y, balloons[i].a, balloons[i].b, pos):
            color = black
    pygame.draw.ellipse(display, color, (pos[0] - r/2, pos[1] - r/2, r, r), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] - l/2), (pos[0], pos[1] - l), 4)
    pygame.draw.line(display, color, (pos[0] + l/2, pos[1]), (pos[0] + l, pos[1]), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] + l/2), (pos[0], pos[1] + l), 4)
    pygame.draw.line(display, color, (pos[0] - l/2, pos[1]), (pos[0] - l, pos[1]), 4)

def lowerPlatform():
    pygame.draw.rect(display, skyBlue, (0, height - lowerBound, width, lowerBound))

def showTitle():
    titleText = font.render("Simple Balloon Shooter Game", True, black)
    display.blit(titleText, (15, height - lowerBound ))

def showScore():
    scoreText = font.render("Balloon Destroyed : " + str(score), True, red)
    display.blit(scoreText, (250, height - lowerBound + 50))


def close():
    pygame.quit()
    sys.exit()

def game():
    global score
    loop = True

    while loop:
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

        display.fill(black)
        
        for i in range(noBalloon):
            balloons[i].show()

        pointer()
        
        for i in range(noBalloon):
            balloons[i].move()

        
        lowerPlatform()
        showTitle()
        showScore()
        pygame.display.update()
        clock.tick(60)


game()
