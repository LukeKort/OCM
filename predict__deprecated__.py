import tensorflow as tf
from function_repository import model_creator, training_data

def predict_val():
    
    #Carregar parâmetros
    file_name, file_path, training_ratio, epochs, batch_size, loss_function, lr_rate, opt = ml_setup()

    #Obter dados
    train_x, train_y, val_x, val_y, test_x, test_y = training_data(file_name,training_ratio)

    #Criar modelo
    model = model_creator(loss_function,opt)
        
    #Restaurar último treinamento
    checkpoint = tf.train.Checkpoint(model)
    checkpoint.restore(file_path).expect_partial()

    #Prever resultados
    pred_params = model.predict(test_x)

    return pred_params