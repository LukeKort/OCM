# Objectives and constraints functions (Aug. 04, 2021)

import math
import numpy as np

def objective(var_o): #objetive functions Weibull

    #confiabilidade

    gamma_ = 
    theta = 
    t = int(math.floor(var_o.copy()))

    r_t = math.exp(-((t/theta)**(gamma_)))
        
    #custo

    c_m = 1000
    c_r = 2500
    c_inc = 10000
    t_ser = 87600
    mttf = 

    c_t = (t_ser/t)*c_m*r_t + (t_ser/mttf)*(c_r+c_inc)*(1-r_t)  
    
    #função objetivo

    y = c_t

    return y

def constraints(var_c): #constraint functions

    #confiabilidade
    
    gamma_ = 
    theta = 

    lim =   #limite

    t = int(math.floor(var_c.copy()))

    r_t = math.exp(-((t/theta)**(gamma_)))

    #disponibilidade

    t_m =        #tempo de reparo
    t_r =      #tempo de manutenção

    a_t = t/(t + r_t*t_m + (1-r_t)*t_r)

    #Substituir r_t por a_t para usar função de confiabilidade como restrição

    #constraint functions 1 to n
    if (r_t >= lim): #test conditions 1 to n
        return True #all conditions has been met
    else:
        return False #one or mor_t condition hasn't been met

def objective(var_o): #objetive functions Lognormal

    #confiabilidade

    mu = 5.9093828021596
    sigma = 0.486238331177103

    t = int(math.floor(var_o.copy()))

    z = (mu - math.log(var_o))/sigma

    termo_1 = ((4-math.pi)*abs(abs(z)) + math.sqrt(2*math.pi)*(math.pi-2))
    termo_2 = (((4-math.pi)*math.sqrt(2*math.pi)*abs(z)**2)+(2*math.pi*abs(z))+(2*math.sqrt(2*math.pi)*(math.pi-2)))
    termo_3 = math.exp(-(abs(z)**2)/2)

    if z < 0:
        r_t = 1-((termo_1/termo_2)*termo_3)
    else:
        r_t = 1 - (1-((termo_1/termo_2)*termo_3))

        
    #custo

    c_m = 1000
    c_r = 2500
    c_inc = 10000
    t_ser = 87600
    mttf = 413

    c_t = (t_ser/t)*c_m*r_t + (t_ser/mttf)*(c_r+c_inc)*(1-r_t)  
    
    #função objetivo

    y = c_t

    return y

def constraints(var_c): #constraint functions

    #confiabilidade

    mu = 5.9093828021596
    sigma = 0.486238331177103

    t = int(math.floor(var_c.copy()))

    z = (mu - math.log(var_c))/sigma

    termo_1 = ((4-math.pi)*abs(abs(z)) + math.sqrt(2*math.pi)*(math.pi-2))
    termo_2 = (((4-math.pi)*math.sqrt(2*math.pi)*abs(z)**2)+(2*math.pi*abs(z))+(2*math.sqrt(2*math.pi)*(math.pi-2)))
    termo_3 = math.exp(-(abs(z)**2)/2)

    if z < 0:
        r_t = 1-((termo_1/termo_2)*termo_3)
    else:
        r_t = 1 - (1-((termo_1/termo_2)*termo_3))


    #disponibilidade

    t_m =  3      #tempo de reparo
    t_r =  5    #tempo de manutenção

    a_t = t/(t + r_t*t_m + (1-r_t)*t_r)

    #Substituir r_t por a_t para usar função de confiabilidade como restrição

    #constraint functions 1 to n
    if (a_t >= 0.99): #test conditions 1 to n
        return True #all conditions has been met
    else:
        return False #one or mor_t condition hasn't been met