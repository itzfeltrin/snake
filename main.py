import random

import pygame
from pygame.locals import *

pygame.init()

grid_size = 32
grid_count = 32
screen_size = grid_size * grid_count

screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
fps = 15


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = Rect(0, 0, grid_size, grid_size)
        self.speed_x = 0
        self.speed_y = 0
        self.tail = []

    def move(self, speed_x, speed_y):
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move_tail(self):
        temp_pos_x = self.rect.x
        temp_pos_y = self.rect.y
        for index, tail_block in enumerate(self.tail):
            loop_temp_x = tail_block.x
            loop_temp_y = tail_block.y
            self.tail[index].x = temp_pos_x
            self.tail[index].y = temp_pos_y
            temp_pos_x = loop_temp_x
            temp_pos_y = loop_temp_y

    def update(self):
        if len(self.tail) > 0:
            self.move_tail()

        self.rect.x += self.speed_x * grid_size
        self.rect.y += self.speed_y * grid_size
        if self.rect.x > grid_count * grid_size:
            self.rect.x = 0
        elif self.rect.x < 0:
            self.rect.x = grid_count * grid_size
        if self.rect.y > grid_count * grid_size:
            self.rect.y = 0
        elif self.rect.y < 0:
            self.rect.y = grid_count * grid_size
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

        if pygame.sprite.spritecollide(self, food_group, True):
            self.tail.append(Rect(self.rect))
            food_group.add(Food())

        for tail_block in self.tail:
            pygame.draw.rect(screen, (255, 255, 255), tail_block)


class Food(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('assets/img/food.png').convert_alpha()
        self.image = pygame.transform.scale(image, (grid_size, grid_size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 31) * grid_size
        self.rect.y = random.randint(0, 31) * grid_size


snake = Snake()

food = Food()
food_group = pygame.sprite.Group()
food_group.add(food)

font = pygame.font.Font('assets/font/8bitwonder.ttf', 20)

run = True
while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_RIGHT:
                snake.move(1, 0)
            if event.key == pygame.K_LEFT:
                snake.move(-1, 0)
            if event.key == pygame.K_UP:
                snake.move(0, -1)
            if event.key == pygame.K_DOWN:
                snake.move(0, 1)

    screen.fill((20, 18, 0))

    # for i in range(1, grid_count):
    #     # horizontal line
    #     pygame.draw.line(screen, (255, 255, 255), (0, i * grid_size), (screen_size, i * grid_size), 1)
    #     # vertical line
    #     pygame.draw.line(screen, (255, 255, 255), (i * grid_size, 0), (i * grid_size, screen_size), 1)

    food_group.update()
    food_group.draw(screen)
    snake.update()

    score_img = font.render(f'score {len(snake.tail)}', True, (255, 255, 255))
    screen.blit(score_img, (screen_size - score_img.get_width(), 0))

    pygame.display.update()

pygame.quit()
