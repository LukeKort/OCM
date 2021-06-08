#code by Kort (2021-06-08)

import numpy as np
import pandas as pd
import random as rand
import math
import tkinter as tk #hide tk window
from tkinter import filedialog #get a file dialog window

#função de densidade weibull
def weibull(theta,gamma,t): 
    f_t = (gamma/theta)*((t/theta)**(gamma-1))*math.exp(-(t/theta)**gamma)
    return f_t

#salvar em arquivo do excel
def export_xlsx(data,parameters,time,index_col):
    df_parameters=pd.DataFrame(parameters,index=range(index_col),columns=['Gamma','Theta'])
    df_simulated_data=pd.DataFrame(data,index=range(index_col))
    header = []
    for i in range(np.size(time[0])): #cabeçalho para os tempos
        header.append('T' + str(i+1))
    df_time=pd.DataFrame(time,index=range(index_col),columns=header)
    root = tk.Tk()
    root.withdraw()
    export_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')
    with pd.ExcelWriter(export_file_path) as writer: #escrever em mais de uma planilha ao mesmo tempo
        df_simulated_data.to_excel(writer,sheet_name='Dados simulados')
        df_parameters.to_excel(writer,sheet_name='Parâmetros')
        df_time.to_excel(writer,sheet_name='Tempos')
#---------------------------------------------------------------------------------------------------------------------------------------
#Configuração dos dados de saída
n_data_sets = 600 #número total de conjunto de dados
vector_length = 5   #tamanho de cada um dos conjuntos de dados
a = 1   #limite inferior de intervalo log(theta)
b = 3.5 #limite superior de intervalo log(theta)
gamma = 0.5   #inicialização de parâmetro gamma (Gamma mínimo)
gamma_plus = 0.5 #incremento de gamma
gamma_each = 100 #incrementar gamma a cada x conjunto de dados
#---------------------------------------------------------------------------------------------------------------------------------------

#Inicialização de variáveis
k = 1 #Contador
data_vector = t = np.zeros(vector_length)   #conjunto de dados / vetor de tempos - preallocation
simulated_data = time_var = np.zeros((n_data_sets,vector_length)).copy()  #conjunto de dados - preallocation
parameters = np.zeros((n_data_sets,2))

#geração automática de dados
for i in range(n_data_sets):
    log_theta = a+(b-a)*rand.random()
    theta = 10**log_theta
    if k==gamma_each:
        gamma += gamma_plus
        k=1
    k += 1
    for j in range(vector_length): #geração dos valores do vetor de dados
        time_var[i,j] = 0+(50-10)*rand.random()
        data_vector[j] = weibull(theta,gamma,time_var[i,j]) #chamando a função e adc ao vetor posição [j]
    time = time_var.copy() #Não sei porque
    simulated_data[i,:] = data_vector   #adc ao conjunto de dados na linha [i]
    parameters[i,:] = [gamma,theta]

#Exportar dados para arquivo do excel
export_xlsx(simulated_data,parameters,time,n_data_sets)