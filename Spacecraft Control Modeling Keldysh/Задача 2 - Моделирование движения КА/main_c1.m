%% Setup
clc
clear all
close all

%%parameters
A_ = 1.0;
B_ = 2.3;
C_ = 5.6;
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
params.w0 = params.mu / (params.scale * params.R)^3; % с^-1

%%Initializing
dt = 1e1;
T = 4000;
t = 0:dt:T; %%start:step:end
N = length(t);

r = zeros(3, N);
v = zeros(3, N);
Q = zeros(N, 4);
w = zeros(3, N);
A0 = zeros(3, 3, N); % ОСК -> ИСК

r_init = params.R * [0.0, params.scale, 0.0]'; % ИСК
%v_init = params.V * [-1/sqrt(params.scale), 0.0, 0.0]'; % ИСК
v_init = params.V * [-1/sqrt(2*params.scale), 0.0, 1/sqrt(2*params.scale)]'; % ИСК
A0(:, 3, 1) = normalized(r_init);
A0(:, 2, 1) = normalized(cross(r_init, v_init));
A0(:, 1, 1) = cross(A0(:, 2, 1), A0(:, 3, 1));
temp = A0(:, :, 1);
incl_init = deg2rad(30);
rotvect = normalized([0 1 0])'; % ОСК
Q_init = quatnormalize(cat(1, cos(incl_init/2), sin(incl_init/2)*rotvect)'); % Из ССК в ОСК
w_init = 0e-4 * [0.3, -0.2, 0.8]'; % Относительная угловая скорость (ССК относительно ОСК), ССК
%w_init = params.w0 * [0 1 0];

r(:, 1) = r_init;
v(:, 1) = v_init;
Q(1, :) = Q_init;
w(:, 1) = w_init;

%% Integration
for i = 1:N - 1
    ret = integrator(@GravMoment, [r(:, i)', v(:, i)', Q(i, :), w(:,i)'], t(i), dt, params);
    r(:, i+1) = ret(1:3)'; % ИСК
    v(:, i+1) = ret(4:6)'; % ИСК
    Q(i+1, :) = ret(7:10); % ССК -> ОСК
    w(:, i+1) = ret(11:13)'; % ССК
    A0(:, 3, i+1) = normalized(r(:, i+1)); % ОСК -> ИСК
    A0(:, 2, i+1) = normalized(cross(r(:, i+1), v(:, i+1)));
    A0(:, 1, i+1) = cross(A0(:, 2, i+1), A0(:, 3, i+1));
end

%%First integrals and other
RF = repmat(eye(3), 1, 1, N); % Relative Frame - Связанная СК
w0 = zeros(1, N);
wabs = zeros(3, N);
Jacobi = zeros(1, N);
Jacobi2 = zeros(1, N);
Moment = zeros(3, N);
F1 = zeros(1, N);
F2 = zeros(1, N);
F3 = zeros(1, N);
for i = 1:N
    Drel = quat2dcm(Q(i, :)); % ССК -> ОСК
    D = A0(:,:,i) * Drel; % ССК -> ИСК
    RF(:,:,i) = D * RF(:,:,i);
    E2 = Drel.' * [0 1 0]'; % E2, ССК
    E3 = Drel.' * [0 0 1]'; % E3, ССК
    wabs(:, i) = w(:, i) + w0(i) * Drel.' * [0 1 0]';
    w0(i) = sqrt(params.mu / norm(r(:, i))^3);
    Jacobi(i) = (0.5 * dot(wabs(:, i), J * wabs(:, i)) - 1.5 * w0(i)^2 * dot(E3, J * E3) - ...
        0* w0(i) * dot(E2, J * wabs(:, i)));
    F1(i) = 0.5 * dot(wabs(:, i), J * wabs(:, i));
    F2(i) = 1.5 * w0(i)^2 * dot(E3, J * E3);
    F3(i) = w0(i) * dot(E2, J * wabs(:, i));
    Jacobi2(i) = (0.5 * dot(w(:, i), J * w(:, i)) + 1.5 * w0(i)^2 * dot(E3, J * E3) - ...
        0.5 * w0(i) * dot(E2, J * E2));
    %Moment(:,i) = 3*w0(i)^2 * cross(A0(:, 3, i), J*A0(:, 3, i)); 
    Moment(:,i) = 3*w0(i)^2 * D * (cross(Drel.' * [0 0 1]', J * Drel.' * [0 0 1]')); % ИСК
end

A0 = permute(A0, [1 3 2]);
RF = permute(RF, [1 3 2]); 

%% Graphics
close all

Kin = figure("Name", "Kinematics");
hold on
Kin.Position(1:2) = [1000, 400];
xlabel('time, seconds')
ylabel('w, seconds^{-1}')
plot(t, w, Visible="on", LineStyle="-");
plot(t, w0.* RF(:, :, 2), LineStyle="--");
plot(t, wabs, Visible="on", LineStyle=":");
legend('w_{отн, x}', 'w_{отн, y}', 'w_{отн, z}', 'w_0 * E2_x', 'w_0 * E2_y', 'w_0 * E2_z', ...
    'w_{абс, x}', 'w_{абс, y}', 'w_{абс, z}')

Mom = figure("Name", "Moment of momentum");
Mom.Position(1:2) = [0, 0];
title('Moment of the gravitational momentum')
xlabel('time, sec')
ylabel('moment, kg*m^{2}/s')
plot(t, Moment);
legend('x', 'y', 'z')

Ja = figure("Name", "Jacobi integral");
hold on
Ja.Position(1:2) = [1000, 0];
title('Jacobi integral of angular motion')
xlabel('time, seconds')
ylabel('h')
plot(t, centralize(Jacobi), Visible="on");
plot(t, centralize(Jacobi2), Visible="off");
plot(t, F1, Visible="off");
plot(t, F2, Visible="off");
plot(t, F3, Visible="off");
legend('Jacobi', 'Jacobi2', 'F1', 'F2', 'F3')

model = figure("Name", "3D modeling");
model.Position(1:4) = [0, 0, 1000, 1000];
hold on
[X, Y, Z] = sphere;
mesh(1.0*X, 1.0*Y, 1.0*Z)
C = cat(1, linspace(0.0, 1.0, N), zeros(1,N), linspace(0.8,0.5, N));
scatter3(r(1, :)/params.R, r(2, :)/params.R, r(3, :)/params.R, [], C', "filled")

scIF = 1.2; % scale Inertial Frame
scOF1 = 1.1; % scale Orbital Frame t = 0
scOF = 1.0; % scale Orbital Frame
scRF1 = 0.7; % scale Relative Frame t = 0
scRF = 1.0; % scale Relative Frame

LWIF = 5.0; % LineWidth Inertial Frame
LWOF1 = 3.0; % LineWidth Orbital Frame t = 0
LWOF = 0.5; % LineWidth Orbital Frame
LWRF1 = 1.5; % LineWidth Relative Frame t = 0
LWRF = 0.75; % LineWidth Relative Frame
k = round(500/dt/T * N);
start = k;
% ИСК
quiver3(0, 0, 0, 1, 0, 0, scIF, LineWidth=LWIF, Color='red')
quiver3(0, 0, 0, 0, 1, 0, scIF, LineWidth=LWIF, Color='green')
quiver3(0, 0, 0, 0, 0, 1, scIF, LineWidth=LWIF, Color='blue')
text(1.2, -0.1, 0, 'X')
text(-0.1, 1.2, 0, 'Y')
text(0, 0.1, 1.2, 'Z')
% ОСК
quiver3(r(1,1)/params.R, r(2,1)/params.R, r(3,1)/params.R, A0(1,1,1), A0(2,1,1), A0(3,1,1), scOF1, LineWidth=LWOF1, Color='red')
quiver3(r(1,1)/params.R, r(2,1)/params.R, r(3,1)/params.R, A0(1,1,2), A0(2,1,2), A0(3,1,2), scOF1, LineWidth=LWOF1, Color='green')
quiver3(r(1,1)/params.R, r(2,1)/params.R, r(3,1)/params.R, A0(1,1,3), A0(2,1,3), A0(3,1,3), scOF1, LineWidth=LWOF1, Color='blue')
text(r(1,1)/params.R + scOF1 * A0(1,1,1), r(2,1)/params.R + scOF1 * A0(2,1,1), r(3,1)/params.R + scOF1 * A0(3,1,1) - 0.15, 'X')
text(r(1,1)/params.R + scOF1 * A0(1,1,2), r(2,1)/params.R + scOF1 * A0(2,1,2), r(3,1)/params.R + scOF1 * A0(3,1,2) + 0.15, 'Y')
text(r(1,1)/params.R + scOF1 * A0(1,1,3), r(2,1)/params.R + scOF1 * A0(2,1,3), r(3,1)/params.R + scOF1 * A0(3,1,3) - 0.15, 'Z')
quiver3(r(1,start:k:end)/params.R, r(2,start:k:end)/params.R, r(3,start:k:end)/params.R, A0(1,start:k:end,1), A0(2,start:k:end,1), A0(3,start:k:end,1), scOF, LineWidth=LWOF, Color='black', Visible='off')
quiver3(r(1,start:k:end)/params.R, r(2,start:k:end)/params.R, r(3,start:k:end)/params.R, A0(1,start:k:end,2), A0(2,start:k:end,2), A0(3,start:k:end,2), scOF, LineWidth=LWOF, Color='black', Visible='off')
quiver3(r(1,start:k:end)/params.R, r(2,start:k:end)/params.R, r(3,start:k:end)/params.R, A0(1,start:k:end,3), A0(2,start:k:end,3), A0(3,start:k:end,3), scOF, LineWidth=LWOF, Color='black', Visible='off')
% ССК
quiver3(r(1,1)/params.R, r(2,1)/params.R, r(3,1)/params.R, RF(1,1,1), RF(2,1,1), RF(3,1,1), scRF1, LineWidth=LWRF1, Color='yellow')
quiver3(r(1,1)/params.R, r(2,1)/params.R, r(3,1)/params.R, RF(1,1,2), RF(2,1,2), RF(3,1,2), scRF1, LineWidth=LWRF1, Color='yellow')
quiver3(r(1,1)/params.R, r(2,1)/params.R, r(3,1)/params.R, RF(1,1,3), RF(2,1,3), RF(3,1,3), scRF1, LineWidth=LWRF1, Color='yellow')
text(r(1,1)/params.R + scRF1 * RF(1,1,1), r(2,1)/params.R + scRF1 * RF(2,1,1), r(3,1)/params.R + scRF1 * RF(3,1,1) - 0.15, 'X')
text(r(1,1)/params.R + scRF1 * RF(1,1,2), r(2,1)/params.R + scRF1 * RF(2,1,2), r(3,1)/params.R + scRF1 * RF(3,1,2) + 0.15, 'Y')
text(r(1,1)/params.R + scRF1 * RF(1,1,3), r(2,1)/params.R + scRF1 * RF(2,1,3), r(3,1)/params.R + scRF1 * RF(3,1,3) - 0.15, 'Z')
quiver3(r(1,start:k:end)/params.R, r(2,start:k:end)/params.R, r(3,start:k:end)/params.R, RF(1,start:k:end,1), RF(2,start:k:end,1), RF(3,start:k:end,1), scRF, LineWidth=LWRF, Color='blue', Visible='on')
quiver3(r(1,start:k:end)/params.R, r(2,start:k:end)/params.R, r(3,start:k:end)/params.R, RF(1,start:k:end,2), RF(2,start:k:end,2), RF(3,start:k:end,2), scRF, LineWidth=LWRF, Color='blue', Visible='on')
quiver3(r(1,start:k:end)/params.R, r(2,start:k:end)/params.R, r(3,start:k:end)/params.R, RF(1,start:k:end,3), RF(2,start:k:end,3), RF(3,start:k:end,3), scRF, LineWidth=LWRF, Color='blue', Visible='on')

quiver3(r(1,start:k:end)/params.R, r(2,start:k:end)/params.R, r(3,start:k:end)/params.R, Moment(1,start:k:end), Moment(2,start:k:end), Moment(3,start:k:end), 2.0, Color='cyan')
legend('Поверхность Земли', 'Траектория движения спутника на орбите', 'ИСК - O_x','ИСК - O_y','ИСК - O_z', 'ОСК в t = 0', '', '', ...
    'ОСК', '', '', 'ССК в t = 0', '', '', 'ССК', '', '', 'Гравитационный момент')
axis equal