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