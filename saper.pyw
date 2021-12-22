import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)



def generate_bombs(row_start,column_start):
    n = int((len(grid)*len(grid[0]))/6)

    i = 0
    while i < n:
        row = random.randint(0,len(grid)-1)
        column = random.randint(0,len(grid[0])-1)
        if grid[row][column][0] != 2 and (row not in range(row_start-1, row_start+2) and column not in range(column_start-1, column_start+2)):
            grid[row][column][0] = 2
            add_numbers(row, column)
            i += 1


def add_numbers(row, column):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if possible(row + i, column + j):
                grid[row + i][column + j][1] += 1


def first_click(row, column):
    generate_bombs(row, column)
    for i in range(-1,2):
        for j in range(-1,2):
            if possible(row+i, column+j):
                grid[row + i][column + j][0] = 1
                check(row + i, column + j, True)


def check(row, column, first_check=False):
    for i in range(-1,2):
        for j in range(-1,2):
            if first_check and possible(row+i, column+j):
                grid[row + i][column + j][0] = 1
                if grid[row + i][column + j][1] == 0:
                    check(row + i, column + j, True)
            if possible(row+i, column+j) and grid[row + i][column + j][1] == 0:
                grid[row + i][column + j][0] = 1
                check(row + i, column + j)


def possible(row, column):
    if (row < 0 or column < 0) or (row >= len(grid) or column >= len(grid[0])):
        return False
    elif grid[row][column][0] != 0:
        return False
    return True


def display_game():
    screen.fill(BLACK)
    for row in range(rows):
        for column in range(columns):
            coordinates = [margin + (margin + size) * column, margin + (margin + size) * row, size, size]
            number = ""
            if grid[row][column][0] == 1:
                color = GRAY
                if grid[row][column][1] != 0:
                    number = grid[row][column][1]
            elif grid[row][column][0] == 2 and lost:
                color = RED
            else:
                color = WHITE

            pygame.draw.rect(screen, color, coordinates)
            text = font.render(str(number), True, (0, 0, 0))
            screen.blit(text, coordinates)
    if won():
        win_font = pygame.font.SysFont('microsoftjhengheimicrosoftjhengheiui', 50)
        text = win_font.render("You win!", True, (0,255,0))
        text_rect = text.get_rect(center=(width / 2, height / 2))
        screen.blit(text, text_rect)
    pygame.display.flip()
    clock.tick(60)


def won():
    for row in grid:
        for column in row:
            if column[0] == 0:
                return False
    return True



pygame.init()
pygame.font.init()
font = pygame.font.SysFont('microsoftjhengheimicrosoftjhengheiui', 22)

size = 25
margin = 2

rows = 10
columns = 10
width = margin+(size+margin)*columns
height = margin+(size+margin)*rows

window_size = (width, height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Saper")

grid = [[[0, 0] for x in range(columns)] for y in range(rows)]



clock = pygame.time.Clock()

done = False
lost = False
first = True

while not done:
    pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN and not lost:
            column = pos[0] // (size + margin)
            row = pos[1] // (size + margin)

            if event.button == 1:
                if first:
                    first_click(row, column)
                    first = False
                else:
                    check(row, column)
                    if grid[row][column][0] == 2:
                        print("you lost")
                        lost = True
                    else:
                        grid[row][column][0] = 1
    display_game()
pygame.quit()





