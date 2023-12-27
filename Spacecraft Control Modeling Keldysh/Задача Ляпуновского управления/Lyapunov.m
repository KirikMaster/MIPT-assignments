function [M_ctrl] = Lyapunov(r, A0, D, w, J, data, params)
%UNTITLED Summary of this function goes here
%   A0: ИСК -> ОСК
%   D: ССК -> ИСК
%   w: ССК
    global task
    global Qstart
    global TMP
    kq = 5e-1;
    kw = 5e-1;
    %J ССК
    mu = params.mu;
    r_nrm = norm(r);
    w0 = sqrt(mu / r_nrm^3);

    incl_ref = deg2rad(0);
    switch task
        %Stabilization in orbital SK
        case 'orbital'
            rotvect_ref = normalized([1.0 1.0 0.0]'); % ОСК
            B = quat2dcm(quatnormalize([cos(incl_ref/2), sin(incl_ref/2)*rotvect_ref.'])); % ОСК -> ОпСК
            R = D * A0 * B.';
            Q_ref = dcm2quat2(R); % ОпСК -> ССК
            w_ref = w0 * A0(:,:,1) * [0 1 0]'; % ИСК
            dw_ref = [0 0 0]'; % ИСК
        %Stabilization in inertial SK
        case 'inertial'
            rotvect_ref = normalized([1.0 1.0 0.0]'); % ИСК
            D_ref = quat2dcm(quatnormalize([cos(incl_ref/2), sin(incl_ref/2)*rotvect_ref.'])); % ИСК -> ОпСК
            R = D.' * D_ref.';
            Q_ref = dcm2quat2(R); % ОпСК -> ССК
            w_ref = [0 0 0]'; % ИСК
            dw_ref = [0 0 0]'; % ИСК
    end
    Qstart = Q_ref;
    TMP = Q_ref;
    w_rel = w - D * w_ref;
    q0 = Q_ref(1);
    q = vect2cols(Q_ref(2:4));

    M_grav_e = data.M_grav;
    M_magn_e = data.M_magn;

    M_ctrl = (cross(w, J*w) - M_grav_e - M_magn_e - J * cross(w, D * w_ref) + ...
        J*D*dw_ref - 0.5*kq*q0*J*q - 0.5*kw*J*w_rel);
end