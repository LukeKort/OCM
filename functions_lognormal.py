# Objectives and constraints functions (May. 05, 2021)
import math
import numpy as np

# from numpy.cor_t.fromnumeric import around

def objective(var_o,mttf,c_m,c_r,c_inc,t_ser,parametro_1,parametro_2): #objetive functions Lognormal

    #confiabilidade

    mu = parametro_1
    sigma = parametro_2

    t = int(math.floor(var_o.copy()))

    ze = (mu - math.log(t))/sigma

    termo_1 = ((4-math.pi)*abs(ze) + math.sqrt(2*math.pi)*(math.pi-2))
    termo_2 = (((4-math.pi)*math.sqrt(2*math.pi)*abs(ze)**2)+(2*math.pi*abs(ze))+(2*math.sqrt(2*math.pi)*(math.pi-2)))
    termo_3 = math.exp(-(abs(ze)**2)/2)

    if ze > 0:
        r_t = 1-((termo_1/termo_2)*termo_3)
    else:
        r_t = 1 - (1-((termo_1/termo_2)*termo_3))

    c_t = (t_ser/t)*c_m*r_t + (t_ser/mttf)*(c_r+c_inc)*(1-r_t)  
    
    #função objetivo

    y = c_t

    return y

def constraints(var_c,parametro_1,parametro_2,t_m,t_r,lim_conf,lim_disp): #constraint functions

    #confiabilidade

    mu = parametro_1
    sigma = parametro_2

    t = int(math.floor(var_c.copy()))

    z = (mu - math.log(t))/sigma

    termo_1 = ((4-math.pi)*abs(abs(z)) + math.sqrt(2*math.pi)*(math.pi-2))
    termo_2 = (((4-math.pi)*math.sqrt(2*math.pi)*abs(z)**2)+(2*math.pi*abs(z))+(2*math.sqrt(2*math.pi)*(math.pi-2)))
    termo_3 = math.exp(-(abs(z)**2)/2)

    if z > 0:
        r_t = 1-((termo_1/termo_2)*termo_3)
    else:
        r_t = 1 - (1-((termo_1/termo_2)*termo_3))


    #disponibilidade

    a_t = t/(t + r_t*t_m + (1-r_t)*t_r)

    #Substituir r_t por a_t para usar função de confiabilidade como restrição

    #constraint functions 1 to n
    if (a_t >= lim_disp) and (r_t >= lim_conf): #test conditions 1 to n
        return True #all conditions has been met
    else:
        return False #one or mor_t condition hasn't been met