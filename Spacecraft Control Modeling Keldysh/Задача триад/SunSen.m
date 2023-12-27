function [s, B] = SunSen(A)
%SUNSEN models a sun sensor on a SC, which measures sun's position
%   Detailed explanation goes here
rs_true = normalized([1, 1, 0]).'; % ИСК
sigma_sun = 0.02;
D = EulerMatrix(0, 0, 0); % ССК -> ДСК СД

rs = D.' * A.' * rs_true; % ДСК
B = D * create_SK(rs); % ССК -> СолСК
alpha = randn2(0, sigma_sun);
phi = rand2(0, 2*pi);
s = B * [sin(alpha) * cos(phi), sin(alpha) * sin(phi), cos(alpha)]'; % ССК
end

