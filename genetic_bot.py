from neuron_for_genetic import NeuronNetwork
import random

class GeneticBot:
    def __init__(self, input_size, hidden_size):
        self.network = NeuronNetwork(input_size, hidden_size)
        self.fitness = 0

    def decide(self, inputs):
        output = self.network.feedforward(inputs)
        return output[0] > 0.5  # Return True to flap, False to do nothing

    def get_chromosome(self):
        return self.network.chromosome()
    
    def crossover(self, other_bot):
        child = GeneticBot(self.network.input_size, self.network.hidden_size)
        child_chromosome = []
        for gene1, gene2 in zip(self.get_chromosome(), other_bot.get_chromosome()):
            child_chromosome.append(gene1 if random.random() < 0.5 else gene2)
        child.network.weights_input_hidden = [child_chromosome[i:i + self.network.hidden_size] for i in range(0, len(child_chromosome) - self.network.output_size * self.network.hidden_size, self.network.hidden_size)]
        child.network.weights_hidden_output = [child_chromosome[i:i + self.network.output_size] for i in range(len(child_chromosome) - self.network.output_size * self.network.hidden_size, len(child_chromosome), self.network.output_size)]
        return child
    
    def mutate(self, mutation_rate):
        MUTATE_WEIGHT = 0.1
        for i in range(len(self.network.weights_input_hidden)):
            for j in range(len(self.network.weights_input_hidden[i])):
                if random.random() < mutation_rate:
                    self.network.weights_input_hidden[i][j] += random.uniform(-MUTATE_WEIGHT, MUTATE_WEIGHT)
        for i in range(len(self.network.weights_hidden_output)):
            for j in range(len(self.network.weights_hidden_output[i])):
                if random.random() < mutation_rate:
                    self.network.weights_hidden_output[i][j] += random.uniform(-MUTATE_WEIGHT, MUTATE_WEIGHT)