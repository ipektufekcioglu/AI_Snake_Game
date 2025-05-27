import pygame
import os

pygame.init()
pygame.display.set_mode((1, 1))

SPRITES_PATH = os.path.join(os.path.dirname(__file__), "Sprites")


def load_images(img_path, img_size):
    path = os.path.join(SPRITES_PATH, img_path)
    sprite = pygame.transform.scale(pygame.image.load(path).convert_alpha(), img_size)
    return sprite

HEAD = load_images("head.png", (32, 32))
BODY = load_images("body.png", (32, 32))
TAIL = load_images("tail.png", (32, 32))
APPLE = load_images("apple.png", (32, 32))
WALL = load_images("wall.png", (800, 800))
BACKGROUND = load_images("background.png", (800, 800))
CORNER = load_images("corner.png", (32, 32))