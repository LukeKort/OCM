import math
#confiabilidade

var_c = 236.83501593

#confiabilidade

mu = 3.17022358779506
sigma = 0.186847401773389

t = int(math.floor(var_c))

z = (mu - math.log(t))/sigma

termo_1 = ((4-math.pi)*abs(abs(z)) + math.sqrt(2*math.pi)*(math.pi-2))
termo_2 = (((4-math.pi)*math.sqrt(2*math.pi)*abs(z)**2)+(2*math.pi*abs(z))+(2*math.sqrt(2*math.pi)*(math.pi-2)))
termo_3 = math.exp(-(abs(z)**2)/2)

if z > 0:
    r_t = 1-((termo_1/termo_2)*termo_3)
else:
    r_t = 1 - (1-((termo_1/termo_2)*termo_3))


#disponibilidade

t_m =  0.5      #tempo de reparo
t_r =  2    #tempo de manutenção

a_t = t/(t + r_t*t_m + (1-r_t)*t_r)

#custo

c_m = 1000
c_r = 2500
c_inc = 10000
t_ser = 87600
mttf = 24.21329475

c_t = (t_ser/t)*c_m*r_t + (t_ser/mttf)*(c_r+c_inc)*(1-r_t)

print('r_t:',r_t,'\na_t:',a_t,'\nc_t:',c_t,'\nt:',t)