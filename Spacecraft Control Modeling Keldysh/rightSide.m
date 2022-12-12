function [dot_x] = rightSide(x, t, params)
    dot_x = [x(2);
             -params.c/params.m*x(1)];
end