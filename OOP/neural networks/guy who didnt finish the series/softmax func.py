import math
import numpy as np
import nnfs
nnfs.init()

layer_ouptuts = [[4.8, 1.21, 2.385],
                 [8.9,-1.81,0.2],
                 [1.41,1.051,0.026]]
E = math.e
exp_values = np.exp(layer_ouptuts)
print(exp_values)

norm_values = exp_values / np.sum(exp_values, axis = 1,keepdims=True)

print(norm_values)