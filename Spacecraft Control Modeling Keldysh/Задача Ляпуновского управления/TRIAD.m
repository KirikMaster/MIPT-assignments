function [D_meas, w_meas] = TRIAD(r, D, w, params)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
%%Sun
rs_true = normalized([1, 1, 0]).'; % ИСК % Опорный вектор V1
[s, ~] = SunSen(D); % ССК % Опорный вектор W1 
% Bsun: ССК -> СолСК

%%Magnetometer
B_vect = Magnetic_field(r, params); % ИСК % Опорный вектор V2
B_meas = Magnetometer(r, D, params); % ССК % Опорный вектор W2

%%AVS
w_meas = AVS(w); % ССК

%%TRIAD
D_meas = Create_basis(rs_true, B_vect) * Create_basis(s, B_meas).'; % ИСК -> ССК
end