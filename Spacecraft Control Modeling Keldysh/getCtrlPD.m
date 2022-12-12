function [control] = getCtrlPD(x_means, x_ref, params)
%GETCTRLPD Summary of this function goes here
%   Detailed explanation goes here
control = - params.k1*(x_means(1) - x_ref(1)) - params.k2*(x_means(2) - x_ref(2)) + params.c*x_means(1);
end

