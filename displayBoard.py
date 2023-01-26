import pygame, sys, random
import textParser as tp
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

def stringToTiles(tiles, string, symbols):
    if not "/" in string:
        string = tp.parseWheel(string)
    tiles.clear()
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
    loadSymbols(tiles, symbols)

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

def loadSymbols(tiles, symbols):
    for tile in tiles:
        if tile.letter in symbols:
            tile.state = "w"

def showAll(tiles):
    for tile in tiles:
        tile.state = "t"

tiles = []
lettersVisual = []

f = open("solutions.txt")
listTitles = f.readlines()

for i in range(len(listTitles) - 1):
    listTitles[i] = listTitles[i].rstrip()

##listTitles = ["  /  Roll for/ Performance",
##              "/  Casting a /  Spell Slot",
##              " Making eye/ contact with/ a beholder",
##              " Valdas's/  Spire of/  Secrets"]

f = open("solutions.txt")


catTitles = f.readlines()

for i in range(len(listTitles) - 1):
    catTitles[i] = catTitles[i].rstrip()

print(catTitles)
##catTitles = ["Webshow Title",
##             "Before & After",
##             "What are you doing?",
##             "Best Sellers"]

SCREENX = 880
SCREENY = 455
alphabet = "abcdefghijklmnopqrstuvwxyz"
symbols = ",.'"

stringToTiles(tiles, "  /  Roll for/ Performance", symbols)
categoryText = "Webshow Title"

pygame.init()
screen = pygame.display.set_mode((SCREENX, SCREENY))
pygame.display.set_caption('Wheel of Fortune')

bg = pygame.image.load('bg.png')

largeLetter = pygame.font.SysFont(name = 'arial', size = 40, bold = True, italic = False)
smallLetter = pygame.font.SysFont(name = 'arial', size = 20, bold = True, italic = False)
category    = pygame.font.SysFont(name = 'trebuchet_ms', size = 20, bold = True, italic = True)

dx = 0
dy = 0

while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                displayRandom(tiles)
            elif event.key == K_1:
                print("Options:")
                print("---------")
                print("1\t- Show this menu")
                print("2\t- Input New Wheel")
                print("3\t- Input New Category")
                print("4\t- Show all letters")
                print("5\t- Load Preloaded Text")
                print("Enter\t- Show random letter")
            elif event.key == K_2:
                stringToTiles(tiles, input("Wheel Text: "), symbols)
            elif event.key == K_3:
                categoryText = input("Category Text: ")
            elif event.key == K_4:
                showAll(tiles)
            elif event.key == K_5:
                n = int(input("Which input? (0 - " + str(min(len(listTitles), len(catTitles)) - 1) + "): "))
                stringToTiles(tiles, listTitles[n], symbols)
                categoryText = catTitles[n]
            else:
                letter = event.unicode
                revealLetter(tiles, letter)
                if not letter in lettersVisual and letter in alphabet:
                    lettersVisual.append(letter)
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            dx, dy = event.pos

    screen.blit(bg, (0,0)) #Paste BG Image

    for t in tiles: #Place tiles
        if t.state == "b":
            pygame.draw.rect(screen, (32, 102, 188), (getX(t.x), getY(t.y), 42, 61))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (getX(t.x), getY(t.y), 42, 61))
            if t.state == "t":
                label = largeLetter.render(t.letter, True, (0, 0, 0))
                labelRect = label.get_rect()
                labelRect.center = (getX(t.x) + 42/2.0, getY(t.y) + 61/2.0)
                screen.blit(label, labelRect)

    for letter in alphabet: #Show bottom letters
        if letter in lettersVisual:
            label = smallLetter.render(letter.upper(), True, (100, 100, 100))
        else:
            label = smallLetter.render(letter.upper(), True, (255, 255, 255))
        
        labelRect = label.get_rect()
        labelRect.center = (alphabet.index(letter) * 20 + 189, 438)
        screen.blit(label, labelRect)

    label = category.render(categoryText, True, (0, 0, 0)) #Display Category
    labelRect = label.get_rect()
    labelRect.center = (SCREENX/2, 405)
    pygame.draw.rect(screen, (0, 0, 0), labelRect, width = 5)
    pygame.draw.rect(screen, (200, 200, 255), labelRect)
    screen.blit(label, labelRect)
    
    #for y in range(4):
        #for x in range(14):
            #pygame.draw.rect(screen, (255,255,255), (getX(x), getY(y), 42, 61), width=1)
    
    pygame.display.update()
