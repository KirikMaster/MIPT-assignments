function [dot_x] = rightSide(x, t, params)
    dot_x = [x(2);
             -params.g/params.l*sin(x(1))];
end