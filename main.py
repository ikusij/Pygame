from collections import namedtuple
from enum import Enum
import pygame
import random

pygame.init()

font = pygame.font.SysFont("Times New Roman", 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)

BLOCK_SIZE = 20
SPEED = 20

class SnakeGame():

    def __init__(self, width = 640, height = 480):
        self.width = width
        self.height = height

        #TODO INIT DISPLAY
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        
        #TODO INIT GAME STATE
        self.direction = Direction.RIGHT
        self.head = Point(self.width / 2, self.height / 2)
        self.snake = [self.head, Point(self.head.x - BLOCK_SIZE, self.head.y), Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        
        self._place_food()

    def _place_food(self):
        
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        
        self.food = Point(x, y)
        
        if self.food in self.snake:
            self._place_food()

    def _update_ui(self):
        
        self.display.fill(BLACK)
        
        #TODO DRAW SNAKE
        for point in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(point.x + 4, point.y + 4, 12, 12))
        
        #TODO DRAW FOOD
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        #TODO DISPLAY SCORE
        text = font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        
        x, y = self.head.x, self.head.y

        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)

    def _is_collision(self):
        
        #TODO HITS BOUNDARY
        if (self.head.x > self.width - BLOCK_SIZE or self.head.x < 0) or (self.head.y > self.height - BLOCK_SIZE or self.head.y < 0):
            return True
        
        #TODO HITS SELF
        if self.head in self.snake[1:]:
            return True

        return False

    def play(self):
        
        #TODO USER INPUT
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        #TODO MOVE SNAKE
        self._move(self.direction)
        self.snake.insert(0, self.head)

        #TODO CHECK IF GAME OVER
        game_over = False
        
        if self._is_collision():
            game_over = True

        #TODO PLACE NEW FOOD OR MOVE
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        #TODO UPDATE BOARD AND CLOCK
        self._update_ui()
        self.clock.tick(SPEED)

        #TODO RETURN GAME OVER AND SCORE
        return game_over, self.score

if __name__ == "__main__":
    game = SnakeGame()

    #TODO GAME LOOP
    while True:
        
        game_over, score = game.play()

        #TODO BREAK IF GAME OVER
        if game_over:
            break
    
    print(f'Final Score: {score}')

    pygame.quit()