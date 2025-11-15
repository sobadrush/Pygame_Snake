import pygame
import sys
import random


class Config:
    """遊戲設定"""
    SCREEN_WIDTH = 720
    SCREEN_HEIGHT = 480
    BLOCK_SIZE = 20
    FPS = 15
    
    # 顏色定義
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    RED = pygame.Color(255, 0, 0)
    GREEN = pygame.Color(0, 255, 0)
    BLUE = pygame.Color(0, 0, 255)


class Snake:
    """貪食蛇類別"""
    
    def __init__(self):
        """初始化蛇的位置與身體"""
        self.position = [100, 60]
        self.body = [[100, 60], [80, 60], [60, 60]]
        self.direction = 'RIGHT'
    
    def change_direction(self, new_direction):
        """改變移動方向（防止反向移動）"""
        opposite = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_direction != opposite[self.direction]:
            self.direction = new_direction
    
    def move(self):
        """根據方向移動蛇頭"""
        if self.direction == 'UP':
            self.position[1] -= Config.BLOCK_SIZE
        elif self.direction == 'DOWN':
            self.position[1] += Config.BLOCK_SIZE
        elif self.direction == 'LEFT':
            self.position[0] -= Config.BLOCK_SIZE
        elif self.direction == 'RIGHT':
            self.position[0] += Config.BLOCK_SIZE
        
        # 處理邊界穿越
        self.position[0] %= Config.SCREEN_WIDTH
        self.position[1] %= Config.SCREEN_HEIGHT
    
    def grow(self):
        """蛇身增長（吃到食物時呼叫）"""
        self.body.insert(0, list(self.position))
    
    def update_body(self):
        """更新蛇身（沒吃到食物時移除尾巴）"""
        self.body.insert(0, list(self.position))
        self.body.pop()
    
    def check_self_collision(self):
        """檢查是否撞到自己"""
        return self.position in self.body[1:]
    
    def draw(self, screen):
        """繪製蛇"""
        for segment in self.body:
            pygame.draw.rect(screen, Config.GREEN, 
                           pygame.Rect(segment[0], segment[1], 
                                     Config.BLOCK_SIZE, Config.BLOCK_SIZE))


class Food:
    """食物類別"""
    
    def __init__(self, color=None):
        """初始化食物"""
        self.color = color or Config.RED
        self.position = [0, 0]
    
    def spawn(self, snake_body, *other_positions):
        """生成食物（避免與蛇身和其他物件重疊）"""
        while True:
            x = random.randrange(0, Config.SCREEN_WIDTH // Config.BLOCK_SIZE) * Config.BLOCK_SIZE
            y = random.randrange(0, Config.SCREEN_HEIGHT // Config.BLOCK_SIZE) * Config.BLOCK_SIZE
            self.position = [x, y]
            
            # 確保不與蛇身或其他物件重疊
            if self.position not in snake_body and \
               all(self.position != pos for pos in other_positions):
                break
    
    def draw(self, screen):
        """繪製食物"""
        pygame.draw.rect(screen, self.color, 
                        pygame.Rect(self.position[0], self.position[1], 
                                  Config.BLOCK_SIZE, Config.BLOCK_SIZE))


class Game:
    """遊戲主控制類別"""
    
    def __init__(self):
        """初始化遊戲"""
        pygame.init()
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption('貪食蛇新手村 (OOP版)')
        self.clock = pygame.time.Clock()
        self.score = 0
        
        # 建立遊戲物件
        self.snake = Snake()
        self.food = Food(Config.RED)
        self.poison = Food(Config.BLUE)
        
        # 生成初始食物和毒藥
        self.food.spawn(self.snake.body)
        self.poison.spawn(self.snake.body, self.food.position)
    
    def handle_input(self):
        """處理使用者輸入"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.snake.change_direction('UP')
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.snake.change_direction('DOWN')
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.snake.change_direction('LEFT')
                elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.snake.change_direction('RIGHT')
    
    def update(self):
        """更新遊戲狀態"""
        self.snake.move()
        
        # 檢查是否吃到食物
        if self.snake.position == self.food.position:
            self.score += 10
            self.snake.grow()
            self.food.spawn(self.snake.body, self.poison.position)
        # 檢查是否吃到毒藥
        elif self.snake.position == self.poison.position:
            return False  # 遊戲結束
        else:
            self.snake.update_body()
        
        # 檢查是否撞到自己
        if self.snake.check_self_collision():
            return False  # 遊戲結束
        
        return True  # 遊戲繼續
    
    def draw(self):
        """繪製遊戲畫面"""
        self.screen.fill(Config.BLACK)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        self.poison.draw(self.screen)
        self.show_score()
        pygame.display.update()
    
    def show_score(self):
        """顯示分數"""
        font = pygame.font.SysFont('consolas', 20)
        score_text = font.render(f'Score: {self.score}', True, Config.WHITE)
        self.screen.blit(score_text, (Config.SCREEN_WIDTH // 10, 15))
    
    def game_over(self):
        """顯示遊戲結束畫面"""
        self.screen.fill(Config.BLACK)
        
        # YOU DIED 文字
        big_font = pygame.font.SysFont('times new roman', 90)
        game_over_text = big_font.render('YOU DIED', True, Config.RED)
        game_over_rect = game_over_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 4))
        self.screen.blit(game_over_text, game_over_rect)
        
        # 分數
        score_font = pygame.font.SysFont('consolas', 30)
        score_text = score_font.render(f'Score: {self.score}', True, Config.WHITE)
        score_rect = score_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        # 重新開始提示
        hint_font = pygame.font.SysFont('consolas', 20)
        hint_text = hint_font.render('Press [R] to Restart or [Q] to Quit', True, Config.WHITE)
        hint_rect = hint_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT * 0.8))
        self.screen.blit(hint_text, hint_rect)
        
        pygame.display.flip()
        
        # 等待使用者選擇
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
    
    def run(self):
        """執行遊戲主迴圈"""
        running = True
        while running:
            self.handle_input()
            running = self.update()
            self.draw()
            self.clock.tick(Config.FPS)
        
        # 遊戲結束
        self.game_over()


def main():
    """主程式進入點"""
    while True:
        game = Game()
        game.run()


if __name__ == '__main__':
    main()
