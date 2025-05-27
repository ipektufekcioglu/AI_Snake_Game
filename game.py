import pygame
import game_logic
from snake import Snake
from apple import Apple
import config
import math
from assets import WALL, BACKGROUND

class Game:

    def __init__(self):
        self.snake = Snake()
        self.apple = Apple()
        self.wall = WALL
        self.background = BACKGROUND
        self.closer_to_apple = False
        self.snake.distance_to_apple = game_logic.calculate_distance((self.snake.body[0][0], self.snake.body[0][1]), self.apple)
        self.is_over = False
        self.score = 0
        self.ate_apple = False
        self.position_history = []
        self.move_history = []

    def game_state(self):
        snake_x, snake_y = self.snake.body[0]
        apple_x, apple_y = self.apple.x, self.apple.y

        dx = (apple_x - snake_x) / config.GRID_WIDTH
        dy = (apple_y - snake_y) / config.GRID_HEIGHT

        direction = self.snake.snake_directions[0]
        dir_right = 1 if direction == "right" else 0
        dir_down = 1 if direction == "down" else 0
        dir_left = 1 if direction == "left" else 0
        dir_up = 1 if direction == "up" else 0

        danger_right = self.is_danger("right")
        danger_right_up = self.is_danger("right_up")
        danger_up = self.is_danger("up")
        danger_left_up = self.is_danger("left_up")
        danger_left = self.is_danger("left")
        danger_left_down = self.is_danger("left_down")
        danger_down = self.is_danger("down")
        danger_right_down = self.is_danger("right_down")
        
        wall_dist_right = ((config.GRID_WIDTH - config.WALL_WIDTH) - snake_x) / config.GRID_WIDTH
        wall_dist_down = ((config.GRID_HEIGHT - config.WALL_WIDTH) - snake_y) / config.GRID_HEIGHT
        wall_dist_left = (snake_x - config.WALL_WIDTH) / config.GRID_WIDTH
        wall_dist_up = (snake_y - config.WALL_WIDTH) / config.GRID_HEIGHT

        apple_right = 1 if apple_x > snake_x else 0
        apple_down = 1 if apple_y > snake_y else 0
        apple_left = 1 if apple_x < snake_x else 0
        apple_up = 1 if apple_y < snake_y else 0
        
        snake_length = len(self.snake.body) / 100

        inputs = [
            dx, dy,
            dir_right, dir_down, dir_left, dir_up,
            danger_right, danger_right_up, danger_up, danger_left_up,
            danger_left, danger_left_down, danger_down, danger_right_down,
            wall_dist_right, wall_dist_down, wall_dist_left, wall_dist_up,
            apple_right, apple_down, apple_left, apple_up,
            snake_length
            ]

        return inputs
    
    def is_danger(self, direction):

        head_x, head_y = self.snake.body[0]

        x, y = head_x, head_y
        if direction == "right":
            x += config.TILE_WIDTH
        elif direction == "left":
            x -= config.TILE_WIDTH
        elif direction == "down":
            y += config.TILE_HEIGHT
        elif direction == "up":
            y -= config.TILE_HEIGHT
        elif direction == "right_up":
            x += config.TILE_WIDTH
            y -= config.TILE_HEIGHT
        elif direction == "right_down":
            x += config.TILE_WIDTH
            y += config.TILE_HEIGHT
        elif direction == "left_up":
            x -= config.TILE_WIDTH
            y -= config.TILE_HEIGHT
        elif direction == "left_down":
            x -= config.TILE_WIDTH
            y += config.TILE_HEIGHT
        
        if x < config.WALL_WIDTH or x > (config.GRID_WIDTH - config.WALL_WIDTH) or y < config.WALL_WIDTH or y > (config.GRID_HEIGHT - config.WALL_WIDTH):
            return 1
        
        if (x, y) in self.snake.body[1:]:
            return 1
        
        return 0
        

    def update(self, move_dir):
        self.ate_apple = False
        if self.is_over:
            return
        
        self.closer_to_apple = False
        
        previous_dir = self.snake.snake_directions
        previous_distance = self.snake.distance_to_apple
        #new_direction = game_logic.calc_next_move(snake, apple)
        self.snake.move(move_dir)

        self.move_history.append(self.snake.body[0])
        if len(self.position_history) > 200:
            self.position_history.pop(0)

        self.snake.distance_to_apple = game_logic.calculate_distance(self.snake.body[0], self.apple)
        if game_logic.is_closer_to_apple(previous_distance, self.snake.distance_to_apple):
            self.closer_to_apple = True

        rotation_info = game_logic.rotate_images(self.snake.snake_img, previous_dir, self.snake.snake_directions, self.snake.corner, self.snake)
        self.snake.snake_img = rotation_info[0]
        self.snake.corner_flag = rotation_info[1]
        self.snake.corner_images = rotation_info[2]

        snake_head_rect = self.snake.rects[0]
        snake_body_rect = self.snake.rects[1:]
        apple_rect = self.apple.rect

        if game_logic.hit_the_wall(self.snake, config.GRID_WIDTH, config.GRID_HEIGHT) or game_logic.snake_body_collision(snake_head_rect, snake_body_rect):
            self.is_over = True

        if game_logic.check_apple_eating(snake_head_rect, apple_rect):
            self.ate_apple = True
            self.score += 1
            self.apple.respawn(self.snake.body)
            self.snake.grow()
            
    
    def detect_loop(self, positions, min_length=3, max_length=30):
        if len(positions) < max_length * 2:
            return False
        
        recent = positions[-max_length * 2:]

        for pattern_len in range(min_length, max_length + 1):
            if len(recent) < pattern_len * 2:
                continue
            
            pattern = recent[-pattern_len:]
            prev_chunk = recent[-(pattern_len * 2): -pattern_len]
            if prev_chunk == pattern:
                repeat_count = 0
                for i in range(2, 5):
                    if len(recent) >= pattern_len * i:
                        check_chunk = recent[-(pattern_len * i): -(pattern_len * (i-1))]
                        if check_chunk == pattern:
                            repeat_count += 1
                        else:
                            break
                if repeat_count >= 1:
                    return True
        return False


        
    def game_over(self):
        return self.is_over
    
    
    def draw(self, win):
        win.fill((0,0,0))
        win.blit(self.background)
        win.blit(self.wall)
        self.snake.draw(win, self.snake.snake_img, self.snake.corner_images, self.snake.corner_flag)
        self.apple.draw(win)

        pygame.display.update()