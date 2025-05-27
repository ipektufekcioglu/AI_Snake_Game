import pygame
from snake import Snake
from apple import Apple
import config
import game_logic
from assets import WALL, BACKGROUND, APPLE
import utils
import game


def draw_window(win, snake, apple, wall, background, rotated_snake, corner_img_list, corner_flag):
    win.fill((0,0,0))
    win.blit(background)
    win.blit(wall)
    snake.draw(win, rotated_snake, corner_img_list, corner_flag)
    apple.draw(win)

    pygame.display.update()


def main():
    pygame.init()
    win = pygame.display.set_mode((config.GRID_WIDTH, config.GRID_HEIGHT))
    
    snake = Snake()
    apple = Apple()
    wall = WALL
    background = BACKGROUND
  
    FPS = 10
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        previous_dir = snake.snake_directions
        new_direction = game_logic.calc_next_move(snake, apple)
        snake.move(new_direction)
        
        rotation_info = game_logic.rotate_images(snake.snake_img, previous_dir, snake.snake_directions, snake.corner, snake)
        snake.snake_img = rotation_info[0]
        snake.corner_flag = rotation_info[1]
        corner_images = rotation_info[2]

        snake_head_rect = snake.rects[0]
        snake_body_rect = snake.rects[1:]
        apple_rect = apple.rect
        if game_logic.check_apple_eating(snake_head_rect, apple_rect):
            print("ate")
            apple.respawn(snake.body)
            snake.grow()
        
        if game_logic.hit_the_wall(snake, config.GRID_WIDTH, config.GRID_HEIGHT):
            run = False
            
        draw_window(win, snake, apple, wall, background, snake.snake_img, corner_images, snake.corner_flag)

main()

