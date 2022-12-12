function [control] = getControl(x_means, x_ref, params)
%GETCTRLPD Summary of this function goes here
%   Detailed explanation goes here
m = params.m;
l = params.l;
g = params.g;
k4 = params.k4;
k3 = params.k3;
control = x_ref(3)*m*l*l + m*g*l*sin(x_means(1)) - k4*(x_means(1) - x_ref(1)) - k3*(x_means(2) - x_ref(2));
end

