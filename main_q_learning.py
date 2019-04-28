import pygame
import numpy as np
from random import randint,randrange,uniform
from bird import Bird
from bird import NeuralNetwork
from block import Block

def play_training_games(num_games):

	pygame.init()
	pygame.font.init()
	myfont = pygame.font.SysFont('Comic Sans MS', 20)
	window = pygame.display.set_mode((500,500))
	pygame.display.set_caption("Flappy Bird AI")
	bird = Bird()
	bird.neural_network = None

	for _ in range(num_games):

		pygame.time.delay(100)

		# Resetting env
		GAP = 200
		upper_block = Block(0,0,500,50)
		lower_block = Block(0,450,500,50)
		upper_pipe = Block(475,50,25,randrange(0,400 - GAP))
		lower_pipe = Block(475,upper_pipe.y_pos + upper_pipe.height + GAP,25,400 - upper_pipe.height - GAP)
		score_incremented = False		
		reward = 0

		# Resetting bird
		bird.x_pos = 200
		bird.y_pos = 250
		bird.y_vel = 0
		bird.score = 0

		done = False

		while not done:

			pygame.time.delay(50)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
				if event.type == pygame.KEYDOWN:
					keys = pygame.key.get_pressed()
					if event.key == pygame.K_SPACE:
						bird.y_vel -= 10
						pass

			# Creating background
			pygame.draw.rect(window,(0,0,0),(0,0,500,500))

			# Writing score
			textsurface = myfont.render(f'Score: {bird.score}', False, (255, 255, 255))
			window.blit(textsurface,(250,250))

			# Getting training data
			upper_dist = bird.y_pos - (upper_block.y_pos + upper_block.height)
			lower_dist = lower_block.y_pos - (bird.y_pos + bird.height)
			bird_y_vel = bird.y_vel
			x_pipe_dist = 0
			if upper_pipe.x_pos + upper_pipe.width > bird.x_pos:
				x_pipe_dist = upper_pipe.x_pos + upper_pipe.width - bird.x_pos
			y_upper_pipe_dist = abs(upper_pipe.y_pos + upper_pipe.height - bird.y_pos)
			y_lower_pipe_dist = abs(bird.y_pos - lower_pipe.y_pos)

			#input = np.array([upper_dist,lower_dist,bird_y_vel,x_pipe_dist,y_upper_pipe_dist,y_lower_pipe_dist]).reshape((-1,6))
			#bird.think(input)
			random = randint(0,1)
			if random is 1:
				bird.flap()

			bird.fly()

			reward = 0

			# Collision detection
			if bird.y_pos <= upper_block.y_pos + upper_block.height:		
				reward -= 1
				done = True	
			elif bird.y_pos + bird.height >= lower_block.y_pos:
				reward -= 1			
				done = True
			elif bird.x_pos + bird.width >= upper_pipe.x_pos and bird.x_pos <= upper_pipe.x_pos + upper_pipe.width:
				if bird.y_pos <= upper_pipe.y_pos + upper_pipe.height:
					reward -= 1
					done = True
				elif bird.y_pos + bird.height >= lower_pipe.y_pos:
					reward -= 1
					done = True  
			
			# Score incrementation when bird passes pipe
			if bird.x_pos >= upper_pipe.x_pos + upper_pipe.width and done is False and score_incremented is False:
				score_incremented = True
				reward += 1
			
			# Adding rewards to training_score
			bird.training_score += reward

			# Drawing bird
			pygame.draw.rect(window,(255,0,0),(bird.x_pos,bird.y_pos,bird.width,bird.height))     
			# Drawing block objects
			pygame.draw.rect(window,(255,255,255),(upper_pipe.x_pos,upper_pipe.y_pos,upper_pipe.width,upper_pipe.height))
			pygame.draw.rect(window,(255,255,255),(lower_pipe.x_pos,lower_pipe.y_pos,lower_pipe.width,lower_pipe.height))
			pygame.draw.rect(window,(255,255,255),(upper_block.x_pos,upper_block.y_pos,upper_block.width,upper_block.height))
			pygame.draw.rect(window,(255,255,255),(lower_block.x_pos,lower_block.y_pos,lower_block.width,lower_block.height))
			# Updating pygame display
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

				score_incremented = False

	pygame.quit()

play_training_games(5)