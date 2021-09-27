# Generates random data in specified shape - Lucas kort (Jun. 23, 2021)

import numpy as np
import pandas as pd
import random as rand
import tkinter as tk #hide tk window
from tkinter import filedialog #get a file dialog window

#Configuração dos dados de saída---------------------------------
record_size = 5 #tamanho de cada vetor de dados
record_total_n = 1000 #número de vetores por dataset
mu_a = 3   #limite inferior de intervalo log(theta)
mu_b = 8 #limite superior de intervalo log(theta)
sigma_a = 0.03 #incremento de sigma
sigma_b = 0.5 #incrementar sigma a cada x conjunto de dados
#----------------------------------------------------------------

#salvar em arquivo do excel
def export_xlsx(parameters,time_weibull,record_size,index_col):

    index = range(index_col) #Index na ordem crescente
    rand_index = np.random.permutation(index) #tornar a ordem do index aleatória
    #Primeiro aleatório, depois crescente, para planilha ficar na ordem crescente
    df_parameters=pd.DataFrame(
        parameters,
        index=rand_index,
        columns=['Mu','Sigma']
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
        df_time_weibull.reindex(index).to_excel(writer,sheet_name = 'Tempos Lognormal')

#Inicialização de variáveis
parameters = np.zeros((record_total_n,2))
time_weibull = np.zeros((record_total_n,record_size))
x = np.random.default_rng().uniform(0,1,record_size)

#geração automática de dados Weibull
for i in range(record_total_n):
    mu = mu_a+(mu_b-mu_a)*rand.random()
    sigma = sigma_a+(sigma_b-sigma_a)*rand.random()
    time_weibull[i,:] = np.sort(np.random.lognormal(mu,sigma,record_size))
    parameters[i,:] = [mu,sigma]

#Exportar dados para arquivo do excel
export_xlsx(parameters,time_weibull,record_size,record_total_n)