import tensorflow as tf

def nll_weibull(y_true, y_pred):
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

    
    
    # Add one dimension to make the right shape
    theta = tf.expand_dims(theta, -1)
    gamma = tf.expand_dims(gamma, -1)

    # Calcular o Log negativo da função de likelihood
    nll = (
        - tf.math.log(gamma) 
        + tf.math.log(theta)
        - (gamma - 1)*(tf.math.log(y_true) - tf.math.log(theta))
        + ((y_true/theta)**gamma)*tf.math.log(math.e)
    )
    return nll

        
