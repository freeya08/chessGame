import pygame
import sys

# 初始化
pygame.init()

# 設定棋盤參數
BOARD_SIZE = 8
CELL_SIZE = 80  # 每格大小（像素）
WINDOW_SIZE = BOARD_SIZE * CELL_SIZE

# 顏色定義
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)

# 建立畫面
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Chess Board")


# 畫棋盤
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)


# 主迴圈
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_board()
    pygame.display.flip()

pygame.quit()
sys.exit()
