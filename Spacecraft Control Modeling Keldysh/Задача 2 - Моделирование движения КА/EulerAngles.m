function [y] = EulerAngles(x, t, params)
S = params.S;
J = params.J;
psi = x(1);
theta = x(2);
phi = x(3);
w = S * x(4:6);
p = w(1);
q = w(2);
r = w(3);
w = x(4:6);

y = zeros(6, 1);
y(1) = (p*sin(phi) + q*cos(phi))/sin(theta);
y(2) = p*cos(phi) - q*sin(phi);
y(3) = r - cot(theta)*(p*sin(phi) + q*cos(phi));
y(4:6) = -cross(J^-1 * w, J * w) + J^-1 * ControlMoment(x(1:3), t, 'Euler Angles', params);
end