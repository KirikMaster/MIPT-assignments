function [w_meas] = AVS(w)
%AVS Measures angular speed of the SC at a given time
%   Detailed explanation goes here
sigma_avs = 5e-5;
delta1 = [0.998, 0.999, 0.998]';
offset = 1e-3 * [1.0, 2.0, 0.5]';
e1 = [1.0, 0.0, 0.0]';
e2 = [0.0, 1.0, 0.0]';
e3 = [0.0, 0.0, 1.0]';

w_meas = [e1, e2, e3].' * w .* delta1 + randn2(offset, sigma_avs);
end

