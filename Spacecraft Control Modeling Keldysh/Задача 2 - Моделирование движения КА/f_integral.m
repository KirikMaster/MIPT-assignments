function [f] = f_integral(x, params)
c = c_integral(x);
r = norm(x(1:3));
f = cross(x(4:6), c) - params.mu * x(1:3) ./ r;
end