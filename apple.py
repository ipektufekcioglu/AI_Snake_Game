import pygame
import random
from assets import APPLE
import config
import utils

class Apple:
    def __init__(self):
        self.x = utils.random_tiles()
        self.y = utils.random_tiles()
        self.apple_img = APPLE
        self.rect = self.apple_img.get_rect(topleft=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.apple_img)
        #self.x = random.randint(config.WALL_WIDTH, config.GRID_WIDTH - config.WALL_WIDTH - config.TILE_WIDTH)
        #self.y = random.randint(config.WALL_WIDTH, config.GRID_HEIGHT - config.WALL_WIDTH - config.TILE_HEIGHT)
        self.eaten = False

    def respawn(self, snake_pos):
        self.x, self.y = utils.randint_exclude(snake_pos)
        self.rect = self.apple_img.get_rect(topleft=(self.x, self.y))   
        self.mask = pygame.mask.from_surface(self.apple_img) 

    def draw(self, win):
        win.blit(self.apple_img, (self.x, self.y))
        


