function [y] = Moment2(x, t, data, params)
%MOMENT2 calculates gravitational, magnetic and control torque
    J = params.J; % ССК
    J_inv = params.J_inv; % ССК
    mu = params.mu;
    r = x(1:3)'; % ИСК
    R = norm(r);
    v = x(4:6)'; % ИСК
    Q = x(7:10); % ИСК -> ССК
    D = quat2dcm(Q); % ССК -> ИСК
    wabs = x(11:13)'; % ССК, Абсолютная
    B = D * data.B;
    mm_c = data.mm_c;
    M_grav = 3*params.mu / norm(r)^5*cross(D*r, J*D*r); % ССК
    M_magn = cross(params.mm + mm_c, B); % ССК
    
    y(1:3) = v; % ИСК
    y(4:6) = -mu * r / R^3; % ИСК
    y(7:10) = 0.5 * quatmultiply(Q, [0, wabs']); % ИСК -> ССК
    y(11:13) = J_inv * (-cross(wabs, J * wabs) + M_grav + M_magn); % ССК, абсолютная
end