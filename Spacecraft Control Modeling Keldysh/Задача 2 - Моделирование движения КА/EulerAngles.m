function [y] = EulerAngles(x, t, params)
%S = params.S;
J = params.J;
J_inv = params.J_inv;
psi = x(3);
theta = x(2);
phi = x(1);
w = x(4:6);
p = w(1);
q = w(2);
r = w(3);

y = zeros(6, 1);
y(3) = (p*sin(phi) + q*cos(phi))/sin(theta);
y(2) = p*cos(phi) - q*sin(phi);
y(1) = r - cot(theta)*(p*sin(phi) + q*cos(phi));
y(4:6) = -J_inv * cross(w, J * w) + J_inv * ControlMoment(x(1:3), t, 'Euler Angles', params);
end