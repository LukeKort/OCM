import tensorflow as tf
import math

def weibull_layer(x):
    """
    Lambda function for generating weibull parameters
    theta and gamma from a Dense(2) output.
    Assumes tensorflow 2 backend.
    
    Usage
    -----
    outputs = Dense(2)(final_layer)
    distribution_outputs = Lambda(weibull_layer)(outputs)
    
    Parameters
    ----------
    x : tf.Tensor
        output tensor of Dense layer
        
    Returns
    -------
    out_tensor : tf.Tensor
        
    """
    
    # Get the number of dimensions of the input
    num_dims = len(x.get_shape())
    
    # Separate the parameters
    theta, gamma = tf.unstack(x, num=2, axis=-1)
    
    # Add one dimension to make the right shape
    theta = tf.expand_dims(theta, -1)
    gamma = tf.expand_dims(gamma, -1)
        
    # Apply a softplus to make positive
    theta = tf.keras.activations.softplus(theta)
    gamma = tf.keras.activations.softplus(gamma)

    #print('theta',theta.get_shape(),'\ngama',gamma.get_shape()) #teste de qualidade apenas
 
    # Join back together again
    out_tensor = tf.concat((theta, gamma), axis=num_dims-1)

    return out_tensor

def weibull_loss(y_true, y_pred):
    """
    Negative log likelihood weibull loss function.
    Assumes tensorflow backend.
    
    Parameters
    ----------
    y_true : tf.Tensor
        Ground truth values of predicted variable.
    y_pred : tf.Tensor
        theta and gamma values of predicted distribution.
        
    Returns
    -------
    nll : tf.Tensor
        Negative log likelihood.
    """

    # Separate the parameters
    theta, gamma = tf.unstack(y_pred, num=2, axis=-1)
    
    # Add one dimension to make the right shape
    theta = tf.expand_dims(theta, -1)
    gamma = tf.expand_dims(gamma, -1)
    
    log_sum = 0
    t_gamma_sum = 0

    size = y_true.get_shape()[-1] #tamanho do vetor

    for i in range(size):
        log_sum += tf.math.log(y_true[i])
        t_gamma_sum += y_true**gamma

    # Calculate the negative log likelihood
    nll = (
        - tf.math.log(gamma) 
        + tf.math.log(theta)
        - (gamma - 1)*log_sum
        + (1/theta)*t_gamma_sum*tf.math.log(math.e)
    )

    return nll

from tensorflow.keras.layers import Input, Dense, Lambda
from tensorflow.keras.models import Model

# Define inputs with predefined shape
inputs = Input(shape=(5,))

# Build network with some predefined architecture
Layer1 = Dense(units=16)
Layer2 = Dense(units=16)

output1 = Layer1(inputs)
output2 = Layer2(output1)

# Predict the parameters of a negative binomial distribution
outputs = Dense(2)(output2)
distribution_outputs = Lambda(weibull_layer)(outputs)

# Construct model
model = Model(inputs=inputs, outputs=distribution_outputs)

from tensorflow.keras.optimizers import Adam

opt = Adam()
model.compile(loss = weibull_loss, optimizer = opt)

import pandas as pd
import numpy as np

time = pd.read_excel(
    'data.xlsx',
    sheet_name= 'Tempos',
    index_col='Index',
) #import data from xlsx file
header = []
vector_n,vector_size = time.shape #tamanho da última dimensão

for i in range(vector_size): #cabeçalho para os tempos
        header.append('T' + str(i+1))

f_t = pd.read_excel(
    'data.xlsx',
    sheet_name= 'Dados simulados',
    index_col='Index',
) #import data from xlsx file

train_x = time.loc[range(vector_n),header].values.tolist()
train_y = f_t.loc[range(vector_n),range(vector_size)].values.tolist()

history = model.fit(train_x, train_y, epochs = 10000) # validation_data = [val_X, val_Y])

test_t = train_x = time.loc[range(590,vector_n),header].values.tolist()

pred_params = model.predict(test_t)

print(pred_params)