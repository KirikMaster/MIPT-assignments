function [dot_x] = rightSideCtrl(x, t, params, control)
    dot_x = [x(2);
             -params.c/params.m*x(1) + control/params.m];
end