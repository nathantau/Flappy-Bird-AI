import pygame
import numpy as np
from random import randint,randrange
from bird import Bird
from block import Block

def create_bird_population(population_size):
    birds = []
    for _ in range(population_size):
        birds.append(Bird(randint(0,500),250,0,10,10))
    return birds

pygame.init()
window = pygame.display.set_mode((500,500))
pygame.display.set_caption("Flappy Bird AI")

GAP = 100
birds = create_bird_population(20)
upper_block = Block(0,0,500,50)
lower_block = Block(0,450,500,50)
upper_pipe = Block(475,50,25,randrange(0,400 - GAP))
lower_pipe = Block(475,upper_pipe.y_pos + upper_pipe.height + GAP,25,400 - upper_pipe.height - GAP)

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
        bird_y_vel = bird.y_vel
        x_pipe_dist = 0
        if upper_pipe.x_pos + upper_pipe.width > bird.x_pos:
            x_pipe_dist = upper_pipe.x_pos + upper_pipe.width - bird.x_pos
        y_upper_pipe_dist = abs(upper_pipe.y_pos + upper_pipe.height - bird.y_pos)
        y_lower_pipe_dist = abs(bird.y_pos - lower_pipe.y_pos)

        input = np.array([upper_dist,lower_dist,bird_y_vel,x_pipe_dist,y_upper_pipe_dist,y_lower_pipe_dist]).reshape((-1,6))
        bird.think(input)
        bird.fly()

        # Collision detection
        if bird.y_pos <= upper_block.y_pos + upper_block.height:
            birds.remove(bird)
        elif bird.y_pos + bird.height >= lower_block.y_pos:
            birds.remove(bird)
        elif bird.x_pos + bird.width >= upper_pipe.x_pos and bird.x_pos <= upper_pipe.x_pos + upper_pipe.width:
            if bird.y_pos <= upper_pipe.y_pos + upper_pipe.height:
                birds.remove(bird)
            elif bird.y_pos + bird.height >= lower_pipe.y_pos:
                birds.remove(bird)       

        pygame.draw.rect(window,(255,0,0),(bird.x_pos,bird.y_pos,bird.width,bird.height))


    pygame.draw.rect(window,(255,255,255),(upper_pipe.x_pos,upper_pipe.y_pos,upper_pipe.width,upper_pipe.height))
    pygame.draw.rect(window,(255,255,255),(lower_pipe.x_pos,lower_pipe.y_pos,lower_pipe.width,lower_pipe.height))
    pygame.draw.rect(window,(255,255,255),(upper_block.x_pos,upper_block.y_pos,upper_block.width,upper_block.height))
    pygame.draw.rect(window,(255,255,255),(lower_block.x_pos,lower_block.y_pos,lower_block.width,lower_block.height))

    pygame.display.update()

    upper_pipe.x_pos -= 8
    lower_pipe.x_pos -= 8

    if upper_pipe.x_pos + upper_pipe.width < 0:
        upper_pipe.x_pos = 500 + 25
        lower_pipe.x_pos = 500 + 25
        
        upper_pipe.height = randrange(0,400 - GAP)
        lower_pipe.y_pos = upper_pipe.y_pos + upper_pipe.height + GAP
        lower_pipe.height = 400 - upper_pipe.height - GAP


pygame.quit()
