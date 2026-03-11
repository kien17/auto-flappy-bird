import pygame
from random import randint
from bird import Bird
from genetic_bot import GeneticBot
import random
import cupy as cp

NUMBER_OF_BOTS = 1000

class Tube:
    def __init__(self, x, gap):
        self.x = x
        self.gap = gap
        self.width = 50
        self.color = (0, 0, 255)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, 0, self.width, self.gap))
        pygame.draw.rect(screen, self.color, (self.x, self.gap + 150, self.width, 600 - (self.gap + 150)))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.background_file = "background.png"
        self.tubes = [Tube(600, 200), Tube(800, 250), Tube(1000, 150)]
        self.bots = [GeneticBot(5, 5) for _ in range(NUMBER_OF_BOTS)]
        self.birds = [Bird() for _ in range(NUMBER_OF_BOTS)]
        self.score = 0
        self.time_since_last_score = 0
        self.font = pygame.font.SysFont(None, 35)

    def run(self):
        self.update_gpu_weights()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((255, 255, 255))
            self.screen.blit(pygame.image.load(self.background_file), (0, 0))
            for tube in self.tubes:
                if tube.x <= -tube.width:
                    tube.x = 600
                    tube.gap = randint(100, 300)
                else:
                    tube.x -= 2
                tube.draw(self.screen)

            all_inputs = []
            for i in range(len(self.birds)):
                info = self.get_info(self.birds[i])
                all_inputs.append(info)

            X_gpu = cp.array(all_inputs).reshape(NUMBER_OF_BOTS, 1, -1)

            Z1 = cp.matmul(X_gpu, self.W1_gpu)
            A1 = 1 / (1 + cp.exp(-cp.clip(Z1, -500, 500))) 

            Z2 = cp.matmul(A1, self.W2_gpu)
            A2 = 1 / (1 + cp.exp(-cp.clip(Z2, -500, 500)))

            decisions = A2.reshape(NUMBER_OF_BOTS, -1).tolist()

            for i in range(len(self.birds)):
                if self.birds[i].y > 600 or self.check_lose(self.birds[i]):
                    continue # Chim chết rồi thì bỏ qua không update
                
                # Cập nhật điểm fitness cho chim còn sống
                self.bots[i].fitness += 1 
                
                if decisions[i][0] > 0.5: 
                    self.birds[i].flap()

                self.birds[i].update()
                self.birds[i].draw(self.screen)

            # Cross over and mutate bots
            # find top 10% bots to cross over and mutate

            if all(self.check_lose(bird) for bird in self.birds) and all(tube.x <= -tube.width for tube in self.tubes):
                new_bots = []
                fitness_scores = [bot.fitness for bot in self.bots]
                num_top_bots = max(1, int(0.1 * NUMBER_OF_BOTS))  # Find top 10% bots
                top_bots = sorted(zip(self.bots, fitness_scores), key=lambda x: x[1], reverse=True)[:num_top_bots]
                for _ in range(NUMBER_OF_BOTS):
                    parent1 = random.choices(top_bots, weights=[score for _, score in top_bots], k=1)[0][0]
                    parent2 = random.choices(top_bots, weights=[score for _, score in top_bots], k=1)[0][0]
                    child = parent1.crossover(parent2)
                    child.mutate()
                    new_bots.append(child)
  
            text_time = self.font.render(f"Time: {self.time_since_last_score // 60}", True, (0, 0, 0))
            self.screen.blit(text_time, (10, 10))
            self.time_since_last_score += 1
            pygame.display.flip()
            # self.clock.tick(60)

        pygame.quit()
    
    def check_lose(self, bird):
        for tube in self.tubes:
            if (bird.x + bird.width > tube.x and bird.x < tube.x + tube.width):
                if (bird.y < tube.gap or bird.y + bird.height > tube.gap + 150):
                    return True
        return False

    def get_info(self, bird):
        # Find the closest tube
        closest_tube = None
        for tube in self.tubes:
            if tube.x + tube.width > bird.x and (closest_tube is None or closest_tube.x > tube.x):
                closest_tube = tube
        
        if closest_tube is None:
            return [bird.y, bird.velocity, 0, 0, 1.0]

        # Return [bird's y position, bird's velocity, horizontal distance to the closest tube, vertical distance to the gap of the closest tube]
        return [bird.y, bird.velocity, closest_tube.x - bird.x, closest_tube.gap - bird.y, 1.0]
    
    def update_gpu_weights(self):
        # Lấy trọng số từ list của Python và nén thành 2 khối Tensor 3D trên GPU
        w1_list = [bot.network.weights_input_hidden for bot in self.bots]
        w2_list = [bot.network.weights_hidden_output for bot in self.bots]
        
        # Shape: (1000, 5, 5) - Giả sử 5 input, 5 hidden
        self.W1_gpu = cp.array(w1_list) 
        
        # Shape: (1000, 5, 2) - Giả sử 5 hidden, 2 output
        self.W2_gpu = cp.array(w2_list)