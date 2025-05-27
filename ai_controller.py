import neat
import numpy as np


class SnakeAI:

    def __init__(self, genome, config):
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.last_direction = "right"
        self.invalid_moves = {
            "right":"left",
            "left":"right",
            "up":"down",
            "down":"up"
        }
        self.direction_map = ["right", "down", "left", "up"]
        self.move_history = []


    def decide(self, inputs):
        output = self.net.activate(inputs)

        invalid_direction = self.invalid_moves[self.last_direction]
        invalid_index = self.direction_map.index(invalid_direction) if invalid_direction in self.direction_map else -1

        masked_outputs = output.copy()
        if invalid_index >= -1:
            output[invalid_index] -= 100
        
        direction_index = np.argmax(masked_outputs)
        self.last_direction = self.direction_map[direction_index]
        if len(self.move_history) > 10:
            self.move_history.pop(0)

        return direction_index