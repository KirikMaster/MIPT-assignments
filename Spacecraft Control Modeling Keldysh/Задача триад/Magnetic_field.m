function [B] = Magnetic_field(R, params)
%MAGNETIC_FIELD yields the dimensionless vector of magnetic induction for a given point
delta = params.delta;
lam = params.lam;
k = [sin(delta) * cos(lam), sin(delta) * sin(lam), cos(delta)]'; % ИСК
mu0 = params.mu0;

R = vect2cols(R); % ИСК
B = mu0 / norm(R)^5 * (k * norm(R)^2 - 3 * dot(k, R) * R); % ИСК
end

