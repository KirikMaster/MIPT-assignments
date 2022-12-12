function [dot_x] = rightSideCtrl(x, t, params, control)
    dot_x = [x(2);
             -params.g/params.l*sin(x(1)) + control/params.m/params.l^2];
end