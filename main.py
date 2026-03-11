import pygame
from game import Game
from game_for_bot import Game as GameForBot

if __name__ == "__main__":
    # game = Game()
    game = GameForBot()
    game.run()