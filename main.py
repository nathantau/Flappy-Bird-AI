import pygame
import numpy as np
from random import randint
from bird import Bird
from block import Block

def create_bird_population(population_size):
    birds = []
    for _ in range(population_size):
        birds.append(Bird(randint(0,500),250,0,50,50))
    return birds

pygame.init()
window = pygame.display.set_mode((500,500))
pygame.display.set_caption("Flappy Bird AI")

birds = create_bird_population(20)
upper_block = Block(0,0,500,50)
lower_block = Block(0,450,500,50)

start = False
run = True
while run:

    if start == False:
        pygame.time.delay(500)
        start = True
    else:
        pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if event.key == pygame.K_SPACE:
                #bird.flap()
                pass

    pygame.draw.rect(window,(0,0,0),(0,0,500,500))

    for bird in birds:

        upper_dist = bird.y_pos - (upper_block.y_pos + upper_block.height)

        lower_dist = lower_block.y_pos - (bird.y_pos + bird.height)

        input = np.array([upper_dist,lower_dist,bird.y_vel]).reshape((-1,3))
        bird.think(input)
        bird.fly()
        if bird.y_pos <= upper_block.y_pos + upper_block.height:
            birds.remove(bird)
        elif bird.y_pos + bird.height >= lower_block.y_pos:
            birds.remove(bird)

        pygame.draw.rect(window,(255,0,0),(bird.x_pos,bird.y_pos,bird.width,bird.height))

    pygame.draw.rect(window,(255,255,255),(upper_block.x_pos,upper_block.y_pos,upper_block.width,upper_block.height))
    pygame.draw.rect(window,(255,255,255),(lower_block.x_pos,lower_block.y_pos,lower_block.width,lower_block.height))

    pygame.display.update()

pygame.quit()
