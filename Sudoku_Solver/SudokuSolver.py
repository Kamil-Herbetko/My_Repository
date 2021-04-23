import pygame
import time
pygame.font.init()

WIN_WIDTH = 630
WIN_HEIGHT = 680
MAIN_FONT = pygame.font.SysFont("comicsans", 35)
PENCIL_FONT = pygame.font.SysFont("comicsans", 20)


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 70
        self.height = 70
        self.text = 0
        self.mode = 0
        self.font = MAIN_FONT
        self.color = (0, 0, 0)
        self.predefined = False

    def draw(self, win):
        if self.text != 0:
            txt = self.font.render(str(self.text), True, self.color)
        else:
            txt = self.font.render("", True, self.color)

        if self.font == MAIN_FONT:
            win.blit(txt, (self.x + self.width/2 - txt.get_width()//2 , self.y + self.height/2 - txt.get_height()//2 ))
        else:
            win.blit(txt,(self.x, self.y))

        if self.mode == 1:
            pygame.draw.lines(win, (0, 0, 255), True, [(self.x, self.y), (self.x, self.y + self.height - 1),
                                                     (self.x + self.width - 1, self.y + self.height - 1), (self.x + self.width - 1, self.y)], 2)
        elif self.mode == 2:
            pygame.draw.lines(win, (0, 0, 0), True, [(self.x, self.y ), (self.x, self.y + self.height - 1),
                                                     (self.x + self.width - 1, self.y + self.height - 1),
                                                     (self.x + self.width - 1, self.y)], 3)

    def actionListener(self, t):
        self.text = t


def checkGrid(grid):
    for row in range(0,9):
        for col in range(0,9):
            if grid[row][col]==0:
                return False
    return True


def solveGrid(tiles):
    grid = [[], [], [], [], [], [], [], [], []]
    for i in range(9):
        for j in range(9):
            if tiles[i][j].predefined:
                grid[i].append(tiles[i][j].text)
            else:
                grid[i].append(0)

    for i in range(0, 81):
        row = i//9
        col = i % 9
        if grid[row][col] == 0:
            for value in range(1, 10):
                if not(value in grid[row]):
                    if not value in (grid[0][col], grid[1][col], grid[2][col], grid[3][col], grid[4][col], grid[5][col], grid[6][col], grid[7][col], grid[8][col]):
                        square = []
                        if row < 3:
                            if col < 3:
                                square = [grid[j][0:3] for j in range(0, 3)]
                            elif col < 6:
                                square = [grid[j][3:6] for j in range(0, 3)]
                            else:
                                square = [grid[j][6:9] for j in range(0, 3)]
                        elif row < 6:
                            if col < 3:
                                square = [grid[j][0:3] for j in range(3, 6)]
                            elif col < 6:
                                square = [grid[j][3:6] for j in range(3, 6)]
                            else:
                                square = [grid[j][6:9] for j in range(3, 6)]
                        else:
                            if col < 3:
                                square = [grid[j][0:3] for j in range(6, 9)]
                            elif col < 6:
                                square = [grid[j][3:6] for j in range(6, 9)]
                            else:
                                square = [grid[j][6:9] for j in range(6, 9)]

                        if not value in (square[0] + square[1] + square[2]):
                            grid[row][col] = value
                            tiles[row][col].font = MAIN_FONT
                            tiles[row][col].text = value
                            tiles[row][col].predefined = True
                            pygame.display.update()

                            if checkGrid(grid):
                                print("Grid Complete and Checked")
                                return True
                            else:
                                if solveGrid(tiles):
                                    return True
            break
    grid[row][col] = 0
    tiles[row][col].text = 0


def redrawWindow(win, time_from_start, tiles, solved):
    win.fill((255, 255, 255))

    for i in range(1, 10):
        if i % 3 == 0:
            pygame.draw.line(win, (0, 0, 0), ((i//3)*WIN_WIDTH//3 - 1, 0), ((i//3)*WIN_WIDTH//3 - 1, WIN_HEIGHT - 50), 3)
            pygame.draw.line(win, (0, 0, 0), (0, (i//3)*(WIN_HEIGHT - 50)//3 - 1), (WIN_WIDTH, (i//3)*(WIN_HEIGHT - 50)//3 - 1), 3)
        else:
            pygame.draw.line(win, (23, 23, 23), (i * WIN_WIDTH // 9, 0), (i * WIN_WIDTH // 9, WIN_HEIGHT - 50), 1)
            pygame.draw.line(win, (23, 23, 23), (0, i*(WIN_HEIGHT - 50) // 9), (WIN_WIDTH, i* (WIN_HEIGHT - 50) // 9), 1)

    if not solved:
        text = MAIN_FONT.render("Time: " + time.strftime("%Hh%Mm%Ss", time.gmtime(time_from_start)), True,  (0, 0, 0))
        win.blit(text, (WIN_WIDTH - 20 - text.get_width(), 645))

    for i in range(9):
        for j in range(9):
            tiles[i][j].draw(win)

    pygame.display.update()


if __name__ == '__main__':
    solved = False
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Sudoku")
    run = True
    start = time.time()
    tiles = [[], [], [], [], [], [], [], [], []]
    clicked = []

    for i in range(9):
        for j in range(9):
            tiles[i].append(Tile(j*70, i*70))
    while run:

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i in range(9):
                    for j in range(9):
                        tile = tiles[i][j]
                        if tile.x < mouse_pos[0] < (tile.x + tile.width) and tile.y < mouse_pos[1] < (
                                tile.y + tile.height):
                            if tile in clicked:

                                if tile.mode == 2:
                                    tile.mode = 0
                                    tile.font = MAIN_FONT
                                    tile.color = (0, 0, 0)
                                    clicked.pop(0)

                                else:
                                    tile.mode += 1
                                    tile.font = PENCIL_FONT
                                    tile.color = (123, 123, 123)

                            else:
                                if len(clicked) == 0 and not tile.predefined:
                                    tile.color = (0, 0, 0)
                                    tile.font = MAIN_FONT
                                    tile.mode += 1
                                    clicked.append(tile)

                                elif len(clicked) == 1 and not tile.predefined:
                                    clicked[0].mode = 0
                                    clicked.pop(0)
                                    tile.color = (0, 0, 0)
                                    tile.font = MAIN_FONT
                                    tile.mode += 1
                                    clicked.append(tile)
            if event.type == pygame.KEYDOWN:
                if len(clicked) == 1:
                    if event.key == pygame.K_1:
                        clicked[0].actionListener(1)
                        clicked[0].mode = 0
                        clicked.pop(0)
                    elif event.key == pygame.K_2:
                        clicked[0].actionListener(2)
                        clicked[0].mode = 0
                        clicked.pop(0)
                    elif event.key == pygame.K_3:
                        clicked[0].actionListener(3)
                        clicked[0].mode = 0
                        clicked.pop(0)
                    elif event.key == pygame.K_4:
                        clicked[0].actionListener(4)
                        clicked[0].mode = 0
                        clicked.pop(0)
                    elif event.key == pygame.K_5:
                        clicked[0].actionListener(5)
                        clicked[0].mode = 0
                        clicked.pop(0)
                    elif event.key == pygame.K_6:
                        clicked[0].actionListener(6)
                        clicked[0].mode = 0
                        clicked.pop(0)
                    elif event.key == pygame.K_7:
                        clicked[0].actionListener(7)
                        clicked[0].mode = 0
                        clicked.pop(0)
                    elif event.key == pygame.K_8:
                        clicked[0].actionListener(8)
                        clicked[0].mode = 0
                        clicked.pop(0)
                    elif event.key == pygame.K_9:
                        clicked[0].actionListener(9)
                        clicked[0].mode = 0
                        clicked.pop(0)
                    elif event.key == pygame.K_BACKSPACE:
                        clicked[0].actionListener(0)
                        clicked[0].mode = 0
                        clicked.pop(0)

                if event.key == pygame.K_SPACE:
                    solveGrid(tiles)
                    if len(clicked) == 1:
                        clicked[0].mode = 0
                        clicked.pop()
                    solved = True

                if event.key == pygame.K_INSERT:
                    for row in range(9):
                        for col in range(9):
                            tile = tiles[row][col]
                            if tile.text != 0:
                                tile.predefined = True
                                tile.mode = 0
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()










        redrawWindow(win, time.time() - start, tiles, solved)