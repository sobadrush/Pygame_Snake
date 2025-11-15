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
    YELLOW = pygame.Color(255, 255, 0)
    CYAN = pygame.Color(0, 255, 255)
    MAGENTA = pygame.Color(255, 0, 255)
    ORANGE = pygame.Color(255, 165, 0)


class Snake:
    """貪食蛇類別"""
    
    def __init__(self, is_auto_run=False, start_pos=None, color=None):
        """
        初始化蛇的位置與身體
        
        參數:
            is_auto_run: 是否為 AI 自動控制
            start_pos: 起始位置 [x, y]，若為 None 則使用隨機位置
            color: 蛇的顏色，若為 None 則使用預設綠色
        """
        self.is_auto_run = is_auto_run
        self.color = color or Config.GREEN
        
        # 決定起始位置
        if start_pos is None:
            # 隨機生成起始位置
            x = random.randrange(3, (Config.SCREEN_WIDTH // Config.BLOCK_SIZE) - 3) * Config.BLOCK_SIZE
            y = random.randrange(3, (Config.SCREEN_HEIGHT // Config.BLOCK_SIZE) - 3) * Config.BLOCK_SIZE
            self.position = [x, y]
        else:
            self.position = list(start_pos)
        
        # 隨機選擇初始方向
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        
        # 根據方向建立初始蛇身
        self.body = [list(self.position)]
        for i in range(1, 3):
            if self.direction == 'RIGHT':
                self.body.append([self.position[0] - i * Config.BLOCK_SIZE, self.position[1]])
            elif self.direction == 'LEFT':
                self.body.append([self.position[0] + i * Config.BLOCK_SIZE, self.position[1]])
            elif self.direction == 'DOWN':
                self.body.append([self.position[0], self.position[1] - i * Config.BLOCK_SIZE])
            elif self.direction == 'UP':
                self.body.append([self.position[0], self.position[1] + i * Config.BLOCK_SIZE])
    
    def auto_decide_direction(self, food_pos):
        """
        AI 自動決定移動方向（簡單邏輯：追蹤食物）
        
        參數:
            food_pos: 食物位置 [x, y]
        """
        if not self.is_auto_run:
            return
        
        # 計算與食物的距離
        dx = food_pos[0] - self.position[0]
        dy = food_pos[1] - self.position[1]
        
        # 優先選擇距離較遠的軸向移動
        if abs(dx) > abs(dy):
            # 橫向距離較遠
            if dx > 0:
                self.change_direction('RIGHT')
            else:
                self.change_direction('LEFT')
        else:
            # 縱向距離較遠
            if dy > 0:
                self.change_direction('DOWN')
            else:
                self.change_direction('UP')
    
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
            pygame.draw.rect(screen, self.color, 
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
        
        # 建立玩家控制的蛇（綠色）
        self.snake = Snake(is_auto_run=False, start_pos=[100, 60], color=Config.GREEN)
        
        # 建立 AI 蛇（黃色），使用隨機起始位置
        self.ai_snake = Snake(is_auto_run=True, start_pos=None, color=Config.YELLOW)
        
        # 建立食物和毒藥
        self.food = Food(Config.RED)
        self.poison = Food(Config.BLUE)
        
        # 生成初始食物和毒藥（避開所有蛇）
        all_snake_bodies = self.snake.body + self.ai_snake.body + self.ai_snake2.body
        self.food.spawn(all_snake_bodies)
        self.poison.spawn(all_snake_bodies, self.food.position)
    
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
        # AI 蛇自動決定方向
        self.ai_snake.auto_decide_direction(self.food.position)
        
        # 移動所有蛇
        self.snake.move()
        self.ai_snake.move()
        
        # 檢查玩家的蛇是否吃到食物
        if self.snake.position == self.food.position:
            self.score += 10
            self.snake.grow()
            all_snake_bodies = self.snake.body + self.ai_snake.body
            self.food.spawn(all_snake_bodies, self.poison.position)
        # 檢查玩家的蛇是否吃到毒藥
        elif self.snake.position == self.poison.position:
            return False  # 遊戲結束
        else:
            self.snake.update_body()
        
        # 檢查 AI 蛇是否吃到食物
        if self.ai_snake.position == self.food.position:
            self.ai_snake.grow()
            all_snake_bodies = self.snake.body + self.ai_snake.body
            self.food.spawn(all_snake_bodies, self.poison.position)
        # 檢查 AI 蛇是否吃到毒藥
        elif self.ai_snake.position == self.poison.position:
            # AI 蛇死亡後重生
            self.ai_snake = Snake(is_auto_run=True, start_pos=None, color=Config.YELLOW)
        else:
            self.ai_snake.update_body()
        
        # 檢查玩家的蛇是否撞到自己或 AI 蛇
        if self.snake.check_self_collision():
            return False  # 遊戲結束
        if self.snake.position in self.ai_snake.body:
            return False  # 撞到 AI 蛇，遊戲結束
        
        # AI 蛇撞到自己則重生
        if self.ai_snake.check_self_collision():
            self.ai_snake = Snake(is_auto_run=True, start_pos=None, color=Config.YELLOW)
        
        return True  # 遊戲繼續
    
    def draw(self):
        """繪製遊戲畫面"""
        self.screen.fill(Config.BLACK)
        self.snake.draw(self.screen)
        self.ai_snake.draw(self.screen)  # 繪製 AI 蛇
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
