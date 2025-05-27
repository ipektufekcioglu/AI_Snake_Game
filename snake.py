import pygame
from assets import HEAD, BODY, TAIL, CORNER
import game_logic
import utils


class Snake:
    TILE_WIDTH = 32
    DIRECTIONS = ["right", "down", "left", "up"]
    VEL = 32

    def __init__(self):
        self.body = [(96 + self.TILE_WIDTH + self.TILE_WIDTH, 384), (96 + self.TILE_WIDTH, 384), (96, 384)]  #head, body, tail
        self.vel = self.VEL
        self.snake_directions = ["right", "right", "right"]
        self.head_dir = "right"
        self.snake_img =  [HEAD, BODY, TAIL]
        self.corner = CORNER
        self.corner_images = []
        self.corner_flag = [0,0,0]
        self.rects = [img.get_rect(topleft=(pos)) for img, pos in zip(self.snake_img, self.body)]
        self.mask = pygame.mask.from_surface(self.snake_img[0])

    def move(self, direction):
        self.head_dir = direction
        self.snake_directions = utils.update_direction(self.snake_directions, self.head_dir)
        for i, part in enumerate(self.snake_directions):
            if part == "right":
                self.body[i] = (self.body[i][0] + self.VEL, self.body[i][1])
            if part == "left":
                self.body[i] = (self.body[i][0] - self.VEL, self.body[i][1])
            if part == "down":
                self.body[i] = (self.body[i][0], self.body[i][1] + self.VEL)
            if part == "up":
                self.body[i] = (self.body[i][0], self.body[i][1] - self.VEL)
        for i, rect in enumerate(self.rects):
            rect.topleft = self.body[i]
        self.mask = pygame.mask.from_surface(self.snake_img[0]) 
        


    def grow(self):
        self.body.insert(-1, (self.body[-1][0], self.body[-1][1]))
        if self.snake_directions[-1] == "right":
            self.body[-1] = (self.body[-1][0] - self.TILE_WIDTH, self.body[-1][1])
        if self.snake_directions[-1] == "left":
            self.body[-1] = (self.body[-1][0] + self.TILE_WIDTH, self.body[-1][1])
        if self.snake_directions[-1] == "down":
            self.body[-1] = (self.body[-1][0], self.body[-1][1] - self.TILE_WIDTH)
        if self.snake_directions[-1] == "up":
            self.body[-1] = (self.body[-1][0], self.body[-1][1] + self.TILE_WIDTH)
        self.snake_img[-1] = game_logic.rotate_tail(self.snake_directions[-1], TAIL)
        
        new_body_img = game_logic.rotate_new_body_img(self.snake_directions[-1], BODY)
        self.snake_img.insert(-1, new_body_img)
        self.snake_directions.insert(-1, self.snake_directions[-1])
        self.corner_flag.insert(-1, self.corner_flag[-1])
        new_rect = new_body_img.get_rect(topleft = self.body[-2])
        self.rects.insert(-1, new_rect)
        

    def draw(self, win, rotated_snake, corner_img_list, corner_flag):
        corner_slided = utils.slide_right(corner_flag)
        for idx, (corner, rotated, part) in enumerate(zip(corner_slided,rotated_snake, self.body)):
            if corner == 1:
                win.blit(corner_img_list[0], part)
                corner_img_list.pop(0)
            else:
                win.blit(rotated, part)

        
        