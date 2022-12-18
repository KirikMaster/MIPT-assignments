function [y] = Quaternions(x, t, params)
J = params.J;
J_inv = params.J_inv;
Q = x(1:4);
w = x(5:7);

y = zeros(7, 1);
y(1:4) = 0.5 * quatmultiply(Q.', cat(1, 0, w).');
y(5:7) = -J_inv * cross(w, J * w) + J_inv * ControlMoment(Q, t, 'Quat', params);
end