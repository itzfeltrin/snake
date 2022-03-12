import pygame
from pygame.locals import *

pygame.init()

grid_size = 20
grid_count = 32
screen_size = grid_size * grid_count

screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
fps = 15


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 0
        self.speed_x = 0
        self.speed_y = 0

    def move(self, speed_x, speed_y):
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        rect = Rect(self.x * grid_size, self.y * grid_size, grid_size, grid_size)
        pygame.draw.rect(screen, (255, 0, 0), rect)


snake = Snake()

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

    for i in range(1, grid_count):
        # horizontal line
        pygame.draw.line(screen, (255, 255, 255), (0, i * grid_size), (screen_size, i * grid_size), 1)
        # vertical line
        pygame.draw.line(screen, (255, 255, 255), (i * grid_size, 0), (i * grid_size, screen_size), 1)

    snake.update()

    pygame.display.update()

pygame.quit()
