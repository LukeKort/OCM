# Randon matrix generator (May. 12, 2021)

import random as rand
import numpy as np

def radom_generator(x,y,a,b): #generates a x for y vector between the limits a and b with real values
    vector = np.zeros((x,y),dtype=float)
    for i in range(x):
        for j in range(y):
            vector[i,j] = a[i]+(b[i]-a[i])*rand.random()
    return vector