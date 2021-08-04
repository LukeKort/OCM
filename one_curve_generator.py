# Generates random data in specified shape - Lucas kort (Jun. 23, 2021)

import numpy as np
import pandas as pd
import random as rand
import math
import tkinter as tk #hide tk window
from tkinter import filedialog #get a file dialog window

#Configuração dos dados de saída---------------------------------
record_size = 100 #tamanho de cada vetor de dados
theta = 1034.950359   #log(theta)
gamma = 2.499768972     #inicialização de parâmetro gamma (Gamma mínimo)
#----------------------------------------------------------------

#função de densidade weibull
def weibull(theta,gamma,x,x_size): 
    weibull_x = np.zeros(x_size)
    for i in range(x_size):
        weibull_x[i] = theta*(-math.log(x[i]))**(1/gamma)
    return weibull_x

#salvar em arquivo do excel
def export_xlsx(time_weibull,record_size):

    header = []

    for i in range(record_size): #cabeçalho para os tempos
        header.append('T' + str(i+1))

    df_time_weibull=pd.DataFrame(
        time_weibull, 
        index=header
    )

    root = tk.Tk()
    root.withdraw()
    export_file_path = filedialog.asksaveasfilename(defaultextension ='.xlsx') #local de salvamento + extensão .xlsx

    df_time_weibull.to_excel(export_file_path,sheet_name = 'Tempos Weibull')

#Inicialização de variáveis
time_weibull = np.zeros((record_size))
x = np.random.default_rng().uniform(0,1,record_size)

#geração automática de dados
time_weibull = np.sort(weibull(theta,gamma,x,record_size).copy())

#Exportar dados para arquivo do excel
export_xlsx(time_weibull,record_size)