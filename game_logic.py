import pygame
import random
import utils
import snake
import math


def check_apple_eating(snake_head, apple):
    if snake_head.colliderect(apple): 
            return True
    return False

def snake_body_collision(snake_head, snake_body):
    for rect in snake_body:
        if snake_head.colliderect(rect):
            return True
    return False

def calculate_distance(snake_head, apple):
    distance = math.sqrt((snake_head[0] - apple.x) ** 2 + (snake_head[1] - apple.y) ** 2)
    return distance

def is_closer_to_apple(prev_dist, new_dist):
    if new_dist < prev_dist:
        return True
    return False

def hit_the_wall(snake, grid_width, grid_height):
    collision = False
    if snake.body[0][0] <= 32 or snake.body[0][0] >= grid_width - 32:
        collision = True
    elif snake.body[0][1] <= 32 or snake.body[0][1] >= grid_height - 32:
        collision = True
    return collision
    
def calc_next_move(snake, apple):
    move_choices = []
    snake_head = snake.body[0]
    print("snake head",snake_head[0])
    if snake_head[0] > apple.x:
        move_choices.append("left")
    elif snake_head[0] < apple.x:
        move_choices.append("right")

    if snake_head[1] > apple.y:
        move_choices.append("up")
    elif snake_head[1] < apple.y:
        move_choices.append("down")

    if utils.opposite_direction(snake.head_dir) not in move_choices:
        if len(move_choices) > 1:
            choice = random.choices(move_choices, [20, 1])[0]
        else:
            choice = random.choices(move_choices)[0]
    else:
        move_choices.remove(utils.opposite_direction(snake.head_dir))
        if len(move_choices) == 0:
            if snake_head[0] == apple.x:
                move_choices.append(random.choice(["right", "left"]))
            elif snake_head[1] == apple.y:
                move_choices.append(random.choice(["down", "up"]))
        choice = move_choices[0]
    return choice

def rotate_images(images, previous_dir, new_dir, corner, snake):
    rotations = ["right", "down", "left", "up"]
    rot_angles = [-90, 90]
    rotated_snake = []
    flaged = []
    snake.corner_images = []
    for idx, (img, prev, new) in enumerate(zip(images, previous_dir, new_dir)):
        prev_ind = rotations.index(prev)
        new_ind = rotations.index(new)
        if abs(new_ind - prev_ind) > 0:
            flaged.append(1)
            snake.corner_images.append(rotate_corner(prev, new, corner))
        else:
            flaged.append(0)
            
        if idx == len(images) -1:
            prev_ind = rotations.index(previous_dir[idx-1])
            new_ind = rotations.index(new_dir[idx-1])

        if new_ind - prev_ind > 1:
            rotated_snake.append(pygame.transform.rotate(img, rot_angles[1]))
        elif new_ind - prev_ind < -1:
            rotated_snake.append(pygame.transform.rotate(img, rot_angles[0])) 
        elif new_ind - prev_ind == 1:
            rotated_snake.append(pygame.transform.rotate(img, rot_angles[0])) 
        elif new_ind - prev_ind == -1:
            rotated_snake.append(pygame.transform.rotate(img, rot_angles[1])) 
        else:
            rotated_snake.append(img)
    images = rotated_snake
    return images, flaged, snake.corner_images

def rotate_new_body_img(tail_direction, body_image):
    if tail_direction == "right" or tail_direction == "left":
        img = body_image
    elif tail_direction == "up":
        img = pygame.transform.rotate(body_image, 90)
    else:
        img = pygame.transform.rotate(body_image, -90)
    return img

def rotate_tail(tail_direction, body_image):
    if tail_direction == "right":
        img = body_image
    elif tail_direction == "left":
        img = pygame.transform.rotate(body_image, 180)
    elif tail_direction == "down":
        img = pygame.transform.rotate(body_image, -90)
    else:
        img = pygame.transform.rotate(body_image, 90)
    return img


def rotate_corner(prev, new, corner):
    img = corner
    if (prev == "up" and new == "right") or (prev == "left" and new == "down"):
        img = corner
    elif (prev == "right" and new == "down") or (prev == "up" and new == "left"):
        img = pygame.transform.rotate(corner, -90)
    elif (prev == "down" and new == "left") or (prev == "right" and new == "up"):
        img = pygame.transform.rotate(corner, -180)
    elif (prev == "left" and new == "up") or (prev == "down" and new == "right"):
        img = pygame.transform.rotate(corner, -270)
    return img