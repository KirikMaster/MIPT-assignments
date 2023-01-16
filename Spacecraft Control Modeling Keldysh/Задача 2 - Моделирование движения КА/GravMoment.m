function [y] = GravMoment(x, t, params)
    J = params.J; % ССК
    J_inv = params.J_inv; % ССК
    mu = params.mu;
    r = x(1:3)'; % ИСК
    R = norm(r);
    e = r / R; % 3 вектор ОСК (задан в ИСК)
    v = x(4:6)'; % ИСК
    Q = x(7:10); % ССК -> ОСК
    w = x(11:13)'; % ССК, Относительная
    % A: ОСК -> ИСК
    E = quat2dcm(Q).' * [0 0 1]'; % ССК
    % A.' * e ≡ [0 0 1]'
    
    y(1:3) = v; % ИСК
    y(4:6) = -mu * e / R^2; % ИСК
    y(7:10) = 0.5 * quatmultiply(Q, cat(2, 0, w')); % ССК -> ОСК
    y(11:13) = -J_inv * (cross(w, J * w) - 3 * params.mu / R^3 * cross(E, J * E)); % ССК, относительная
end