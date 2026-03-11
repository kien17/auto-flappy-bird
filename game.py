import pygame
from random import randint
from bird import Bird

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
        self.bird = Bird()
        self.lose = False
        self.score = 0
        self.time_since_last_score = 0
        self.font = pygame.font.SysFont(None, 35)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not self.lose:
                            self.bird.flap()
                        else:
                            self.__init__()

            if self.lose:
                self.screen.fill((255, 255, 255))
                text = self.font.render("Game Over", True, (255, 0, 0))
                self.screen.blit(text, (100, 250))
                pygame.display.flip()
                continue

            self.screen.fill((255, 255, 255))
            self.screen.blit(pygame.image.load(self.background_file), (0, 0))
            for tube in self.tubes:
                if tube.x <= -tube.width:
                    tube.x = 600
                    tube.gap = randint(100, 300)
                else:
                    tube.x -= 2
                tube.draw(self.screen)
            self.bird.update()
            self.bird.draw(self.screen)

            text_score = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
            self.screen.blit(text_score, (10, 10))   
            text_time = self.font.render(f"Time: {self.time_since_last_score // 60}", True, (0, 0, 0))
            self.screen.blit(text_time, (10, 50))
            self.time_since_last_score += 1
            for tube in self.tubes:
                if (self.bird.x + self.bird.width > tube.x and self.bird.x < tube.x + tube.width):
                    if (self.bird.y < tube.gap or self.bird.y + self.bird.height > tube.gap + 150):
                        self.lose = True
                elif tube.x + tube.width < self.bird.x and not hasattr(tube, 'passed'):
                    self.score += 1
                    setattr(tube, 'passed', True)
                elif tube.x + tube.width >= self.bird.x:
                    if hasattr(tube, 'passed'):
                        delattr(tube, 'passed')
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
    
    def get_info(self):
        tube_info = []
        for tube in self.tubes:
            tube_info.append((tube.x, tube.gap))
        return (self.bird.y, tube_info)