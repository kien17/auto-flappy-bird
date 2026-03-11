import random
import numpy as np
import cupy as cp

class NeuronNetwork:
    def __init__(self, input_size, hidden_size, output_size=2):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weights_input_hidden = [[random.uniform(-1, 1) for _ in range(hidden_size)] for _ in range(input_size)]
        self.weights_hidden_output = [[random.uniform(-1, 1) for _ in range(output_size)] for _ in range(hidden_size)]

    def sigmoid(self, x):
        # Giới hạn x để tránh lỗi Overflow như lúc nãy
        x = np.clip(x, -500, 500) 
        return 1 / (1 + np.exp(-x))

    def feedforward(self, inputs):
        # Mọi thứ diễn ra trên CPU, không tốn thời gian chuyển dữ liệu sang GPU
        inputs_np = np.array(inputs)
        weights_ih_np = np.array(self.weights_input_hidden)
        weights_ho_np = np.array(self.weights_hidden_output)

        z1 = np.dot(inputs_np, weights_ih_np)
        hidden_layer = self.sigmoid(z1)
        
        z2 = np.dot(hidden_layer, weights_ho_np)
        output_layer = self.sigmoid(z2)

        return output_layer.tolist()

    def chromosome(self):
        return [self.weights_input_hidden[i][j] for i in range(self.input_size) for j in range(self.hidden_size)] + \
               [self.weights_hidden_output[i][j] for i in range(self.hidden_size) for j in range(self.output_size)]