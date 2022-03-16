import random

import pygame
from pygame.locals import *

pygame.init()

grid_size = 24
grid_count = 32
screen_size = grid_size * grid_count

screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
fps = 15


def get_cell_center(x, y):
    pos_x = x * grid_size + grid_size // 2
    pos_y = y * grid_size + grid_size // 2
    return pos_x, pos_y


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = Rect(0, 0, grid_size, grid_size)
        self.pos_x = 0
        self.pos_y = 0
        self.speed_x = 0
        self.speed_y = 0
        self.tail = []
        self.has_collided = False

    def move(self, speed_x, speed_y):
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move_tail(self):
        index = len(self.tail) - 1
        while index >= 0:
            if index == 0:
                self.tail[index].rect.center = self.rect.center
            else:
                self.tail[index].rect.center = self.tail[index - 1].rect.center
            index -= 1

    def update(self) -> int:
        if self.has_collided:
            return 1  # game over

        self.move_tail()
        for segment in self.tail:
            segment.update()

        self.pos_x += self.speed_x
        self.pos_y += self.speed_y
        if self.pos_x > grid_count - 1:
            self.pos_x = 0
        elif self.pos_x < 0:
            self.pos_x = grid_count - 1
        if self.pos_y > grid_count - 1:
            self.pos_y = 0
        elif self.pos_y < 0:
            self.pos_y = grid_count - 1
        new_pos = get_cell_center(self.pos_x, self.pos_y)

        for segment in self.tail:
            if segment.rect.center == new_pos:
                self.has_collided = True
                return 1  # game over
        if not self.has_collided:
            self.rect.center = new_pos
        pygame.draw.rect(screen, (0, 255, 0), self.rect)

        if pygame.sprite.spritecollide(self, food_group, True):
            self.tail.append(Segment(self.rect.centerx, self.rect.centery))
            food_group.add(Food())

        return 0  # keep playing


class Segment(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        segment_size = grid_size * 0.9
        self.rect = Rect(pos_x, pos_y, segment_size, segment_size)

    def update(self):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)


class Food(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('assets/img/food.png').convert_alpha()
        self.image = pygame.transform.scale(image, (grid_size, grid_size))
        self.rect = self.image.get_rect()
        self.rect.center = get_cell_center(random.randint(1, 31), random.randint(1, 31))


snake = Snake()

food = Food()
food_group = pygame.sprite.Group()
food_group.add(food)

font = pygame.font.Font('assets/font/8bitwonder.ttf', 20)

game_over = 0
# 1 = yes
# 0 = no
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

    screen.fill((255, 255, 255))

    for i in range(1, grid_count):
        # horizontal line
        if i > 1:
            pygame.draw.line(screen, (0, 0, 0), (0, i * grid_size), (screen_size, i * grid_size), 1)
        # vertical line
        pygame.draw.line(screen, (0, 0, 0), (i * grid_size, 0), (i * grid_size, screen_size), 1)

    food_group.update()
    game_over = snake.update()
    food_group.draw(screen)

    score_img = font.render(f'score {len(snake.tail)}', True, (20, 18, 3))
    screen.blit(score_img, (screen_size - score_img.get_width(), 0))

    if game_over == 1:
        for segment in snake.tail:
            segment.update()
        pygame.draw.rect(screen, (0, 255, 0), snake.rect)

        game_over_img = font.render('Game over Press R to restart', True, (20, 18, 3))
        game_over_pos = (
            screen_size // 2 - game_over_img.get_width() // 2, screen_size // 2 - game_over_img.get_height() // 2)
        screen.blit(game_over_img, game_over_pos)

    pygame.display.update()

pygame.quit()
