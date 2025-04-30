import pygame
import random
import time

pygame.init()
pygame.mixer.init()

WINDOW_SIZE = 600
GRID_SIZE = 50
GRID_COUNT = WINDOW_SIZE // GRID_SIZE
HEAD_SIZE = GRID_SIZE
FOOD_SIZE = 50
SEGMENT_SPACING = 5  
SEGMENT_SIZE = GRID_SIZE - (SEGMENT_SPACING * 2)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Hichem Cook")

head_img = pygame.image.load("images/face.png")
head_img = pygame.transform.scale(head_img, (SEGMENT_SIZE, SEGMENT_SIZE))
food_img = pygame.image.load("images/pizza.png")
food_img = pygame.transform.scale(food_img, (FOOD_SIZE, FOOD_SIZE))

pygame.display.set_icon(pygame.transform.scale(head_img, (32, 32)))

eat_sound = pygame.mixer.Sound("sounds/benna-karita.WAV")
lose_sound = pygame.mixer.Sound("sounds/hichem-loose.WAV")

font = pygame.font.Font(None, 36)

class Snake:
    def __init__(self):
        self.body = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = [1, 0]
        self.grow = False
        self.score = 0
        self.move_counter = 0
        self.move_delay = 10

    def move(self):
        self.move_counter += 1
        if self.move_counter < self.move_delay:
            return True

        self.move_counter = 0
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        new_head = (new_head[0] % GRID_COUNT, new_head[1] % GRID_COUNT)
        
        if new_head in self.body[1:]:
            lose_sound.play()
            return False
        
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
            self.score += 10
        return True

    def draw(self):
        for i, segment in enumerate(self.body):
            if i == 0:
                x = segment[0] * GRID_SIZE + SEGMENT_SPACING
                y = segment[1] * GRID_SIZE + SEGMENT_SPACING
                screen.blit(head_img, (x, y))
            else:
                rect = pygame.Rect(
                    segment[0] * GRID_SIZE + SEGMENT_SPACING,
                    segment[1] * GRID_SIZE + SEGMENT_SPACING,
                    SEGMENT_SIZE,
                    SEGMENT_SIZE
                )
                pygame.draw.rect(screen, WHITE, rect, border_radius=8)

class Food:
    def __init__(self):
        self.position = self.generate_position()

    def generate_position(self):
        x = random.randint(0, GRID_COUNT - 1)
        y = random.randint(0, GRID_COUNT - 1)
        return (x, y)

    def draw(self):
        x = self.position[0] * GRID_SIZE - (FOOD_SIZE - GRID_SIZE) // 2
        y = self.position[1] * GRID_SIZE - (FOOD_SIZE - GRID_SIZE) // 2
        screen.blit(food_img, (x, y))

def draw_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WINDOW_SIZE - 150, 10))

def show_game_over(score):
    time.sleep(1.5)
    
    screen.fill(BLACK)
    
    game_over_text = font.render("khsert yakho !", True, RED)
    game_over_rect = game_over_text.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2 - 50))
    screen.blit(game_over_text, game_over_rect)
    
    score_text = font.render(f"score final : {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2 + 10))
    screen.blit(score_text, score_rect)
    
    restart_text = font.render("drok 3la SPACE bech t3wd", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WINDOW_SIZE/2, WINDOW_SIZE/2 + 70))
    screen.blit(restart_text, restart_rect)
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
    return False

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != [0, 1]:
                    snake.direction = [0, -1]
                elif event.key == pygame.K_DOWN and snake.direction != [0, -1]:
                    snake.direction = [0, 1]
                elif event.key == pygame.K_LEFT and snake.direction != [1, 0]:
                    snake.direction = [-1, 0]
                elif event.key == pygame.K_RIGHT and snake.direction != [-1, 0]:
                    snake.direction = [1, 0]

        if not snake.move():
            if not show_game_over(snake.score):
                running = False
            else:
                snake = Snake()
                food = Food()
                continue

        if snake.body[0] == food.position:
            snake.grow = True
            food.position = food.generate_position()
            eat_sound.play()

        screen.fill(BLACK)
        snake.draw()
        food.draw()
        draw_score(snake.score)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
