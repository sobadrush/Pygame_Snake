import pygame
import sys
import time
import random

# 顯示分數
def show_score(score):
    score_font = pygame.font.SysFont('consolas', 20)
    score_surface = score_font.render('Score : ' + str(score), True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (screen_width / 10, 15)
    screen.blit(score_surface, score_rect)

# 生成食物
def generate_food(snake_body):
    while True:
        pos = [random.randrange(0, screen_width // BLOCK_SIZE) * BLOCK_SIZE,
               random.randrange(0, screen_height // BLOCK_SIZE) * BLOCK_SIZE]
        if pos not in snake_body:
            return pos

# Game Over 訊息
def game_over_message(score):
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (screen_width / 2, screen_height / 4)
    screen.blit(game_over_surface, game_over_rect)

    # 這裡可以呼叫 show_score 來顯示最終分數，但我們需要稍作修改
    # 暫時先這樣
    final_score_font = pygame.font.SysFont('consolas', 20)
    final_score_surface = final_score_font.render(
        'Final Score: ' + str(score), True, WHITE)
    final_score_rect = final_score_surface.get_rect()
    final_score_rect.midtop = (screen_width / 2, screen_height / 1.5)
    screen.blit(final_score_surface, final_score_rect)

    pygame.display.flip()

    time.sleep(2)  # 暫停兩秒
    
    # 接下來要處理[重新開始]
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                waiting = False # 結束等待，返回 main 函式



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
snake_speed = 5  # 越大越快

# 遊戲變數
snake_pos = [100, 60]
snake_body = [[100, 60], [80, 60]]
direction = 'RIGHT'
change_to = direction

# 食物位置
food_pos = generate_food(snake_body)

# 分數
score = 0

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
    # 防止180度轉彎
    direction = change_to

    # 更新蛇頭位置
    if direction == 'UP':
        snake_pos[1] -= BLOCK_SIZE
    if direction == 'DOWN':
        snake_pos[1] += BLOCK_SIZE
    if direction == 'LEFT':
        snake_pos[0] -= BLOCK_SIZE
    if direction == 'RIGHT':
        snake_pos[0] += BLOCK_SIZE

    # 畫面渲染
    screen.fill(BLACK)

    # 蛇身體移動機制
    # print(f"list(snake_pos) = {list(snake_pos)}")
    snake_body.insert(0, list(snake_pos))  # 將新蛇頭位置插入蛇身體列表

    # 碰撞與成長
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 10  # 吃到食物，分數增加
        food_pos = generate_food(snake_body)
    else:
        snake_body.pop()  # 移除蛇尾

    for pos in snake_body:
        # pygame.Rect(left, top, width, height)
        pygame.draw.rect(screen, GREEN, pygame.Rect(
            pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

    # 繪製食物
    pygame.draw.circle(
        screen, RED, (food_pos[0] + BLOCK_SIZE // 2, food_pos[1] + BLOCK_SIZE // 2), BLOCK_SIZE // 2)

    # 蛇頭撞到牆壁，遊戲失敗
    if snake_pos[0] < 0 or snake_pos[0] >= screen_width or snake_pos[1] < 0 or snake_pos[1] >= screen_height:
        game_over_message(score)
        pass

    # 蛇頭撞到自己，遊戲吃拜
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over_message(score)
            pass

    show_score(score)
    pygame.display.update()
    clock.tick(snake_speed)
