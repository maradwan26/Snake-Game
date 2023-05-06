import pygame
import sys
import random
from pygame.math import Vector2


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]  # size 3
        self.direction = Vector2(0, 0)
        self.new_block = False

        # head positions
        self.head_up = pygame.image.load('images/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('images/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('images/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('images/head_left.png').convert_alpha()
        # tail positions
        self.tail_up = pygame.image.load('images/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('images/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('images/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('images/tail_left.png').convert_alpha()
        # body
        self.body_vertical = pygame.image.load('images/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('images/body_horizontal.png').convert_alpha()
        # curved bodies
        self.body_tr = pygame.image.load('images/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('images/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('images/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('images/body_bl.png').convert_alpha()
        # sound
        self.munch_sound = pygame.mixer.Sound('sound/munch.mp3')


    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_diff = self.body[1] - self.body[0]

        if head_diff == Vector2(1, 0): self.head = self.head_left
        elif head_diff == Vector2(-1, 0): self.head = self.head_right
        elif head_diff == Vector2(0, 1): self.head = self.head_up
        elif head_diff == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_diff = self.body[-2] - self.body[-1]

        if tail_diff == Vector2(1, 0): self.tail = self.tail_left
        elif tail_diff == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_diff == Vector2(0, 1): self.tail = self.tail_up
        elif tail_diff == Vector2(0, -1): self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def grow(self):
        self.new_block = True

    def munch(self):
        self.munch_sound.play()

    def reset(self):   ###################
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class FOOD:
    def __init__(self):
        self.place_food()

    def draw_food(self):
        food_rect = pygame.Rect(self.x * cell_size, self.y * cell_size, cell_size, cell_size)
        screen.blit(apple, food_rect)

    def place_food(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.position = Vector2(self.x, self.y)


class GAME:
    def __init__(self):
        self.snake = SNAKE()
        self.food = FOOD()

    def update(self):
        self.snake.move_snake()
        self.check_eat()
        self.check_game_over()

    def draw_elements(self):
        self.draw_checkerboard()
        self.food.draw_food()
        self.snake.draw_snake()
        self.draw_score()

    def check_eat(self):
        if self.food.position == self.snake.body[0]:  # <-- head
            self.food.place_food()  # place a new one
            self.snake.grow()
            self.snake.munch()
        # prevent food from spawning on snake
        while self.food.position in self.snake.body[1:]:  # excluding head
            self.food.place_food()


    def check_game_over(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:  # hit wall
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:  # snake head hits itself
                self.game_over()

    def game_over(self):
        self.snake.reset()  ###############

    def draw_checkerboard(self):
        grass_colour = (167, 209, 61)  # dark green
        for row in range(cell_number):
            if row % 2 == 0:
                for column in range(cell_number):
                    if column % 2 != 0:
                        grass_rect = pygame.Rect(column * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_colour, grass_rect)
            else:
                for column in range(cell_number):
                    if column % 2 == 0:
                        grass_rect = pygame.Rect(column * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_colour, grass_rect)


    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)  # subtract initial snake length
        score_surface = score_font.render(score_text, False, (0, 0, 0))
        # top right corner:
        score_x = int(cell_size * cell_number - 42)
        score_y = 35
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))  # same level as score but diff x
        bg_score_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 9 , apple_rect.height)  # surround score+apple

        pygame.draw.rect(screen, (167, 209, 61), bg_score_rect)  # dark green
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (0, 0, 0), bg_score_rect, 3)  # frame w/ line width = 1


pygame.mixer.pre_init(44100, 16, 2, 4096)  # preset
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))  # (W,L)
clock = pygame.time.Clock()
apple = pygame.image.load('images/apple.png').convert_alpha()
score_font = pygame.font.Font('fonts/score_font.ttf', 25)

# background music
background_music = pygame.mixer.Sound('sound/Sutekimeppou.mp3')
background_music.set_volume(0.11)  # volume
background_music.play(-1)  # loop

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 140)  # snake speed (ms)
game = GAME()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and game.snake.direction.y != 1:  # prevent reverse
                game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_a and game.snake.direction.x != 1:  # prevent reverse
                game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_s and game.snake.direction.y != -1:  # prevent reverse
                game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_d and game.snake.direction.x != -1:  # prevent reverse
                game.snake.direction = Vector2(1, 0)

    screen.fill((175, 215, 70))  # light green
    game.draw_elements()
    pygame.display.update()
    clock.tick(60)  # fps
