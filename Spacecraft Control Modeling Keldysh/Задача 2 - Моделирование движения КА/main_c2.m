%% Setup
clc
clear all
close all

%%parameters
A_ = 1.0;
B_ = 2.3;
C_ = 2.6;
J = [A_, 0, 0;
     0, B_, 0;
     0, 0, C_];

params = struct();
params.mu = 3.98e5; % км^3/с^2
params.J = J;
params.J_inv = inv(J);
params.R = 6371; % км
params.V = sqrt(params.mu / params.R); % км/с
params.scale = 1.3;
params.w0 = sqrt(params.mu / (params.scale * params.R)^3); % с^-1

%%Initializing
dt = 1e1;
T =10000;
t = 0:dt:T; %%start:step:end
N = length(t);

r = zeros(3, N);
v = zeros(3, N);
Q = zeros(N, 4);
w = zeros(3, N);
wabs = zeros(3, N);
A0 = zeros(3, 3, N); % ОСК -> ИСК

r_init = params.R * [0.0, params.scale, 0.0]'; % ИСК
v_init = params.V * [-1/sqrt(params.scale), 0.0, 0.0]'; % ИСК
A0(:, 3, 1) = normalized(r_init);
A0(:, 2, 1) = normalized(cross(r_init, v_init));
A0(:, 1, 1) = cross(A0(:, 2, 1), A0(:, 3, 1));

incl_init = deg2rad(0);
rotvect = normalized([0 1 0])'; % ОСК
Q_init = quatnormalize([cos(incl_init/2), sin(incl_init/2)*(A0(:,:,1)*rotvect).']); % Из ССК в ИСК
D_init = quat2dcm(Q_init); % Из ССК в ИСК
w_init = 0e-4 * [0.3, -0.2, 0.8]'; % Относительная угловая скорость (ССК относительно ОСК), ССК

r(:, 1) = r_init;
v(:, 1) = v_init;
Q(1, :) = Q_init;
w(:, 1) = w_init;

%% Integration
for i = 1:3
    for j = 1:3, j~=i;
        for isign = -1:2:1
            for jsign = -1:2:1
                e1 = [0 0 0];
                e2 = [0 0 0];
                e1(i) = isign;
                e2(j) = jsign;
                e3 = cross(e1, e2);
                Drel = [e1; e2; e3]; % ССК -> ОСК
                eps = 1e-1;
                sigma = 1e-5;
                R = chol(sigma);
                w_init = randn(1,3)*R;
                wabs_init = w_init + params.w0 * D_init * normalized(cross(r_init, v_init)); % Абсолютная угловая скорость (ССК относительно ИСК), ССК
                wabs(:, 1) = wabs_init;
                dq = randn(3,1)*R;
                dQ = quatnormalize(cat(1, sqrt(1 - norm(dq)^2), dq)');
                Q_init = dcm2quat(Drel);
                Q = quatmultiply(dQ, Q_init);
                for k = 1:N - 1
                    ret = integrator(@GravMoment, [r(:, k)', v(:, k)', Q, wabs(:, k)'], t(i), dt, params);
                    Q = ret(1:4);
                    wrel = ret(5:7);
                    unstable = false;
                    dQ_n = quatdivide(Q, Q_init);
                    if norm(wrel) > eps || norm(dQ_n(2:4)) > eps
                        disp(["eps ", eps])
                        disp(["wrel ", norm(wrel)])
                        disp(["dq", norm(dQ_n(2:4))])
                        unstable = true;
                        break
                    end
                end
                if unstable
                    disp(["i = ", isign*i, "j = ", jsign*j, " - unstable, t = ", k * dt])
                else
                    disp(["i = ", isign*i, "j = ", jsign*j, " - stable, for t = ", T])
                end
            end
        end
    end
end