function [rv] = osc2rv(z, params)
% z = e, a, Om, v, i, w
% № = 1, 2, 3,  4, 5, 6
e = z(1);
a = z(2);
Om = z(3);
v = z(4);
i = z(5);
w = z(6);
p = a * (1 - e^2);
r = p / (1 + e * cos(v));
rv = zeros(6, 1);
r_OF = [r*cos(v), r*sin(v), 0];
c = sqrt(params.mu * p);
v_OF = c/p*e*sin(v) * [cos(v), sin(v), 0] + c/r * [-sin(v), cos(v), 0];
B = RotationMatrix(3, Om) * RotationMatrix(1, i) * RotationMatrix(3, w);
rv = [(B*r_OF')', (B*v_OF')'];
end