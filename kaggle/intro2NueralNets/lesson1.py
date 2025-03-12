#A sequential Neural network -> one neuron with multiple inputs and weights
from tensorflow import keras
from keras import layers

model = keras.Sequential([
    layers.Dense(units=1,input_shape = [3]),
    #units is how many outputs we want, input shape is the number of inputs that we want

    #for every layer you want in the neural network just add another layer.Dense and define the shape

    #ie

    """ 
    layers.Dense(units=3,activation='relu',input_shape=[3])
    layers.Dense(units=3,activation='relu')
    layers.Dense(units=1)
    
    This creates a neural network with 3 layers (3:3:1)(3 inputs and 1 output)
    last layer doesnt have an activation function so would be appropriate for regression
    if it did have an activation function it could do other tasks like classification

    activation func needed so that it can fit non-linear relationships

    """
])

