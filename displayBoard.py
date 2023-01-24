import pygame, sys, random
from pygame.locals import *

class Tile:
    def __init__(self, x, y, state, letter):
        self.x = x
        self.y = y
        self.state = state
        self.letter = letter

        #States:
        #'t' - Text showing
        #'b' - Text about to show
        #'w' - Text not showing

def getX(x):
    return (62 + (x * 55))

def getY(y):
    return (85 + (y * 75))

def revealLetter(tiles, letter):
    for tile in tiles:
        if tile.state == "b":
            tile.state = "t"
            break
    for tile in tiles:
        if tile.state == "b" and tile.letter.lower() != letter:
            tile.state = "t"
        if tile.letter.lower() == letter and tile.state == "w":
            tile.state = "b"

def stringToTiles(tiles, string):
    x = 1
    y = 0
    for char in string:
        if char == "/":
            y += 1
            x = 0
            if y == 0 or y == 3:
                x = 1
        elif char == " ":
            x += 1
        else:
            tiles.append(Tile(x,y,"w",char))
            x += 1

def displayRandom(tiles):
    allShowing = True
    for tile in tiles:
        if tile.state != "t":
            allShowing = False
            break

    if not allShowing:
        while True:
            n = random.choice(tiles)
            if n.state != "t":
                n.state = "t"
                break

tiles = []
lettersVisual = []
stringToTiles(tiles, "  /  Roll for/ Performance")


SCREENX = 880
SCREENY = 455
alphabet = "abcdefghijklmnopqrstuvwxyz"

pygame.init()
screen = pygame.display.set_mode((SCREENX, SCREENY))
pygame.display.set_caption('Wheel of Fortune')

bg = pygame.image.load('bg.png')

largeLetter = pygame.font.SysFont(name = 'arial', size = 40, bold = True, italic = False)
smallLetter = pygame.font.SysFont(name = 'arial', size = 20, bold = True, italic = False)

while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                displayRandom(tiles)
            else:
                letter = event.unicode
                revealLetter(tiles, letter)
                if not letter in lettersVisual and letter in alphabet:
                    lettersVisual.append(letter)
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)

    screen.blit(bg, (0,0)) #Paste BG Image

    for t in tiles:
        if t.state == "b":
            pygame.draw.rect(screen, (32, 102, 188), (getX(t.x), getY(t.y), 42, 61))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (getX(t.x), getY(t.y), 42, 61))
            if t.state == "t":
                label = largeLetter.render(t.letter, True, (0, 0, 0))
                labelRect = label.get_rect()
                labelRect.center = (getX(t.x) + 42/2.0, getY(t.y) + 61/2.0)
                screen.blit(label, labelRect)

    for letter in alphabet:
        if letter in lettersVisual:
            label = smallLetter.render(letter.upper(), True, (100, 100, 100))
        else:
            label = smallLetter.render(letter.upper(), True, (255, 255, 255))
        
        labelRect = label.get_rect()
        labelRect.center = (alphabet.index(letter) * 20 + 189, 438)
        screen.blit(label, labelRect)
    
    #for y in range(4):
        #for x in range(14):
            #pygame.draw.rect(screen, (255,255,255), (getX(x), getY(y), 42, 61), width=1)
    
    pygame.display.update()
