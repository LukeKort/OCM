# Resumes training from selected previously saved weights - Lucas kort (Jun. 23, 2021)

import tensorflow as tf
from function_repository import model_creator, plot_loss_val, save_file, get_data, results_check, ml_setup

#Carregar parâmetros
file_name, test_file_name, file_path, training_ratio, epochs, batch_size, loss_function, lr_rate, opt = ml_setup()

#Criar modelo
model = model_creator(loss_function,opt)

#Obter dados
train_x, train_y, val_x, val_y, test_x, test_y = get_data(file_name,training_ratio)

#Restaurar último treinamento
checkpoint = tf.train.Checkpoint(model)

checkpoint.restore(file_path).expect_partial()

# Treinamento do modelo
history = model.fit(train_x, train_y, batch_size = batch_size, epochs = epochs, validation_data = (val_x, val_y))

#Prever resultados
pred_params = model.predict(test_x)

#Teste de sanidade
results_check(pred_params,test_y)

#Plotar loss e val
plot_loss_val(history)

#Salvar treinamento
save_file(model)