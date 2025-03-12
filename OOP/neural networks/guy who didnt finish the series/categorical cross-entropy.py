import numpy as np

softmax_ouput = np.array([[0.7,0.1,0.2],
                 [0.1,0.5,0.4],
                 [0.02,0.9,0.08]])


class_targets = [0,1,1]

loss = -np.log(softmax_ouput[
    range(len(softmax_ouput)),class_targets
])

print(loss)

avg_loss = np.mean(loss)
print(avg_loss)