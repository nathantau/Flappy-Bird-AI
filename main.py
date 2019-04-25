import pygame
import numpy as np
from random import randint,randrange,uniform
from bird import Bird
from bird import NeuralNetwork
from block import Block

def create_bird_population(population_size):
    birds = []
    for _ in range(population_size):
        birds.append(Bird(200,250,0,10,10))
    return birds

def pick_one():
    index = 0
    random = uniform(0,1)
    global saved_birds

    while random > 0:
        random = random - saved_birds[index].fitness
        index += 1
        #print(index)

    index -= 1
    bird = saved_birds[index]
    child_model = bird.neural_network.model

    return child_model

def calculate_fitness():
    global saved_birds    
    sum = 0
    for bird in saved_birds:
        sum += bird.score
    for bird in saved_birds:
        bird.fitness = bird.score / sum
       # bird.fitness = bird.fitness**4

def mutate(model):
    for layer in model.layers:
        random = uniform(0,1)
        if random > 0.75:
            pass

def next_generation(population_size):
    global saved_birds
    global birds
    calculate_fitness()
    new_birds = saved_birds

    for new_bird in new_birds:
        bird_model = pick_one() 
        new_bird.neural_network.model.set_weights(bird_model.get_weights())
        new_bird.y_pos = randint(50,450)

    birds = []
    saved_birds = []

    return new_birds

pygame.init()
window = pygame.display.set_mode((500,500))
pygame.display.set_caption("Flappy Bird AI")

GAP = 200
POP_SIZE = 100
birds = create_bird_population(POP_SIZE)
saved_birds = []
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
            saved_birds.append(bird)
            birds.remove(bird)
        elif bird.y_pos + bird.height >= lower_block.y_pos:
            saved_birds.append(bird)
            birds.remove(bird)
        elif bird.x_pos + bird.width >= upper_pipe.x_pos and bird.x_pos <= upper_pipe.x_pos + upper_pipe.width:
            if bird.y_pos <= upper_pipe.y_pos + upper_pipe.height:
                saved_birds.append(bird)
                birds.remove(bird)
            elif bird.y_pos + bird.height >= lower_pipe.y_pos:
                saved_birds.append(bird)
                birds.remove(bird)       
        
        if bird is not None:
            pygame.draw.rect(window,(255,0,0),(bird.x_pos,bird.y_pos,bird.width,bird.height))
            # Increasing score of bird
            bird.score += 1            

    # Drawing block objects
    pygame.draw.rect(window,(255,255,255),(upper_pipe.x_pos,upper_pipe.y_pos,upper_pipe.width,upper_pipe.height))
    pygame.draw.rect(window,(255,255,255),(lower_pipe.x_pos,lower_pipe.y_pos,lower_pipe.width,lower_pipe.height))
    pygame.draw.rect(window,(255,255,255),(upper_block.x_pos,upper_block.y_pos,upper_block.width,upper_block.height))
    pygame.draw.rect(window,(255,255,255),(lower_block.x_pos,lower_block.y_pos,lower_block.width,lower_block.height))

    #if len(birds) <= 10:
    pygame.display.update()

    # Velocity of pipes
    upper_pipe.x_pos -= 8
    lower_pipe.x_pos -= 8

    # Reloading pipes each time they are passed
    if upper_pipe.x_pos + upper_pipe.width < 0:
        upper_pipe.x_pos = 500 + 25
        lower_pipe.x_pos = 500 + 25
        
        upper_pipe.height = randrange(0,400 - GAP)
        lower_pipe.y_pos = upper_pipe.y_pos + upper_pipe.height + GAP
        lower_pipe.height = 400 - upper_pipe.height - GAP

    if len(birds) == 0:
        print('Next generation!')
        # respawn birds
        # temporary
        #POP_SIZE = int(POP_SIZE/2)
        birds = next_generation(POP_SIZE)
        print(len(birds))

        # Reset pipe positions
        upper_pipe.x_pos = 500 + 25
        lower_pipe.x_pos = 500 + 25        
        upper_pipe.height = randrange(0,400 - GAP)
        lower_pipe.y_pos = upper_pipe.y_pos + upper_pipe.height + GAP
        lower_pipe.height = 400 - upper_pipe.height - GAP

    # If the number of birds is 0, we will respawn them
    #birds = next_generation(20)

pygame.quit()
