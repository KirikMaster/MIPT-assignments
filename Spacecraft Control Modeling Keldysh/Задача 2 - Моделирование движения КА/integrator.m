function [x_i1] = integrator(func, x_i, t_i, dt, params)
    k1 = func(x_i, t_i, params);
    k2 = func(x_i + dt/2*k1, t_i + dt/2, params);
    k3 = func(x_i + dt/2*k2, t_i + dt/2, params);
    k4 = func(x_i + dt*k3, t_i + dt/2, params);
    x_i1 = x_i +  dt/6*(k1 + 2*k2 + 2*k3 + k4);
end