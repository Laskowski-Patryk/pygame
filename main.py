import pickle

import pygame
from paddle import Paddle
from player import Player
from loot import Loot
import time
import neat
import os
import numpy as np


def main(genomes, config):
    window_height = 800
    window_width = 1000
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('My_game')
    pygame.display.flip()
    clock = pygame.time.Clock()
    done = False
    frame_cap = 1.0 / 1600000
    time_1 = time.perf_counter()
    unprocessed = 0
    balls = []
    blocks = []
    points = 0
    startgame = 0
    pygame.font.init()
    i = 0
    nets = []
    ge = []
    players = []
    my_font = pygame.font.SysFont('Comic Sans MS', 30)

    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        ge.append(genome)
        players.append(Player(screen))

    while not done:
        screen.fill((255, 255, 12))

        startgame = 1
        for n, player in enumerate(players):
            player.fillblocks()
            ball_cord = 0
            firstloot = np.array([0, 0])
            for loot in player.loot:
                if firstloot[0] == 0:
                    firstloot[0] = loot.x
                    firstloot[1] = loot.y
                p = loot.draw()
                if p == 0:
                    ge[n].fitness -= 10
            if firstloot[0] != 0:
                ball_cord = np.array([player.balls[0].xy[0], player.balls[0].xy[1]])
                ball_cord = np.linalg.norm(firstloot - ball_cord)
            for block in player.blocks:
                block.draw()
            if len(players) == 1:
                text_surface = my_font.render('Points: ' + str(player.points), False, (0, 0, 0))
                screen.blit(text_surface, (20, window_height - 50))
            output = nets[n].activate(
                (player.padd.x, player.balls[0].xy[0], player.balls[0].xy[1], ball_cord))
            if output[0] >= 0:
                pkt = player.padd.move(4)
                if pkt != 0:
                    player.points += pkt
                    ge[n].fitness += pkt
            elif output[0] < 0:
                pkt = player.padd.move(-4)
                if pkt != 0:
                    player.points += pkt
                    ge[n].fitness += pkt

            ge[n].fitness -= 0.001
            player.padd.redraw()
            for ball in player.balls:
                pkt = ball.redraw(startgame, player.blocks)
                if pkt == 1:
                    player.points += 1
                    ge[n].fitness += 1
                if ball.checkLose() == 1:
                    ge[n].fitness -= 30
                    nets.pop(n)
                    ge.pop(n)
                    players.remove(player)
            if len(players) == 0:
                done = True
                break

            if player.points >= 1000:
                done = True
                break
        # pygame.image.save(screen, "./screens/screenshot" + str(i) + ".jpg")
        # i += 1
        # startgame = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.display.flip()


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)

    print('\nBest genome:\n{!s}'.format(winner))
    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)
        f.close()


def replay_genome(config_path, genome_path="winner.pkl"):
    # Load requried NEAT config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    # Unpickle saved winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    # Convert loaded genome into required data structure
    genomes = [(1, genome)]

    # Call game with only the loaded genome
    main(genomes, config)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
    # replay_genome(config_path)
