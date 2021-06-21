import math
import numpy as np
import pandas as pd
import tkinter as tk #hide tk window
from tkinter import filedialog #get a file dialog window

# y_true = [27.12452461,	28.45456999,	18.02816841,	33.0956017,	9.24779012]
# gamma = 6.74797833e-01
# theta = 5.26510166e-06
# f_t = np.zeros(5)
# total = 1
# for i in range(5):
#     f_t[i] = (gamma/theta)*(y_true[i]**(gamma-1))*math.exp(-((y_true[i]**gamma)/theta))
#     print(f_t[i])
# for i in range(5):
#     total = total*f_t[i]

# print(math.log(total))

x = np.random.default_rng().uniform(0,1,100)

theta = theta = 125
gamma = 2.5

weibull_x = np.zeros(100)

for i in range(100):
    weibull = theta*(-math.log(x[i]))**(1/gamma)
    weibull_x[i] = weibull

df_weibull_x = pd.DataFrame(weibull_x,index=range(1,101), columns = ['TTF'])
root = tk.Tk()
root.withdraw()
export_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')
df_weibull_x.to_excel(export_file_path,sheet_name='Dados simulados')
        