function [y] = GravMoment(x, t, params)
    J = params.J; % ССК
    J_inv = params.J_inv; % ССК
    mu = params.mu;
    r = x(1:3)'; % ИСК
    R = norm(r);
    e = r / R; % 3 вектор ОСК (задан в ИСК)
    v = x(4:6)'; % ИСК
    Q = x(7:10); % ССК -> ИСК
    D = quat2dcm(Q); % ССК -> ИСК
    %Qrel - ССК -> ОСК
    % A0: ОСК -> ИСК
    A0 = zeros(3, 3);
    A0(:, 3) = normalized(r);
    A0(:, 2) = normalized(cross(r, v));
    A0(:, 1) = cross(A0(:, 2), A0(:, 3));
    Drel = D * A0; % ССК -> ОСК
    w0 = sqrt(params.mu / R^3);
    wabs = x(11:13)'; % ССК, Относительная
    %wabs = w + w0 * Drel.' * [0 1 0]'; % ССК, Абсолютная
    E = Drel.' * [0 0 1]'; % ССК
    % A.' * e ≡ [0 0 1]'
    
    y(1:3) = v; % ИСК
    y(4:6) = -mu * e / R^2; % ИСК
    y(7:10) = 0.5 * quatmultiply(Q, [0, wabs']); % ССК -> ИСК
    y(11:13) = -J_inv * (cross(wabs, J * wabs) - 3 * params.mu / R^3 * cross(E, J * E)); % ССК, абсолютная
end