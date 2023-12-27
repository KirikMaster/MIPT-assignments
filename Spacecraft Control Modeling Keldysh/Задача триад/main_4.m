%% Setup
clc
clear all
close all

%%Parameters
A_ = 1.0;
B_ = 2.3;
C_ = 3.1;
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
params.mu0 = 7.812e6; % кг * км^3 * А^-1 * с^-2
params.B0 = params.mu0 / (params.R * params.scale)^3; % Тл
params.k = [0, 0, 1];
params.mm = 1e-1 * [0.0, 0.0, 5.0]; % А * м^2, ССК

%%Initializing
dt = 1e-1;
T =4000;
t = 0:dt:T; %%start:step:end
N = length(t);

%Kinematics
r = zeros(3, N);
v = zeros(3, N);
Q = zeros(N, 4); % ИСК -> ССК
A = zeros(3, 3, N); % ИСК -> ССК
%w = zeros(3, N);
wabs = zeros(3, N);
w0 = zeros(1, N);

r_init = params.R * [0.0, params.scale, 0.0]'; % ИСК
%v_init = params.V * [-1/sqrt(params.scale), 0.0, 0.0]'; % ИСК
v_init = params.V * [-1/sqrt(2*params.scale), 0.0, 1/sqrt(2*params.scale)]'; % ИСК

