# Objectives and constraints functions (May. 05, 2021)
import math
import numpy as np

# from numpy.cor_t.fromnumeric import around

def objective(var_o,mttf,c_m,c_r,c_inc,t_ser,parametro_1,parametro_2): #objetive functions Lognormal

    #confiabilidade

    gamma_ = parametro_2
    theta = parametro_1

    t = int(math.floor(var_o.copy()))

    r_t = math.exp(-((t/theta)**(gamma_)))
    
    c_t = (t_ser/t)*c_m*r_t + (t_ser/mttf)*(c_r+c_inc)*(1-r_t)  
    
    #função objetivo

    y = c_t

    return y

def constraints(var_c,parametro_1,parametro_2,t_m,t_r,lim_conf,lim_disp): #constraint functions

    #confiabilidade
    
    gamma_ = parametro_2
    theta = parametro_1

    t = int(math.floor(var_c.copy()))

    r_t = math.exp(-((t/theta)**(gamma_)))

    a_t = t/(t + r_t*t_m + (1-r_t)*t_r)

    #constraint functions 1 to n
    if (a_t >= lim_disp) and (r_t >= lim_conf): #test conditions 1 to n
        return True #all conditions has been met
    else:
        return False #one or mor_t condition hasn't been met