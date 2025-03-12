class neuron():
    def __init__(self) -> None:
        self.input1 = -1
        self.input2 = -1
        self.input3 = -1

        self.weightN1 = 0.5
        self.weightN2 = 0.2
        self.weightN3 = 0.82

        self.bias = 1.2

    def updateInputs(self,inputs):
        self.input1 = inputs[0]
        self.input2 = inputs[1]
        self.input3 = inputs[2]

    def createOutput(self):
        outscore = (self.input1*self.weightN1 + self.input2*self.weightN2 + self.input3*self.weightN3)*self.bias
        return outscore

inputs = [1,0.5,0.8]
neuron1 = neuron()
neuron1.updateInputs(inputs)
print(neuron1.createOutput())
