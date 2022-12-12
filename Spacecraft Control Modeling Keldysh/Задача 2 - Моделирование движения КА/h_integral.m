function [h] = h_integral(x, params)
r = norm(x(1:3));
v = norm(x(4:6));
h = v.^2/2 - params.mu./r;
end