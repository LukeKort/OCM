# Generates random data in specified shape - Lucas kort (Jun. 23, 2021)

import numpy as np
import pandas as pd
import random as rand
import math
import tkinter as tk #hide tk window
from tkinter import filedialog #get a file dialog window

#Configuração dos dados de saída---------------------------------
record_size = 5 #tamanho de cada vetor de dados
record_total_n = 1000 #número de vetores por dataset
a = 1   #limite inferior de intervalo log(theta)
b = 3.5 #limite superior de intervalo log(theta)
gamma = 0.5   #inicialização de parâmetro gamma (Gamma mínimo)
gamma_plus = 0.5 #incremento de gamma
gamma_each = 150 #incrementar gamma a cada x conjunto de dados
#----------------------------------------------------------------

#função de densidade weibull
def weibull(theta,gamma,x,x_size): 
    weibull_x = np.zeros(x_size)
    for i in range(x_size):
        weibull_x[i] = theta*(-math.log(x[i]))**(1/gamma)
    return weibull_x

#salvar em arquivo do excel
def export_xlsx(parameters,time_weibull,record_size,index_col):

    index = range(index_col) #Index na ordem crescente
    rand_index = np.random.permutation(index) #tornar a ordem do index aleatória
    #Primeiro aleatório, depois crescente, para planilha ficar na ordem crescente
    df_parameters=pd.DataFrame(
        parameters,
        index=rand_index,
        columns=['Theta','Log(Theta)','Gamma']
    )

    header = []

    for i in range(record_size): #cabeçalho para os tempos
        header.append('T' + str(i+1))

    df_time_weibull=pd.DataFrame(
        time_weibull,
        index=rand_index, 
        columns=header
    )

    new_index = np.random.permutation(index) #tornar a ordem dos dados aleatória

    root = tk.Tk()
    root.withdraw()
    export_file_path = filedialog.asksaveasfilename(defaultextension ='.xlsx') #local de salvamento + extensão .xlsx

    with pd.ExcelWriter(export_file_path) as writer: #escrever em mais de uma planilha ao mesmo tempo
        df_parameters.reindex(index).to_excel(writer,sheet_name = 'Parâmetros')
        df_time_weibull.reindex(index).to_excel(writer,sheet_name = 'Tempos Weibull')

#Inicialização de variáveis
parameters = np.zeros((record_total_n,3))
time_weibull = np.zeros((record_total_n,record_size))
x = np.random.default_rng().uniform(0,1,record_size)

#geração automática de dados Weibull
for i in range(record_total_n):
    log_theta = a+(b-a)*rand.random()
    theta = 10**log_theta
    if (i%gamma_each==0):
        gamma += gamma_plus
    time_weibull[i,:] = np.sort(weibull(theta,gamma,x,record_size).copy())
    parameters[i,:] = [theta,log_theta,gamma]

#Exportar dados para arquivo do excel
export_xlsx(parameters,time_weibull,record_size,record_total_n)