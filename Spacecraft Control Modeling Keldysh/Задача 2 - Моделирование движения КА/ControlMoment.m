function [Mctrl] = ControlMoment(x, t, params)
if params.scenario == "Euler"
    Mctrl = zeros(3, 1);
elseif params.scenario == "Lagrange"
    Mctrl = params.m * cross(params.g, x);
end
end