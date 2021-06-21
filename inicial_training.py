import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Lambda
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam


#Configuração da rede--------------------------------------------
#Banco de dados - com extensão
file_name = 'data_5_1.xlsx'

#proporção dos dados para treinamento/dados de validação
training_ratio = 0.5

#número de epochs
epochs = 50000

#quantidade de dados por epoch         
batch_size = 10

#Função de erro - escolher
loss_function = tf.keras.losses.MeanSquaredError()

#taxa de aprendizado - dinâmica
lr_rate = tf.keras.optimizers.schedules.InverseTimeDecay( #taxa de aprendizado - dinâmica
    #initial_learning_rate / (1 + decay_rate * step / decay_step)
    initial_learning_rate=1e-4,
    decay_steps=10000,
    decay_rate=1
) 

opt = Adam(learning_rate = lr_rate) #otimizador
#----------------------------------------------------------------
from function_repository import weibull_layer, model_creator, plot_loss_val, save_file, training_data, sanity_check

# Treinamento do modelo
model = model_creator(loss_function,opt)

train_x, train_y, val_x, val_y, test_x, test_y = training_data(file_name,training_ratio)

history = model.fit(train_x, train_y, batch_size = batch_size, epochs = epochs) #, validation_data = (val_x, val_y))

pred_params = model.predict(test_x)

sanity_check(pred_params,test_x,test_y)

plot_loss_val(history)

save_file(model)