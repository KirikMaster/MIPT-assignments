function [B_meas] = Magnetometer(r, D, params)
%MAGNETOMETER measures the vector of magnetic field on a SC
%   r - radius-vector of the SC, expected in inertial frame
%   A - matrix of an orientation of the SC, sets transform from inertial to
%   related frame
sigma_magn = 1e-2 * norm(Magnetic_field(r, params));
sigma_orient = 1e-4;
A = EulerMatrix(0, 0, 0); % ССК -> Д2СК
Bias_mat = randn2(eye(3), sigma_orient);

B_true = A.' * D * Magnetic_field(r, params); % Д2СК
%B_meas = B_true;
B_meas = Bias_mat * randn2(B_true, sigma_magn); % ССК
end