incl_init = deg2rad(30);
rotvect = normalized([0 1 0])'; % ОСК
Q_init = quatnormalize([cos(incl_init/2), sin(incl_init/2)*rotvect.']); % ИСК -> ССК
A_init = quat2dcm(Q_init); % ИСК -> ССК
w_init = 0e-4 * [0.3, -0.2, 0.8]'; % Относительная угловая скорость (ССК относительно ОСК), ССК
%w_init = params.w0 * A0(:,:,1).' * [0 1 0];
wabs_init = w_init; % Абсолютная угловая скорость (ССК относительно ИСК), ССК

r(:, 1) = r_init;
v(:, 1) = v_init;
Q(1, :) = Q_init;
A(:, :, 1) = A_init;
%w(:, 1) = w_init;
wabs(:, 1) = wabs_init;

delta = deg2rad(11);
lam = deg2rad(0);
params.k = [sin(delta) * cos(lam), sin(delta) * sin(lam), cos(delta)]';

%% Sensors
%%Sun
rs_true = normalized([1, 1, 0]).'; % ИСК % Опорный вектор V1
s = zeros(3, N); % ССК % Опорный вектор W1
B = zeros(3, 3, N); % ССК -> СолСК
[s(:, 1), B(:, :, 1)] = SunSen(A_init);

%%Magnetometer
B_vect = zeros(3, N); % ИСК, безразмерный % Опорный вектор V2
B_meas = zeros(3, N); % ССК, безразмерный % Опорный вектор W2
B_vect(:, 1) = Magnetic_field(r_init, params);
B_meas(:, 1) = Magnetometer(r_init, A_init, params);

%%AVS
w_meas = zeros(3, N); % ССК
w_meas(:, 1) = AVS(wabs_init);

%%TRIAD
A_meas = zeros(3, 3, N); % ИСК -> ССК
A_meas(:, :, 1) = Create_basis(rs_true, B_vect(:, 1)) * Create_basis(s(:, 1), B_meas(:, 1)).';
Q_delta = zeros(N, 4); % ССК -> ССК_ТРИАД
Q_delta(1, :) = dcm2quat(A_meas(:, :, 1).' * A(:, :, 1));

%% Integration
for i = 1:N - 1
    ret = integrator(@Moment, [r(:, i)', v(:, i)', Q(i, :), wabs(:,i)'], t(i), dt, params);
    r(:, i+1) = ret(1:3)'; % ИСК
    v(:, i+1) = ret(4:6)'; % ИСК
    Q(i+1, :) = ret(7:10); % ССК -> ИСК
    A(:, :, i+1) = quat2dcm(Q(i+1, :)); % ССК -> ИСК
    wabs(:, i+1) = ret(11:13)'; % ССК, Абсолютная

    [s(:, i+1), B(:, :, i+1)] = SunSen(A(:, :, i+1));
    w_meas(:, i+1) = AVS(wabs(:, i+1));
    B_vect(:, i+1) = Magnetic_field(r(:, i+1), params);
    B_meas(:, i+1) = Magnetometer(r(:, i+1), A(:, :, i+1), params);
    A_meas(:, :, i+1) = Create_basis(rs_true, B_vect(:, i+1)) * Create_basis(s(:, i+1), B_meas(:, i+1)).';
    Q_delta(i+1, :) = dcm2quat(A_meas(:, :, i+1).' * A(:, :, i+1));
end

%% Graphics
close all
C = cat(1, linspace(0.0, 1.0, N), zeros(1,N), linspace(0.8,0.5, N));

sensors = figure("Name", "Sensors data");
sensors.Position(1:4) = [900, 500, 600, 300];
subplot(2, 2, 1)
plot(t, s);
title("Измерения солнечного датчика в ДСК")
xlabel('time, sec')
ylabel('sun, m')
legend('Ss_x', 'Ss_y', 'Ss_z')

subplot(2, 2, 2)
plot(t, B_meas);
title("Измерения магнитометра")
xlabel('time, sec')
ylabel('B, Tl')
legend('B_x', 'B_y', 'B_z')

subplot(2, 2, 3)
plot(t, w_meas);
title("Измерения ДУС")
xlabel('time, sec')
ylabel('w, sec^-1')
legend('w_x', 'w_y', 'w_z')

subplot(2, 2, 4)
delta_triad_vect = reshape(A - A_meas, 9, []);
plot(t, Q_delta(:, 2:4));
title("Кватернион между истинной и оцененной ориентациями")
xlabel('time, sec')
%ylabel('w, sec^-1')
legend('q1', 'q2', 'q3')

DSK = figure();
DSK.Position(1:4) = [1000, 0, 500, 400];
scatter3(s(1, :), s(2, :), s(3, :), [], C', "filled", Visible="on")

model = figure("Name", "3D modeling");
model.Position(1:4) = [0, 0, 700, 500];
hold on
[X, Y, Z] = sphere;
mesh(1.0*X, 1.0*Y, 1.0*Z)

%ИСК
scIF = 1.2; % scale Inertial Frame
LWIF = 5.0; % LineWidth Inertial Frame
quiver3(0, 0, 0, 1, 0, 0, scIF, LineWidth=LWIF, Color='red')
quiver3(0, 0, 0, 0, 1, 0, scIF, LineWidth=LWIF, Color='green')
quiver3(0, 0, 0, 0, 0, 1, scIF, LineWidth=LWIF, Color='blue')
text(1.2, -0.1, 0, 'X')
text(-0.1, 1.2, 0, 'Y')
text(0, 0.1, 1.2, 'Z')
%Траектория
scatter3(r(1, :)/params.R, r(2, :)/params.R, r(3, :)/params.R, [], C', "filled", Visible="on")
%Направление на солнце
quiver3(r(1, 1)/params.R, r(2, 1)/params.R, r(3, 1)/params.R, rs_true(1), rs_true(2), rs_true(3))
%Магнитная ось
scB = 1.5; % scale Magnetic Field
LWB = 6.0; % LineWidth Magnetic Field
quiver3(0, 0, 0, params.k(1), params.k(2), params.k(3), scB, LineWidth=LWB, Color='#00125f', LineStyle='-.', ShowArrowHead='off')
quiver3(0, 0, 0, -params.k(1), -params.k(2), -params.k(3), scB, LineWidth=LWB, Color='#00125f', LineStyle='-.', ShowArrowHead='off')
legend('Поверхность Земли','ИСК - O_x','ИСК - O_y','ИСК - O_z', 'Траектория движения спутника на орбите', 'Направление на солнце', 'Ось магнитного диполя', '')
axis equal