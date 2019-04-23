from tensorflow import keras

class NeuralNetwork():

    def __init__(self):
        self.model = keras.models.Sequential()
        # We will choose to have 3 features:
        # - distance from ceiling
        # - distance from ground
        # - current y-velocity
        self.model.add(keras.layers.Dense(128,input_dim=(3),activation='relu',kernel_initializer='random_normal'))
        self.model.add(keras.layers.Dense(64,activation='relu',kernel_initializer='random_normal'))
        # We will have one output
        self.model.add(keras.layers.Dense(1,activation='relu'))

class Bird():

    def __init__(self,x_pos,y_pos,y_vel,width,height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.y_vel = y_vel
        self.width = width
        self.height = height
        self.neural_network = NeuralNetwork()

    def think(self,input):
        # inputs is a numpy array with 3 parameters
        output = self.neural_network.model.predict(input)
        # if the output layer has a value greater than 0.5 we will flap the bird
        print(output)
        if output[0] > 0.5:
            self.flap()

    def flap(self):
        self.y_vel -= 1

    def fly(self):
        self.y_vel += 0.5
        self.y_pos += self.y_vel