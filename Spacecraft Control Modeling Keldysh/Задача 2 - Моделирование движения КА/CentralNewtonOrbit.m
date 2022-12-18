function [y] = CentralNewtonOrbite(x, t, params)
    r = x(1:3);
    v = x(4:6);
    y = [v; -params.mu * r / norm(r)^3 + SecondHarm(r, params)];
end