from tensorflow import keras
from random import randint

class NeuralNetwork():

    def __init__(self,input_size,output_size):
        self.model = keras.models.Sequential()
        # We will choose to have 6 features:
        # - distance from ceiling
        # - distance from ground
        # - current y-velocity
        # - x-distance from pipe
        # - y-distance from upper pipe
        # - y-distance from lower pipe
        self.model.add(keras.layers.Dense(128,input_dim=(input_size),activation='relu'))
        self.model.add(keras.layers.Dense(64,activation='relu'))
        # We will have one output
        self.model.add(keras.layers.Dense(output_size,activation='relu'))
        self.model.compile(loss='mean_squared_error',optimizer='Adam')

class Bird():
   
    def __init__(self,x_pos=200,y_pos=250,y_vel=0,width=10,height=10,model=None):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.y_vel = y_vel
        self.width = width
        self.height = height
        self.score = 0
        self.training_score = 0
        self.fitness = 0
        self.neural_network = NeuralNetwork(6,1)
        if model is not None:
            self.neural_network.model = model

    def think(self,input):
        # inputs is a numpy array with 3 parameters
        output = self.neural_network.model.predict(input)
        # if the output layer has a value greater than 0.5 we will flap the bird
        if output[0] > 0.5:
            self.flap()

    def flap(self):
        self.y_vel -= 1

    def fly(self):
        self.y_vel += 0.5
        self.y_pos += self.y_vel