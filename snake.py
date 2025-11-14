import pygame
import sys
import time
import random

# 初始化 Pygame
pygame.init()

# 視窗尺寸
screen_width = 720
screen_height = 480
BLOCK_SIZE = 20

# 建立遊戲視窗
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('貪食蛇新手村')

# 顏色定義
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)

# FPS 控制器
clock = pygame.time.Clock()
snake_speed = 15

def show_score(score, choice=1):
    score_font = pygame.font.SysFont('consolas', 20)
    score_surface = score_font.render('Score : ' + str(score), True, WHITE)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (screen_width / 10, 15)
    else:
        score_rect.midtop = (screen_width / 2, screen_height / 1.5)
    screen.blit(score_surface, score_rect)

def game_over_message(score):
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (screen_width / 2, screen_height / 4)
    screen.blit(game_over_surface, game_over_rect)
    
    show_score(score, choice=0)

    restart_font = pygame.font.SysFont('consolas', 20)
    restart_surface = restart_font.render('Press [R] to Restart or [Q] to Quit', True, WHITE)
    restart_rect = restart_surface.get_rect()
    restart_rect.midtop = (screen_width / 2, screen_height / 1.25)
    screen.blit(restart_surface, restart_rect)
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    waiting = False

def main():
    def generate_food(snake_body):
        while True:
            pos = [random.randrange(0, screen_width // BLOCK_SIZE) * BLOCK_SIZE, 
                   random.randrange(0, screen_height // BLOCK_SIZE) * BLOCK_SIZE]
            if pos not in snake_body:
                return pos

    # 新增 generate_poison 函式
    def generate_poison(snake_body, food_pos):
        while True:
            pos = [random.randrange(0, screen_width // BLOCK_SIZE) * BLOCK_SIZE, 
                   random.randrange(0, screen_height // BLOCK_SIZE) * BLOCK_SIZE]
            if (pos not in snake_body) and (pos != food_pos): # 確保不會產生在蛇身上，也不會跟食物重疊
                return pos
        

    score = 0
    snake_pos = [100, 60]
    snake_body = [[100, 60], [80, 60], [60, 60]]
    food_pos = generate_food(snake_body)
    poison_pos = generate_poison(snake_body, food_pos) # 毒藥
    direction = 'RIGHT'
    change_to = direction

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == ord('w')) and direction != 'DOWN':
                    change_to = 'UP'
                if (event.key == pygame.K_DOWN or event.key == ord('s')) and direction != 'UP':
                    change_to = 'DOWN'
                if (event.key == pygame.K_LEFT or event.key == ord('a')) and direction != 'RIGHT':
                    change_to = 'LEFT'
                if (event.key == pygame.K_RIGHT or event.key == ord('d')) and direction != 'LEFT':
                    change_to = 'RIGHT'

        direction = change_to

        if direction == 'UP': snake_pos[1] -= BLOCK_SIZE
        if direction == 'DOWN': snake_pos[1] += BLOCK_SIZE
        if direction == 'LEFT': snake_pos[0] -= BLOCK_SIZE
        if direction == 'RIGHT': snake_pos[0] += BLOCK_SIZE

        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]: # 吃到食物
            score += 10
            food_pos = generate_food(snake_body)
        elif snake_pos[0] == poison_pos[0] and snake_pos[1] == poison_pos[1]: # 吃到毒藥
            game_over_message(score)
            break
        else:
            snake_body.pop()

        screen.fill(BLACK)
        for pos in snake_body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
            
        # 繪製食物
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # 繪製毒藥
        pygame.draw.rect(screen, BLUE, pygame.Rect(poison_pos[0], poison_pos[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # 若接觸邊界則從另一側出現
        if snake_pos[0] >= screen_width:
            snake_pos[0] = 0
        elif snake_pos[0] < 0:
            snake_pos[0] = screen_width - BLOCK_SIZE
        if snake_pos[1] >= screen_height:
            snake_pos[1] = 0
        elif snake_pos[1] < 0:
            snake_pos[1] = screen_height - BLOCK_SIZE
            
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over_message(score)
                main()

        show_score(score)
        pygame.display.update()
        clock.tick(snake_speed)

if __name__ == '__main__':
    main()