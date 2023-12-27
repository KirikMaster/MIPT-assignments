function [Q] = dcm2quat2(A)
%DCM2QUAT2 Summary of this function goes here
%   Detailed explanation goes here
global Qref_init
Q = dcm2quat(A);
%if quatnorm(Q - Qref_init) > quatnorm(Q + Qref_init)
if Q(1) < 0
    Q = -Q;
end
end

