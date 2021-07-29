# Compares predict to real data - Lucas kort (Jun. 23, 2021)

import pandas as pd
import numpy as np
import tkinter as tk #hide tk window
from tkinter import filedialog #get a file dialog window
from function_repository import ml_setup, get_data, predict_val

file_name, test_file_name, file_path, training_ratio, epochs, batch_size, loss_function, lr_rate, opt = ml_setup() #obter configurações

train_x, train_y, val_x, val_y, test_x, test_y = get_data(test_file_name,training_ratio = 1) #obter dados

model_val = predict_val(train_x) #prever valores pelo modelo

vector_n = len(train_x) #tamanho do vetor de dados

error = np.zeros((vector_n,2)) #pre-allocation

for i in range(vector_n): #calcular o MAPE - Mean Absolute Porcentile Error
    for j in range(2):
        error[i,j] = 100*abs(model_val[i][j] - train_y[i][j])/train_y[i][j]

data_compared = np.zeros((vector_n,6))

data_compared[:,0],data_compared[:,1] = np.transpose(train_y)
data_compared[:,2],data_compared[:,3] = np.transpose(model_val)
data_compared[:,4],data_compared[:,5] =np.transpose(error)

df_result_compare = pd.DataFrame(
        data_compared,
        index=range(1,vector_n+1),
        columns=['Log(Theta) real', 'Gamma real', 'Log(Theta) Modelo', 'Gamma Modelo','APE Log(Theta)', 'APE Gamma']
    )

root = tk.Tk()
root.withdraw()
export_file_path = filedialog.asksaveasfilename(defaultextension ='.xlsx') #local de salvamento + extensão .xlsx

df_result_compare.to_excel(export_file_path,sheet_name = 'Resultados comparados')