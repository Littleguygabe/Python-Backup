import numpy as np
import nnfs
from nnfs.datasets import spiral_data

nnfs.init()

np.random.seed(0)
#setup input values

class Layer_dense:
    def __init__(self,n_inputs,n_neurons) -> None:
        self.weights = 0.1*np.random.randn(n_inputs, n_neurons) #n_inputs by n_neurons
        self.biases = np.zeros((1,n_neurons))
        
    def forward(self,inputs):
        self.output = np.dot(inputs,self.weights)+self.biases
        
class activation_ReLU:
    def forward(self, inputs):
        self.output = np.maximum(0,inputs)
        
class activation_softmax:
    def forward(self,inputs):
        exp_values = np.exp(inputs-np.max(inputs, axis=1,keepdims=True))
        probabilities = exp_values/np.sum(exp_values,axis=1,keepdims=True)
        self.output = probabilities
    
class loss:
    def calculate(self,output,y):
        sample_losses = self.forward(output,y)
        data_loss = np.mean(sample_losses)
        return data_loss
    
class loss_categoricalCrossEntropy(loss):
    def forward(self,y_pred,y_True):
        samples = len(y_pred)
        y_pred_clipped = np.clip(y_pred,1e-7, 1-1e-7)
        
        #for scalar class values
        if len(y_True.shape) == 1:
            correct_confidences = y_pred_clipped[range(samples),y_True]
            
        # for one hot encoding
        elif len(y_True.shape) == 2:
            correct_confidences = np.sum(y_pred_clipped*y_True,axis=1)
            
        negative_log_likelihood = -np.log(correct_confidences)
        return negative_log_likelihood
        
        
    
X,y = spiral_data(samples=100,classes=3)
dense1 = Layer_dense(2,3)
activation1 = activation_ReLU()


dense2 = Layer_dense(3,3) #N inputs is same as N outputs of previous layer
activation2 = activation_softmax()

dense1.forward(X)
activation1.forward(dense1.output)

dense2.forward(activation1.output)
activation2.forward(dense2.output)

print(activation2.output[:5])

loss_function = loss_categoricalCrossEntropy()
loss = loss_function.calculate(activation2.output,y) #First param is the values the netowrk has created, the second is the expected output
print('loss: ',loss)