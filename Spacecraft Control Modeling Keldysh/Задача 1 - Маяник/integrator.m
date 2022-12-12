function [x_i1] = integrator(x_i, t_i, regime, dt, control, params)
    if regime == "Control"
        k1 = rightSideCtrl(x_i, t_i, params, control);
        k2 = rightSideCtrl(x_i + dt/2*k1, t_i + dt/2, params, control);
        k3 = rightSideCtrl(x_i + dt/2*k2, t_i + dt/2, params, control);
        k4 = rightSideCtrl(x_i + dt*k3, t_i + dt/2, params, control);
    else
        k1 = rightSide(x_i, t_i, params);
        k2 = rightSide(x_i + dt/2*k1, t_i + dt/2, params);
        k3 = rightSide(x_i + dt/2*k2, t_i + dt/2, params);
        k4 = rightSide(x_i + dt*k3, t_i + dt/2, params);
    end
    x_i1 = x_i +  dt/6*(k1 + 2*k2 + 2*k3 + k4);
end