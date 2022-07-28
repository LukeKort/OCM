# Main ( May 03, 2022) by Lucas Kort
import math
import numpy as np
from numpy.core.fromnumeric import mean, transpose
from numpy.lib.arraypad import pad
from numpy.lib.function_base import append #some arry operations
import pandas as pd
import sys 
from PyQt5 import QtGui, QtCore, QtWidgets
import app_gui
import os #to open external programms
import tkinter as tk #hide tk window
from tkinter import filedialog #get a file dialog window
from function_repository import predict_val

#Parâmetros
# theta = gamma_ = sigma = mu = parametro_1 = parametro_2 = 0

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = app_gui.Ui_mainWindow() # in this and next line you say that you will use all widgets from testUI over self.ui
        self.ui.setupUi(self)
        self.setWindowTitle('OCM - v1.0.2') #set windows title Opp [--v]

        #Aba dados
        self.ui.salvar_dados_2.clicked.connect(self.salvar_dados)
        self.ui.carregar_dados_salvos_2.clicked.connect(self.carregar_dados)
        self.ui.processar_rede_2.clicked.connect(self.ajustar_dados)
        self.ui.select_weibull.toggled.connect(self.weibull_check)

        #Aba indicadores
        self.ui.calcular_conf_para_tempo.clicked.connect(self.calcular_conf_para_tempo)
        self.ui.calcular_tempo_p_conf.clicked.connect(self.calcular_tempo_para_conf)
        self.ui.calcular_falha_p_tempo.clicked.connect(self.calcular_falha_para_tempo)
        self.ui.calcular_tempo_p_falha.clicked.connect(self.calcular_tempo_para_falha)

        #Aba Otimização
        self.ui.link_to_opp.clicked.connect(self.link_2_opp)
        self.ui.processar_opp.clicked.connect(self.otimizar)
        self.ui.plotar_grafico_opp.clicked.connect(self.plt_grafico_opp)

        #Aba Sobre
        self.ui.link_to_github.clicked.connect(self.link_2_github)
        self.ui.link_to_ajuda_yt.clicked.connect(self.link_to_ajuda_yt)
        #self.ui.link_to_doc.clicked.connect(self.link_2_doc)
        self.ui.link_kort.clicked.connect(self.link_kort)




    def salvar_dados(self):

        #Salvar dados em um arquivo .csv

        try:
            nome_sistema = str(self.ui.lineEdit.text())
            ttf1 = float(self.ui.ttf1.text())
            ttf2 = float(self.ui.ttf2.text())
            ttf3 = float(self.ui.ttf3.text())
            ttf4 = float(self.ui.ttf4.text())
            ttf5 = float(self.ui.ttf5.text())

            ttf = {nome_sistema:[ttf1,ttf2,ttf3,ttf4,ttf5]}

        except:
            root = tk.Tk() #abrir janela para entrar com path de salvamento
            root.withdraw() #esconder janela do terminal
            tk.messagebox.showerror('Erro de entrada de dados', 'Por favor, complete o campo TTF.')
            return

        df_ttf = pd.DataFrame(ttf, index = range(1,6))

        root = tk.Tk() #abrir janela para entrar com path de salvamento
        root.withdraw() #esconder janela do terminal
        salvar_arquivo_path = filedialog.asksaveasfilename(defaultextension='.csv') #local de salvamento
        try:
            df_ttf.to_csv(salvar_arquivo_path)
        except:
            return

    def carregar_dados(self):

        global ttf #criar variáveis globais

        root = tk.Tk() #abrir janela para entrar com path de salvamento
        root.withdraw() #esconder janela do terminal
        file_path = filedialog.askopenfile(filetypes=(('cvs file', '*.csv'),))

        try:
            dada_df = pd.read_csv(file_path) #se nenhum path foi informado, não lerá arquivo
        except:
            root = tk.Tk() #abrir janela para entrar com path de salvamento
            root.withdraw() #esconder janela do terminal
            tk.messagebox.showinfo('Erro de seleção', 'Nenhum arquivo selecionado.')
            return 
       
        col_name = list(dada_df)[1]

        df = dada_df[col_name]

        ttf1 = df[0]
        ttf2 = df[1]
        ttf3 = df[2]
        ttf4 = df[3]
        ttf5 = df[4]

        ttf = [[ttf1,ttf2,ttf3,ttf4,ttf5]]

        print(ttf)

        self.ajustar_dados()

    def ajustar_dados(self):

        global ttf, theta, gamma_, mu, sigma #criar variáveis globais

        try:
            teste = ttf
        except:
            try:
                ttf1 = float(self.ui.ttf1.text())
                ttf2 = float(self.ui.ttf2.text())
                ttf3 = float(self.ui.ttf3.text())
                ttf4 = float(self.ui.ttf4.text())
                ttf5 = float(self.ui.ttf5.text())

                ttf = [[ttf1,ttf2,ttf3,ttf4,ttf5]]
            except:
                root = tk.Tk() #abrir janela para entrar com path de salvamento
                root.withdraw() #esconder janela do terminal
                tk.messagebox.showerror('Erro de entrada de dados', 'Por favor, complete o campo TTF.')
                return

        #Weibull

        model_val = predict_val(ttf) #prever valores pelo modelo rna
        theta = 10**model_val[0,0]   #transformar log(theta) em theta
        gamma_ = model_val[0,1]

        self.ui.mostrar_theta.clear() #limpar qualquer valor já exposto
        self.ui.mostrar_gamma.clear()
        self.ui.mostrar_theta.append(str(round(theta,4))) #exibir valor com 4 casas decimais
        self.ui.mostrar_gamma.append(str(round(gamma_,4)))
        
        #Lognomal

        soma_log = soma_log_quadrado = 0

        for i in range(5):
            soma_log = soma_log + math.log(ttf[0][i])
            soma_log_quadrado = soma_log_quadrado + (math.log(ttf[0][i]))**2

        mu = soma_log/5
        sigma = math.sqrt((soma_log_quadrado - ((soma_log**2)/5))/5)

        self.ui.mostrar_mu.clear()
        self.ui.mostrar_sigma.clear()
        self.ui.mostrar_mu.append(str(round(mu,4)))
        self.ui.mostrar_sigma.append(str(round(sigma,4)))

        #Cálculo do coeficiente de correlação
        r_x = np.zeros(5)
        r_y_w = np.zeros(5)
        r_y_l = np.zeros(5)

        for i in range(5):
            r_x[i] = ttf[0][i]
            try:
                f_x = 1 - math.exp(-((ttf[0][i]/theta)**(gamma_)))
            except:
                root = tk.Tk() #abrir janela para entrar com path de salvamento
                root.withdraw() #esconder janela do terminal
                tk.messagebox.showerror('Erro de entrada de dados', 'Os dados de TTF são muito grandes.\nExperimente converter a unidade.')
                return
            r_y_w[i] = -math.log(1-f_x)
            r_y_l[i] = (math.log(ttf[0][i])-mu)/sigma
        
        r_weibull = np.corrcoef(r_x,r_y_w)
        r_lognormal = np.corrcoef(r_x,r_y_l)

        self.ui.mostrar_r_weibull.clear()
        self.ui.mostrar_r_lognormal.clear()
        self.ui.mostrar_r_weibull.append((str(round(r_weibull[1,0]*100,4)) + '%'))
        self.ui.mostrar_r_lognormal.append((str(round(r_lognormal[1,0]*100,4)) + '%'))
        

    def weibull_check(self):

        #Verificar qual distribuição escolhida

        global parametro_1, parametro_2, cdf_type

        try:
            teste = theta #testar se os dados já foram ajustados
        except:
            self.ajustar_dados() #ajustar se não tiverem sido ainda

        if self.ui.select_weibull.isChecked():
            cdf_type = 'weibull'
            parametro_1 = theta
            parametro_2 = gamma_
        else:
            cdf_type = 'lognormal'
            parametro_1 = mu
            parametro_2 = sigma


    def calcular_conf_para_tempo(self):

        #Calcular confiabildiade a partir de uma dado tempo

        try:
            t = float(self.ui.tempo_2_conf.text())
        except:
            root = tk.Tk() #abrir janela para entrar com path de salvamento
            root.withdraw() #esconder janela do terminal
            tk.messagebox.showerror('Erro de entrada de dados', 'Por favor, complete o campo "Tempo".')
            return

        try:
            teste = cdf_type #testar se a distribuição foi escolhida
        except:
            self.weibull_check() #chamar a função de escolha caso não tenha sido ainda
        
        if cdf_type == 'weibull':
            #Calculo da confiabilidade
            re = math.exp(-((t/theta)**(gamma_)))
        else:
            #Calculo da confiabilidade
            z = (mu - math.log(t))/sigma
            termo_1 = ((4-math.pi)*abs(abs(z)) + math.sqrt(2*math.pi)*(math.pi-2))
            termo_2 = (((4-math.pi)*math.sqrt(2*math.pi)*abs(z)**2)+(2*math.pi*abs(z))+(2*math.sqrt(2*math.pi)*(math.pi-2)))
            termo_3 = math.exp(-(abs(z)**2)/2)
            if z > 0:
                re = 1-((termo_1/termo_2)*termo_3)
            else:
                re = 1 - (1-((termo_1/termo_2)*termo_3))
            
        self.ui.exibir_conf_para_tempo.clear()
        self.ui.exibir_conf_para_tempo.append(str(round(re,4)))

    def calcular_tempo_para_conf(self):

        #Calcular confiabildiade a partir de uma dado tempo

        try:
            re = float(self.ui.conf_2_tempo.text())
        except:
            root = tk.Tk() #abrir janela para entrar com path de salvamento
            root.withdraw() #esconder janela do terminal
            tk.messagebox.showerror('Erro de entrada de dados', 'Por favor, complete o campo "Confiabildiade".')
            return

        try:
            teste = cdf_type #testar se a distribuição foi escolhida
        except:
            self.weibull_check() #chamar a função de escolha caso não tenha sido ainda


        if cdf_type == 'weibull':
            #Calculo do tempo weibull
            log_re = -math.log(re)
            t = log_re**(1/gamma_)*theta
        else:
            root = tk.Tk() #abrir janela para entrar com path de salvamento
            root.withdraw() #esconder janela do terminal
            tk.messagebox.showinfo('Informação', 'Função não disponivel para Lognormal.\nPor favor, altere para Weibull.')
            return
        
        self.ui.exibir_tempo_para_conf.clear()
        self.ui.exibir_tempo_para_conf.append(str(round(t,4)))


    def calcular_falha_para_tempo(self):

        #Calcular taxa de falha a partir de uma dado tempo

        try:
            t = float(self.ui.tempo_2_falha.text())
        except:
            root = tk.Tk() #abrir janela para entrar com path de salvamento
            root.withdraw() #esconder janela do terminal
            tk.messagebox.showerror('Erro de entrada de dados', 'Por favor, complete o campo "Tempo".')
            return

        try:
            teste = cdf_type #testar se a distribuição foi escolhida
        except:
            self.weibull_check() #chamar a função de escolha caso não tenha sido ainda
        
        if cdf_type == 'weibull':
            #calculo da tx. de falha
            h = (gamma_/theta)*((t/theta)**(gamma_-1))
        else:
            #Calculo da confiabilidade (precisa para calcula a tx)
            z = (mu - math.log(t))/sigma
            termo_1 = ((4-math.pi)*abs(abs(z)) + math.sqrt(2*math.pi)*(math.pi-2))
            termo_2 = (((4-math.pi)*math.sqrt(2*math.pi)*abs(z)**2)+(2*math.pi*abs(z))+(2*math.sqrt(2*math.pi)*(math.pi-2)))
            termo_3 = math.exp(-(abs(z)**2)/2)
            if z > 0:
                re = 1-((termo_1/termo_2)*termo_3)
            else:
                re = 1 - (1-((termo_1/termo_2)*termo_3))
            #calculo da tx. de falha
            h = ((1/(math.sqrt(2*math.pi)*sigma*t))*math.exp(-(1/(2*(sigma**2)))*(math.log(t)-mu)**2))/re

        self.ui.exibir_falha_para_tempo.clear()
        #self.ui.exibir_falha_para_tempo.append(str(round(h,4)))
        self.ui.exibir_falha_para_tempo.append("{:.4e}".format(h))

    def calcular_tempo_para_falha(self):

        #Calcular tempo a partir de uma dada taxa de falha

        try:
            h = float(self.ui.falha_2_tempo.text())
        except:
            root = tk.Tk() #abrir janela para entrar com path de salvamento
            root.withdraw() #esconder janela do terminal
            tk.messagebox.showerror('Erro de entrada de dados', 'Por favor, complete o campo "Tx de falha".')
            return


        try:
            teste = cdf_type #testar se a distribuição foi escolhida
        except:
            self.weibull_check() #chamar a função de escolha caso não tenha sido ainda
        
        if cdf_type == 'weibull':
            #calculo da tx. de falha
            t = theta*((h*theta/gamma_)**(1/(gamma_-1)))
        else:
            root = tk.Tk() #abrir janela para entrar com path de salvamento
            root.withdraw() #esconder janela do terminal
            tk.messagebox.showinfo('Informação', 'Função não disponivel para Lognormal.\nPor favor, altere para Weibull.')
            return

        self.ui.exibir_tempo_p_falha.clear()
        self.ui.exibir_tempo_p_falha.append(str(round(t,4)))




    def link_2_opp(self):

        #Abrir link para o aplicativo Opp

        import webbrowser

        url = 'https://github.com/LukeKort/Opp/releases'
        os.startfile(url)

    def otimizar(self):

        #Processar otimização

        global melhor_intervalo, b

        try:
            teste = cdf_type #testar se a distribuição foi escolhida
        except:
            self.weibull_check() #chamar a função de escolha caso não tenha sido ainda
        
        from pso import pso #Importar o método numérico
        
        mttf = np.mean(ttf) 


        #Configuração PSO
        n_particles = 600
        n_variables = 1
        n_iterations = 100
        tolerance = 1e-20
        a = [1] #A função random_generator precisa de trabalhar com listas
        
        try:
            b = [float(self.ui.limite_tempo.text())]
            pso_only_w = float(self.ui.w_pso.text())
            pso_only_c1 = float(self.ui.c1_pso.text())
            pso_only_c2 = float(self.ui.c2_pso.text())

            #Custos de manutenção
            c_m = float(self.ui.c_rep_prog.text())
            c_r = float(self.ui.c_rep_n_prog.text())
            c_inc = float(self.ui.perdas_parada.text())
            t_ser = float(self.ui.tempo_servico.text())

            #Tempos de manutenção
            tm = float(self.ui.t_rep_prog.text())
            tr = float(self.ui.t_rep_n_prog.text())

            #Restrição
            lim_conf = float(self.ui.conf_lim.text())
            lim_disp = float(self.ui.disp_lim.text())
        except:
            root = tk.Tk() #abrir janela para entrar com path de salvamento
            root.withdraw() #esconder janela do terminal
            tk.messagebox.showerror('Erro de entrada de dados', 'Por favor, entre com valores em todos os campos.')
            return

        melhor_intervalo = pso(
            n_particles,
            n_variables,
            n_iterations,
            tolerance,
            a,
            b,
            pso_only_w,
            pso_only_c1,
            pso_only_c2,
            cdf_type,
            mttf,
            c_m,
            c_r,
            c_inc,
            t_ser,
            parametro_1,
            parametro_2,
            tm,
            tr,
            lim_conf,
            lim_disp
            ) #Chamar o método PSO e enviar as variáveis

        self.ui.mostrar_intervalo.clear()
        self.ui.mostrar_intervalo.append(str(int(melhor_intervalo['x_best'][0])))
        self.ui.mostrar_custo.clear()
        self.ui.mostrar_custo.append('R$' + str(round(melhor_intervalo['best_result'],2)))
    
    def plt_grafico_opp(self):

        import matplotlib.pyplot as plt

        self.otimizar() #Garantir que a otimização tinha sido executada

        try:
            plt.figure('Gráfico otimização')
            plt.scatter(range(100),melhor_intervalo['acumulate_result'][0:100],alpha=0.5,label='Custo [R$]')
            plt.title('Otimização do intervalo de MP para custo')
            plt.ylabel('Custo [R$]')
            plt.xlabel('Iteration')
            plt.legend()
            plt.xlim([0,100])
            plt.show()

            stop = b[0] #evitar perda de tempo em acessar lista

            t = np.zeros(100)
            re = np.zeros(100)
            h = np.zeros(100)

            if cdf_type == 'weibull':

                for i in range(100):
                    t[i] = (1+i)*math.ceil(stop/100)
                    #Calculo da confiabilidade
                    re[i] = math.exp(-((t[i]/theta)**(gamma_)))
                    #calculo da tx. de falha
                    h[i] = (gamma_/theta)*((t[i]/theta)**(gamma_-1))
            else:

                for i in range(100):
                    #Calculo da confiabilidade
                    t[i] = (1+i)*math.ceil(stop/100)
                    z = (mu - math.log(t[i]))/sigma
                    termo_1 = ((4-math.pi)*abs(abs(z)) + math.sqrt(2*math.pi)*(math.pi-2))
                    termo_2 = (((4-math.pi)*math.sqrt(2*math.pi)*abs(z)**2)+(2*math.pi*abs(z))+(2*math.sqrt(2*math.pi)*(math.pi-2)))
                    termo_3 = math.exp(-(abs(z)**2)/2)
                    if z > 0:
                        re[i] = 1-((termo_1/termo_2)*termo_3)
                    else:
                        re[i] = 1 - (1-((termo_1/termo_2)*termo_3))
                    #calculo da tx. de falha
                    h[i] = ((1/(math.sqrt(2*math.pi)*sigma*t[i]))*math.exp(-(1/(2*(sigma**2)))*(math.log(t[i])-mu)**2))/re[i]
            
            plt.figure('Gráfico Confiabilidade e Tx. de falha')
            plt.scatter(t,re,alpha=0.5,label='Confiabilidade')
            plt.scatter(t,h,alpha=0.5,label='Taxa de falha')
            plt.title('Confiabilidade por intervalo de MP')
            plt.xlabel('Intervalo de MP')
            plt.legend()
            plt.show()
        except:
            return
        
    def link_2_github(self):

        #Abrir link para o aplicativo Opp

        import webbrowser

        url = 'https://github.com/LukeKort/ocm/releases'
        os.startfile(url)

    def link_to_ajuda_yt(self):

        #Abrir link para o aplicativo Opp

        import webbrowser

        url = 'https://youtu.be/LIYQkKxuirg'
        os.startfile(url)
    
    def link_kort(self):

        #Abrir link para o aplicativo Opp

        import webbrowser

        url = 'https://www.linkedin.com/in/lucaskort/'
        os.startfile(url)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())