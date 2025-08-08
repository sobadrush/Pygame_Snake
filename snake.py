import pygame
import sys
import time
import random

# 初始化 Pygame
pygame.init()

# 視窗尺寸
screen_width = 720
screen_height = 480

# 網格尺寸
BLOCK_SIZE = 20

# 建立遊戲視窗
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('貪食蛇')

# 顏色定義
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)

clock = pygame.time.Clock()
snake_speed = 15

# 遊戲變數
snake_pos = [100, 60]
snake_body = [[100, 60], [80, 60]]
direction = 'RIGHT'
change_to = direction

# 畫面渲染
screen.fill(BLACK)

while True:
  
  # 這幾行註解掉看看
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    
    # 鍵盤輸入
    if event.type == pygame.KEYDOWN:
        if (event.key == pygame.K_UP or event.key == ord('w')) and direction != 'DOWN':
            change_to = 'UP'
        if (event.key == pygame.K_DOWN or event.key == ord('s')) and direction != 'UP':
            change_to = 'DOWN'
        if (event.key == pygame.K_LEFT or event.key == ord('a')) and direction != 'RIGHT':
            change_to = 'LEFT'
        if (event.key == pygame.K_RIGHT or event.key == ord('d')) and direction != 'LEFT':
            change_to = 'RIGHT'

  # 遊戲邏輯更新 (暫時為空)

  
  for pos in snake_body:
    # pygame.Rect(left, top, width, height)
    pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
    
  pygame.display.update()
  clock.tick(snake_speed)