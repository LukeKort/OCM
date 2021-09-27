# Particle Swarm (Aug. 04, 2021)

import time
import numpy as np
import random as rand

def pso(
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
    ):

    from random_matrix import radom_generator #random generator. takes x and y vector dimentions between the limits a and b
    
    if cdf_type == 'weibull':
        from functions_weibull import objective #objetive function(s)
        from functions_weibull import constraints #constraint function(s)
    else:
        from functions_lognormal import objective #objetive function(s)
        from functions_lognormal import constraints #constraint function(s)

    best_result_acum = np.empty((n_iterations)) #preallocation
    v = radom_generator(n_variables,n_particles,a,b) #velocity matrix
    x_aux = radom_generator(n_variables,n_particles,a,b)
    x = radom_generator(n_variables,n_particles,a,b)
    x_best = np.zeros((n_variables))

    cc = 1 #controler counter

    t_0 = time.time() #start time

    for i in range(n_iterations):  
        x_0=x.copy() #stores the last x before uptade
        for j in range(n_particles):
            v[:,j]= pso_only_w*v[:,j] + rand.random()*pso_only_c1*(x_aux[:,j]-x[:,j]) + rand.random()*pso_only_c2*(x_best - x[:,j]) #new velocity matrix
            x[:,j]=x_0[:,j]+v[:,j] #new position matrix
            for k in range(n_variables): #test with the limits (a,b)
                if x[k,j]<a[k]:
                    x[k,j]=a[k]+(b[k]-a[k])*rand.random()
                if x[k,j]>b[k]:
                    x[k,j]=a[k]+(b[k]-a[k])*rand.random()
            if constraints(x[:,j],parametro_1,parametro_2,tm,tr,lim_conf,lim_disp) is True: #teste the new x within the constraints functions
                if objective(x[:,j],mttf,c_m,c_r,c_inc,t_ser,parametro_1,parametro_2) < objective(x_aux[:,j],mttf,c_m,c_r,c_inc,t_ser,parametro_1,parametro_2): #teste the new x within the objetive function
                    x_aux[:,j] = x[:,j].copy() #setting new best particle position
                    
                    if cc == 1:
                        results = np.full(n_particles,objective(x_aux[:,j],mttf,c_m,c_r,c_inc,t_ser,parametro_1,parametro_2)) #the 1st best value will fill the results vector
                        best_result_acum = np.full(n_iterations,objective(x_aux[:,j],mttf,c_m,c_r,c_inc,t_ser,parametro_1,parametro_2))
                        cc += 1
                    else:    
                        results[j] = objective(x_aux[:,j],mttf,c_m,c_r,c_inc,t_ser,parametro_1,parametro_2) #save result per particle
                    
                    best_result = min(results).copy() #find best result of all particles
                    best_result_acum[i] = best_result.copy()
                    idx = results.tolist().index(best_result) #find the best result's index inside the results vector
                    x_best = x_aux[:,idx] #find the best result's position
        
        if tolerance >= np.amax(abs(x-x_0)): #break for setting tolerance
            break

    t_end = time.time() #finish time
    t_total = t_end - t_0 #total processing time

    if cc == 1:
        best_result = x_best = 'Not found!' #if the problem can't be solved, rise the messange
    
    return({'best_result':best_result,'acumulate_result':best_result_acum,'x_best':x_best,'t_total':t_total,'max_n_iteration':i})