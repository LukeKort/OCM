import math
#confiabilidade

var = 11

gamma_ = 3.000122547
theta = 30.63657894

t = int(math.floor(var))

r_t = math.exp(-((t/theta)**(gamma_)))


#disponibilidade

t_m = 0.5       #tempo de reparo
t_r = 2      #tempo de manutenção

a_t = t/(t + r_t*t_m + (1-r_t)*t_r)

#custo

c_m = 1000
c_r = 2500
c_inc = 10000
t_ser = 87600
mttf = 27.8067216

c_t = (t_ser/t)*c_m*r_t + (t_ser/mttf)*(c_r+c_inc)*(1-r_t) 

print('r_t:',r_t,'\na_t:',a_t,'\nc_t:',c_t,'\nt:',t)