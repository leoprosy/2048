import numpy as np
import random
import pygame
import math

SIZE = 200
COLOR_GRID = (187, 173, 160)
COLORS = [(205, 193, 180),(238, 228, 218),(237, 224, 200),(242, 177, 121),(245, 149, 99),(246, 124, 95),(246, 94, 59),(237, 207, 114),(237, 204, 97),(237, 200, 80),(237, 197, 63),(237, 194, 46)]

board = np.zeros((4,4))
score = 0

def get_empty():
    return [(i, j) for i, y in enumerate(board) for j, x in enumerate(y) if x==0]

def get_adjacent_indices(i, j, m, n) -> list:
    adjacent_indices = []
    if i > 0:
        adjacent_indices.append(board[i-1][j])
    if i+1 < m:
        adjacent_indices.append(board[i+1][j])
    if j > 0:
        adjacent_indices.append(board[i][j-1])
    if j+1 < n:
        adjacent_indices.append(board[i][j+1])
    return adjacent_indices

def check_possibilities():
    for row, col in np.ndindex(board.shape):
        adj = get_adjacent_indices(row, col, 4, 4)
        if board[row][col] in adj:
            return True
    return False

def add_cell():
    next = random.randint(1,8)
    next = 4 if next == 8 else 2
    new = random.choice(get_empty())
    board[new[0]][new[1]] = next

def check_collision(x, cell, yp, xp):
    if 0 <= cell[0]+yp <= 3 and 0 <= cell[1]+xp <= 3:
        if board[cell[0]+yp][cell[1]+xp] == 0 or board[cell[0]+yp][cell[1]+xp] == x:
            return True
    else: return False

def move_cells(direction:str):
    direction_mapping = {"b": (1, 0), "t": (-1, 0), "r": (0, 1), "l": (0, -1)}
    yp, xp = direction_mapping.get(direction, (0, 0))
    moves=0
    for i, y in enumerate(board[::yp*-1 if yp!=0 else 1]):
        for j, x in enumerate(y[::xp*-1 if xp!=0 else 1]):
            if x!=0:
                I=i
                J=j
                if yp*-1 == -1:
                    I = (3 - I)
                if xp*-1 == -1:
                    J = (3 - j)
                while check_collision(x, (I,J), yp, xp):
                    board[I+yp][J+xp]+=x
                    board[I][J] = 0
                    I+=yp
                    J+=xp
                    moves +=1
    return moves

def display(screen, size):
    for row, col in np.ndindex(board.shape):
        color = COLORS[0] if board[row][col] ==0 else COLORS[int(math.log2(int(board[row][col])))]
        pygame.draw.rect(screen, color, (col*size, row*size, size-10, size-10), border_radius=10)
    for row, col in np.ndindex(board.shape):
        if board[col][row] > 0:
            font_color = (119, 110, 101) if board[col][row] in [2.0,4.0] else (249, 246, 242)
            font = pygame.font.SysFont("Clear", 80)
            txt = font.render(str(int(board[col][row])), True, font_color)
            screen.blit(txt, (row*size+((size-txt.get_width()-10)/2),col*size+((size-txt.get_height()-10)/2)))

def reset():
    for i, y in enumerate(board):
        for j, _ in enumerate(y):
            board[i][j] = 0
    for _ in range(2):
        add_cell()

def main():
    pygame.init()
    pygame.display.set_caption("2048")
    screen = pygame.display.set_mode((800,800))
    screen.fill(COLOR_GRID)

    for _ in range(2):
        add_cell()

    while True:
        display(screen, SIZE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moves = move_cells(direction="l")
                    if moves > 0: add_cell()
                if event.key == pygame.K_RIGHT:
                    moves = move_cells(direction="r")
                    if moves > 0: add_cell()
                if event.key == pygame.K_UP:
                    moves = move_cells(direction="t")
                    if moves > 0: add_cell()
                if event.key == pygame.K_DOWN:
                    moves = move_cells(direction="b")
                    if moves > 0: add_cell()
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.button == 1:
            #         if button.collidepoint(event.pos):
            #             reset()
                        

        if len(get_empty()) == 0 and not check_possibilities():
            pygame.draw.rect(screen, (25,25,25), ((screen.get_width() - 400)//2, (screen.get_height() - 200)//2, 400, 200), border_radius=20)
            font = pygame.font.SysFont("Clear", 80)
            txt = font.render("Game Over!", True, (255,255,255))
            screen.blit(txt, ((screen.get_width() - txt.get_width())//2, (screen.get_height() - txt.get_height())//2, 400, 200))
            # button = pygame.Rect(200,300, 400, 200)
        
        pygame.display.flip()
        pygame.display.update()

if __name__ == "__main__":
    main()