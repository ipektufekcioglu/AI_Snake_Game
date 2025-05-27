import pygame
import snake
import random
import config
from assets import HEAD, BODY, TAIL

def opposite_direction(head_dir):
    op_dir = None
    if head_dir == "left":
        op_dir = "right"
    elif head_dir == "right":
        op_dir = "left"
    elif head_dir == "up":
        op_dir = "down"
    elif head_dir == "down":
        op_dir = "up"
    return op_dir

def randint_exclude(exclude):
    collides_snake = True
    while collides_snake:
        x = random_tiles()
        y = random_tiles()
        for i, grid in enumerate(exclude):
            if (x + config.TILE_WIDTH, y + config.TILE_HEIGHT) > grid and (x + config.TILE_WIDTH, y + config.TILE_HEIGHT) < (grid[0] + config.TILE_WIDTH, grid[1] + config.TILE_HEIGHT):
                collides_snake = True
                continue
            if collides_snake and i == len(exclude) - 1:
                collides_snake = False
    return x, y

def update_direction(snake_positions, head_direction):
    new_positions = [head_direction]
    for i, pos in enumerate(snake_positions):
        if i == len(snake_positions) - 1:
            break
        new_positions.append(pos)
    return new_positions


def random_tiles():
    choice_list = []
    for i in range(1, 24):
        choice_list.append(32 * i)
    return random.choices(choice_list)[0]

def slide_right(arr):
    slided_arr = [arr[-1]] + arr[:-1]
    slided_arr[0] = 0
    slided_arr[-1] = 0
    return slided_arr
            







    


        





