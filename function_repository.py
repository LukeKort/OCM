# Functions need in other scripts - Lucas kort (Jun. 23, 2021)

from tkinter.constants import UNITS
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Input, Dense, Lambda
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import tkinter as tk #hide tk window
from tkinter import filedialog #get a file dialog window


def ml_setup():
    #Banco de dados - com extensão
    training_data_file_name = 'data/data_5_total.xlsx'
    file_path = 'treinamentos/set 5/Teste 31-5/Teste 31-5' #carregar treinamento salvo
    teste_data_file_name = 'data/data_5_5.xlsx' #Válido apenas para previsão

    #proporção dos dados para treinamento/dados de validação
    training_ratio = 0.8

    #número de epochs
    epochs = 10000

    #quantidade de dados por epoch         
    batch_size = 10

    #Função de erro - escolher
    #loss_function = tf.keras.losses.MeanSquaredError()
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

    return training_data_file_name, teste_data_file_name, file_path, training_ratio, epochs, batch_size, loss_function, lr_rate, opt

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
    gamma,theta = tf.unstack(x, num=2, axis=-1)
    
    # Add one dimension to make the right shape
    theta = tf.expand_dims(theta, -1)
    gamma = tf.expand_dims(gamma, -1)
        
    # Apply a softplus to make positive
    theta = tf.keras.activations.softplus(theta)
    gamma = tf.keras.activations.softplus(gamma)

    #print('theta',theta.get_shape(),'\ngama',gamma.get_shape()) #teste de qualidade apenas
 
    # Join back together again
    out_tensor = tf.concat((gamma,theta), axis=num_dims-1)

    return out_tensor

def model_creator(loss_function, opt):
    # Define inputs with predefined shape
    inputs = Input(shape=(5,))

    # Build network with some predefined architecture
    #Layer1 = Dense(units=20, activation = 'sigmoid')
    # Layer2 = Dense(units=20, activation = 'sigmoid')
    Layer3 = Dense(units=20, activation = 'sigmoid')

    #output1 = Layer1(inputs)
    # output2 = Layer2(output1)
    last_output = Layer3(inputs)

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

def plot_loss_val(history):    
    loss = history.history['loss']

    val_loss = history.history['val_loss']
    epochs = range(1, len(loss) + 1)

    plt.plot(epochs, loss, '-', label='Training loss')
    plt.plot(epochs, val_loss, '--', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.legend()
    plt.show()

def save_file(model):
    try:
        tk.Tk().withdraw()
        export_file_path = filedialog.asksaveasfilename() #local de salvamento sem extensão
        #Salvar modelo para reuso
        #model.save(export_file_path)
        model.save_weights(export_file_path)
    except:
        print('File not saved!')

def get_data(file_name,training_ratio):
    time = pd.read_excel(
        file_name,
        sheet_name= 'Tempos Weibull',
        index_col=0 #não tem nenhuma columa com nome para o index
    )

    parameters = pd.read_excel(
        file_name,
        sheet_name= 'Parâmetros',
        index_col=0 #não tem nenhuma columa com nome para o index
    )

    header = []
    vector_n,vector_size = time.shape #tamanho da última dimensão

    for i in range(vector_size): #cabeçalho para os tempos
            header.append('T' + str(i+1))

    # Divisão dos dados de acordo com a divisão

    lim_training = round(vector_n*training_ratio)

    train_x = time.loc[range(lim_training),header].values.tolist()
    train_y = parameters.loc[range(lim_training),['Log(Theta)','Gamma']].values.tolist()

    val_x = time.loc[range(lim_training,vector_n),header].values.tolist()
    val_y = parameters.loc[range(lim_training,vector_n),['Log(Theta)','Gamma']].values.tolist()

    # Sanity check de algumas amostras

    test_x = time.loc[range(vector_n-10,vector_n),header].values.tolist()
    test_y = parameters.loc[range(vector_n-10,vector_n),['Log(Theta)','Gamma']].values.tolist()
    
    return train_x, train_y, val_x, val_y, test_x, test_y

def results_check(pred_params,test_y):
    
    #vector_n,vector_size = test_y.shape #tamanho da última dimensão

    vector_n = len(test_y)

    MSE_test = 0
    for i in range(vector_n):
        MSE_test += (pred_params[i] - test_y[i])**2
    MSE_test = MSE_test/vector_n

    print('\n#Sanity check\n\n#MSE\n Theta|Gamma:\n', MSE_test,'\n\n#Valores pelo odelo\n Theta|Gamma:\n',pred_params,'\n\n#Valores reais\n Theta|Gamma:')
    for i in range(10):
        print(test_y[i])

def predict_val(test_x):
    
    #Carregar parâmetros
    file_name, test_file_name, file_path, training_ratio, epochs, batch_size, loss_function, lr_rate, opt = ml_setup()

    #Criar modelo
    model = model_creator(loss_function,opt)
        
    #Restaurar último treinamento
    checkpoint = tf.train.Checkpoint(model)
    checkpoint.restore(file_path).expect_partial()

    #Prever resultados
    pred_params = model.predict(test_x)

    return pred_params