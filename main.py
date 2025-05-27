import pickle
from collections import Counter
import neat.config
import pygame
import neat
import os
from config import GRID_WIDTH, GRID_HEIGHT
from game import Game
from ai_controller import SnakeAI
import game_logic

def eval_genomes(genomes, config, visualize=False):
    if visualize:
        pygame.init()
        win = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
        FPS = 10
        clock = pygame.time.Clock()
    else:
        win = None
        clock = None
    games = []
    snakes = []
    genomes_list = []
    for _, genome in genomes:
        game = Game()
        ai_snake = SnakeAI(genome, config)
        games.append(game)
        snakes.append(ai_snake)
        genomes_list.append(genome)
        genome.fitness = 0

        genome.steps_without_apple = 0
        genome.position_history = []
        genome.loop_count = 0
        genome.steps = 0
        genome.max_steps = 2000
        genome.deaths_by_wall = 0
        genome.deaths_by_self = 0
        genome.last_distance_to_apple = None
        genome.survival_time = 0
        genome.lifetime_apples = 0
        genome.consecutive_closer_move = 0
        genome.visited_positions = {}
    

    while len(games) > 0:
        if clock:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.is_over = True
                    pygame.quit()
                    quit()
        
        idx = 0
        while idx < len(games):
            game = games[idx]
            genome = genomes_list[idx]
            ai_snake = snakes[idx]

            prev_score = game.score
            prev_position = game.snake.body[0]
            snake_length = len(game.snake.body)

            pos_key = str(prev_position)
            genome.visited_positions[pos_key] = genome.visited_positions.get(pos_key, 0) + 1

            genome.position_history.append(prev_position)
            if len(genome.position_history) > max(100, snake_length * 4):
                genome.position_history.pop(0)
            
            max_revisits = max(4, snake_length // 3)
            
            if game.detect_loop(genome.position_history, min_length=6, max_length=40):
                genome.loop_count += 1
                genome.fitness -= min(genome.loop_count * 0.25, 5) / max(1, snake_length/3)
            else:
                genome.loop_count = max(0, genome.loop_count - 0.5)

            if genome.last_distance_to_apple == None:
                genome.last_distance_to_apple = game.snake.distance_to_apple

            inputs = game.game_state()
            action_index = ai_snake.decide(inputs)
            move_direction = ["right", "down", "left", "up"][action_index]
            game.update(move_direction)

            genome.steps += 1
            genome.fitness += 0.01

            current_distance = game.snake.distance_to_apple
            distance_diff = genome.last_distance_to_apple - current_distance
            normalized_distance_diff = distance_diff / (GRID_WIDTH / 4)

            genome.last_distance_to_apple = current_distance

            if distance_diff > 0:
                genome.consecutive_closer_move += 1

                closer_reward = 0.2 + min(0.1 * genome.consecutive_closer_move, 0.8)
                genome.fitness += closer_reward
            else:
                genome.consecutive_closer_move = 0
                genome.fitness -= 0.1 * min(1.0, abs(normalized_distance_diff))


            if game.ate_apple:
                genome.steps_without_apple = 0
                genome.lifetime_apples += 1

                apple_base_reward = 50 
                apple_bonus_reward = genome.lifetime_apples * 5
                genome.fitness += apple_bonus_reward + apple_base_reward

            else:
                genome.steps_without_apple += 1


            current_position = game.snake.body[0]
            position_visits = genome.visited_positions.get(str(current_position), 0)
            if position_visits > max_revisits:
                genome.fitness -= 0.1 * (position_visits - max_revisits)
        
                
            if genome.steps_without_apple > 150:
                genome.fitness -= 0.03 * (genome.steps_without_apple - 150)

                if genome.steps_without_apple > 400 + (snake_length * 10):
                    game.is_over = True

                        
            if game.score > prev_score:
                genome.fitness += 50
                genome.steps_without_apple = 0

                snake_length = len(game.snake.body)
                genome.fitness += min(snake_length * 2, 150)
            
            if genome.loop_count > 20 or genome.steps > genome.max_steps:
                game.is_over = True
            
            if game.game_over():
                genomes_list.pop(idx)
                snakes.pop(idx)
                games.pop(idx)
                if game_logic.hit_the_wall(game.snake, GRID_WIDTH, GRID_HEIGHT):
                    genome.deaths_by_wall +=1
                    genome.fitness -= 8
                elif game_logic.snake_body_collision(game.snake.rects[0], game.snake.rects[1:]):
                    genome.deaths_by_self +=1
                    genome.fitness -= 4
                genome.survival_time = genome.steps
            else:
                idx += 1
            
            if visualize and len(games) > 0:
                game.draw(win)
                font = pygame.font.SysFont('Arial', 20)
                text = font.render(f"Score: {game.score} | Fitness: {genome.fitness:.1f}", True, (255, 255, 255))
                win.blit(text, (10, 10))
                pygame.display.update()

def watch_winner(winner, config):
    pygame.init()
    game = Game()
    ai = SnakeAI(winner, config)

    win = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
    FPS = 10
    clock = pygame.time.Clock()
    while not game.game_over():
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.is_over = True
                pygame.quit()
                quit()
        inputs = game.game_state()
        action_index = ai.decide(inputs)
        move_direction = ["right", "down", "left", "up"][action_index]
        game.update(move_direction)
        game.draw(win)
        font = pygame.font.SysFont('Arial', 30)
        text = font.render(f"Score: {game.score} | Fitness: {winner.fitness:.1f}", True, (0, 0, 0))
        win.blit(text, (10, 10))
        pygame.display.update()

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    os.makedirs("checkpoints", exist_ok = True)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    checkpoint_reporter = neat.Checkpointer(
        generation_interval=5,
        time_interval_seconds=300,
        filename_prefix="checkpoints/neat-checkpoint-"
    )
    population.add_reporter(checkpoint_reporter)

    winner = population.run(eval_genomes, 5000)
    print("The winner is:", winner)
    print("The winner fitness is:", winner.fitness)
    with open("winner_snake.pkl", "wb") as f:
        pickle.dump(winner, f)
    best_ever = stats.best_genome() 
    watch_winner(best_ever,config)
    print("The best ever is:", best_ever)
    print("The best ever fitness is:", best_ever.fitness)
    with open("best_genome_snake.pkl", "wb") as f:
        pickle.dump(best_ever, f)

    

if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    config_path = os.path.join(current_dir, "config-feedforward.txt")
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    with open("/Users/ipektufekcioglu/Desktop/Python Projects/AI_Snake/best_genome_snake.pkl", "rb") as f:
        best = pickle.load(f)
    watch_winner(best,config)
    print(best.fitness)
    """
    run(config_path)