function [y] = EulerAngles(x, t, params)
J = params.J;
psi = x(1);
theta = x(2);
phi = x(3);
p = x(4);
q = x(5);
r = x(6);
w = [p, q, r]';

y = zeros(6, 1);
y(1) = (p*sin(phi) + q*cos(phi))/sin(theta);
y(2) = p*cos(phi) - q*sin(phi);
y(3) = r - cot(theta)*(p*sin(phi) + q*cos(phi));
y(4:6) = -cross(J^-1 * w, J * w) + J^-1 * ControlMoment(t, x, params);
end