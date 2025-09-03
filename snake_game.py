import pygame, random, asyncio
pygame.init()
W, H, GS = 600, 600, 20
GW, GH = W//GS, H//GS
FPS = 10
BLACK, WHITE = (0,0,0), (255,255,255)
GREEN, RED = (0,255,0), (255,0,0)
BLUE, YELLOW, PURPLE, GRAY = (0,120,255), (255,255,0), (180,0,255), (100,100,100)
UP, DOWN, LEFT, RIGHT = (0,-1), (0,1), (-1,0), (1,0)
class Snake:
    def __init__(self):
        self.positions = [(GW//2, GH//2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = self.grow_to = 3
        self.speed_boost = self.invincible = 0  
    def get_head_position(self): return self.positions[0]
    def turn(self, point):
        if self.grow_to > 3 and (point[0]*-1, point[1]*-1) == self.direction: return
        self.direction = point
    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new = ((head[0]+x)%GW, (head[1]+y)%GH)
        if not self.invincible and new in self.positions[1:]: 
            self.__init__()
            return True    
        self.positions.insert(0, new)
        if len(self.positions) > self.grow_to: self.positions.pop()
        if self.speed_boost > 0: self.speed_boost -= 1
        return False
    def draw(self, s):
        for i, p in enumerate(self.positions):
            r = pygame.Rect((p[0]*GS, p[1]*GS), (GS, GS))
            color = PURPLE if self.invincible else BLUE if self.speed_boost else GREEN
            pygame.draw.rect(s, color, r)
            pygame.draw.rect(s, BLACK, r, 1)
class Food:
    def __init__(self):
        self.position = (0,0)
        self.randomize_position()
    def randomize_position(self):
        self.position = (random.randint(0,GW-1), random.randint(0,GH-1))
        r = random.random()
        self.type = "normal" if r < 0.7 else "speed" if r < 0.9 else "invincible"
    def draw(self, s):
        r = pygame.Rect((self.position[0]*GS, self.position[1]*GS), (GS, GS))
        color = RED if self.type=="normal" else YELLOW if self.type=="speed" else PURPLE
        pygame.draw.rect(s, color, r)
        pygame.draw.rect(s, BLACK, r, 1)
async def main():
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()
    snake, food = Snake(), Food()
    font = pygame.font.SysFont('Arial', 20)
    game_over = False
    current_speed = FPS 
    obstacles = []     # Generate obstacles
    for _ in range(5):
        pos = (random.randint(0,GW-1), random.randint(0,GH-1))
        while pos in obstacles: pos = (random.randint(0,GW-1), random.randint(0,GH-1))
        obstacles.append(pos)
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP: snake.turn(UP)
                elif e.key == pygame.K_DOWN: snake.turn(DOWN)
                elif e.key == pygame.K_LEFT: snake.turn(LEFT)
                elif e.key == pygame.K_RIGHT: snake.turn(RIGHT)
                elif e.key == pygame.K_r and game_over:
                    snake, food = Snake(), Food()
                    game_over = False
                    current_speed = FPS
        if not game_over:
            current_speed = FPS*2 if snake.speed_boost else FPS
            game_over = snake.move()
            if not snake.invincible and snake.get_head_position() in obstacles:
                snake, food = Snake(), Food()
                game_over = True
            if snake.get_head_position() == food.position:
                if food.type == "normal": snake.grow_to += 1
                snake.score += 1 if food.type=="normal" else 2 if food.type=="speed" else 3
                if food.type == "speed": snake.speed_boost = 15
                if food.type == "invincible": snake.invincible = True
                food.randomize_position()
                while food.position in snake.positions or food.position in obstacles:
                    food.randomize_position()
        screen.fill(BLACK)
        for y in range(0, H, GS):
            for x in range(0, W, GS):
                pygame.draw.rect(screen, WHITE, pygame.Rect((x, y), (GS, GS)), 1)
        for p in obstacles:
            pygame.draw.rect(screen, GRAY, pygame.Rect((p[0]*GS, p[1]*GS), (GS, GS)))
        snake.draw(screen)
        food.draw(screen)
        screen.blit(font.render(f'Score: {snake.score}', True, WHITE), (5, 5))
        if snake.speed_boost: screen.blit(font.render(f'Speed: {snake.speed_boost}', True, YELLOW), (5, 30))
        if snake.invincible: screen.blit(font.render('Invincible!', True, PURPLE), (5, 55))
        if game_over:
            screen.blit(font.render('Game Over! Press R to restart', True, RED), (W//2-180, H//2))
        pygame.display.update()
        clock.tick(current_speed)
        await asyncio.sleep(0)
if __name__ == "__main__":
    asyncio.run(main())