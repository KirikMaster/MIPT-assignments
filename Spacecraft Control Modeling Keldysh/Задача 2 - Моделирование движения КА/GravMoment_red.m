function [y] = GravMoment_red(x, t, params)
    J = params.J; % ССК
    J_inv = params.J_inv; % ССК
    w0 = params.w0;
    Q = x(1:4); % ССК -> ОСК
    w = x(5:7)'; % ССК, Относительная
    % A: ОСК -> ИСК
    E = quat2dcm(Q).' * [0 0 1]'; % ССК
    % A.' * e ≡ [0 0 1]'
    
    y(1:4) = 0.5 * quatmultiply(Q, cat(2, 0, w')); % ССК -> ОСК
    y(5:7) = -J_inv * (cross(w, J * w) - 3 * w0^2 * cross(E, J * E)); % ССК, относительная
end