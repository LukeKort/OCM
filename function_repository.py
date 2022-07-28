# Functions need in other scripts - Lucas kort (Jun. 23, 2021)

import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Lambda
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import keras.engine


def ml_setup():
    #Banco de dados - com extensão
    file_path = 'rede/Teste 38' #carregar treinamento salvo

    #Função de erro - escolher
    
    loss_function = tf.keras.losses.MeanAbsolutePercentageError()
    

    #taxa de aprendizado - dinâmica
    lr_rate = tf.keras.optimizers.schedules.InverseTimeDecay( #taxa de aprendizado - dinâmica
        #initial_learning_rate / (1 + decay_rate * step / decay_step)
        initial_learning_rate=1e-3,
        decay_steps=100000,
        decay_rate=0.01
    ) 

    opt = Adam(
        learning_rate = lr_rate,
        amsgrad = True) #otimizador

    return file_path, loss_function,opt


def model_creator(loss_function, opt):
    # Define inputs with predefined shape
    inputs = Input(shape=(5,))

    # Build network with some predefined architecture
    Layer1 = Dense(units=20, activation = 'sigmoid')
    Layer2 = Dense(units=20, activation = 'sigmoid')
    
    output1 = Layer1(inputs)
    #output2 = Layer2(output1)
    last_output = Layer2(output1)

    # Predict the parameters of a negative binomial distribution
    outputs = Dense(2)(last_output)
    #distribution_outputs = Lambda(weibull_layer)(outputs)

    # Construct model

    model = Model(
        inputs=inputs, 
        outputs=outputs
    )

    model.compile(
        loss = loss_function, 
        optimizer = opt
    )
    return model

def predict_val(test_x):
    
    #Carregar parâmetros
    file_path, loss_function, opt = ml_setup()

    #Criar modelo
    model = model_creator(loss_function,opt)
        
    #Restaurar último treinamento
    checkpoint = tf.train.Checkpoint(model)
    checkpoint.restore(file_path).expect_partial()

    #Prever resultados
    pred_params = model.predict(test_x)

    return pred_params