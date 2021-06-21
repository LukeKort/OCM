from tensorflow.keras.optimizers import Adam
import tensorflow as tf
from function_repository import model_creator, training_data

training_ratio = 0.5
file_name = 'data_100_2.xlsx'
file_path = 'Teste 24.2'

train_x, train_y, val_x, val_y, test_x, test_y = training_data(file_name,training_ratio)

opt = Adam()
loss_function = tf.keras.losses.MeanSquaredError()
model = model_creator(loss_function,opt)
    
#Restaurar último treinamento
checkpoint = tf.train.Checkpoint(model)
checkpoint.restore(file_path).expect_partial()

pred_params = model.predict(test_x)

print(pred_params)