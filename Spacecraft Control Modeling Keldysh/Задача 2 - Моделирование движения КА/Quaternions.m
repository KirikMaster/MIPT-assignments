function [y] = Quaternions(x, t, params)
J = params.J;
Q = x(1:4);
w = x(5:7);

y = zeros(7, 1);
y(1:4) = 0.5 * quatmultiply(Q.', cat(1, 0, w).');
y(5:7) = -cross(J^-1 * w, J * w) + J^-1 * ControlMoment(t, x, params);
end