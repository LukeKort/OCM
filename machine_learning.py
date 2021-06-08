import tensorflow as tf

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
    gamma = tf.expand_dims(theta, -1)
        
    # Apply a softplus to make positive
    theta = tf.keras.activations.softplus(theta)
    gamma = tf.keras.activations.sigmoid(gamma)
 
    # Join back together again
    out_tensor = tf.concat((theta, gamma), axis=num_dims-1)

    return out_tensor

def negative_weibull_loss(y_true, y_pred):
    """
    Negative binomial loss function.
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
    
    # Calculate the negative log likelihood
    nll = (
        tf.math.lgamma(theta) 
        + tf.math.lgamma(y_true + 1)
        - tf.math.lgamma(theta + y_true)
        - theta * tf.math.log(gamma)
        - y_true * tf.math.log(1 - gamma)
    )                  

    return nll

from tensorflow.keras.layers import Input, Dense, Lambda
from tensorflow.keras.models import Model

# Define inputs with predefined shape
inputs = Input(shape=input_shape)

# Build network with some predefined architecture
output1 = Layer1(inputs)
output2 = Layer2(output1)

# Predict the parameters of a negative binomial distribution
outputs = Dense(2)(output2)
distribution_outputs = Lambda(weibull_layer)(outputs)

# Construct model
model = Model(inputs=inputs, outputs=distribution_outputs)

from tensorflow.keras.optimizers import Adam

opt = Adam()
model.compile(loss = negative_weibull_loss, optimizer = opt)

history = model.fit(train_X, train_Y, epochs = num_epochs, validation_data = [val_X, val_Y])