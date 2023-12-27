function [y] = Moment4(x, t, params)
%MAGNMOMENT calculates gravitational and magnetic torque
    J = params.J; % ССК
    J_inv = params.J_inv; % ССК
    mu = params.mu;
    r = x(1:3)'; % ИСК
    R = norm(r);
    e = r / R; % 3 вектор ОСК (задан в ИСК)
    v = x(4:6)'; % ИСК
    Q = x(7:10); % ИСК -> ССК
    wabs = x(11:13)'; % ССК, Абсолютная
    M_grav = data.M_grav;
    M_magn = data.M_magn;
    M_ctrl = data.M_ctrl;
    
    y(1:3) = v; % ИСК
    y(4:6) = -mu * e / R^2; % ИСК
    y(7:10) = 0.5 * quatmultiply(Q, [0, wabs']); % ССК -> ИСК
    y(11:13) = J_inv * (-cross(wabs, J * wabs) + M_grav + M_magn + M_ctrl); % ССК, абсолютная
end

