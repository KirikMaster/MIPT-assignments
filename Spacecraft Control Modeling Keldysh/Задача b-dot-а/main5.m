%% Setup
clc
clear all
close all

%%Parameters
A_ = 2.0;
B_ = 3.0;
C_ = 4.0;
J = [A_, 0, 0;
     0, B_, 0;
     0, 0, C_];

params = struct();
params.mu = 3.98e5; % км^3/с^2
params.J = J;
params.J_inv = inv(J);
params.R = 6371; % км
params.V = sqrt(params.mu / params.R); % км/с
params.i = deg2rad(60);
params.scale = 1.3;
params.w0 = sqrt(params.mu / (params.scale * params.R)^3); % с^-1
params.delta = deg2rad(12);
params.lam = deg2rad(0);
params.mu0 = 7.812e6; % кг * км^3 * А^-1 * с^-2
params.B0 = params.mu0 / (params.R * params.scale)^3; % Тл
params.k = [sin(params.delta) * cos(params.lam), sin(params.delta) * sin(params.lam), cos(params.delta)]';
params.mm = 1e-2 * [0.0, 0.0, 5.0]'; % А * м^2, ССК
params.mmax = 10;
params.b_dot_ctrl = 1e7;
params.eps = params.b_dot_ctrl * params.B0^2 / C_ / params.w0;

%%Initializing
dt = 1e-1;
T =20000;
t = 0:dt:T; %%start:step:end
N = length(t);

%Kinematics
r = zeros(3, N);
v = zeros(3, N);
Q = zeros(N, 4);
w = zeros(3, N);
D = zeros(3, 3, N); % ССК -> ИСК

r_init = params.R * params.scale * normalized([0.0, 1.0, 0.0]'); % ИСК
v_init = params.V * 1/sqrt(params.scale) * normalized(-[cos(params.i), 0.0, sin(params.i)]'); % ИСК

incl_init = deg2rad(0);
rotvect = EulerMatrix(deg2rad(30), deg2rad(30), deg2rad(0)) * normalized([0 0 1]).'; % ИСК
Q_init = quatnormalize([cos(incl_init/2), sin(incl_init/2)*rotvect.']); % ИСК -> ССК
D_init = quat2dcm(Q_init); % ССК -> ИСК
w_init = 1e-2 * [3.0, -2.0, 8.0]'; % Относительная угловая скорость (ССК относительно ОСК), ССК

r(:, 1) = r_init;
v(:, 1) = v_init;
Q(1, :) = Q_init;
D(:, :, 1) = D_init;
w(:, 1) = w_init;

global mm_coil
coil = zeros(3, N);
%% Integration
data = struct();
for i = 1:N - 1
    rc = r(:, i); % ИСК
    Dc = D(:, :, i); % ССК -> ИСК
    wc = w(:, i); % ССК
    data.B = Magnetic_field(rc, params); % ИСК
    B_meas = Magnetometer(rc, Dc, params); % ССК
    data.mm_c = b_dot(wc, B_meas, params); % ССК

    ret = integrator(@Moment2, [r(:, i)', v(:, i)', Q(i, :), w(:,i)'], t(i),  dt, data, params);
    r(:, i+1) = ret(1:3)'; % ИСК
    v(:, i+1) = ret(4:6)'; % ИСК
    Q(i+1, :) = ret(7:10); % ИСК -> ССК
    w(:, i+1) = ret(11:13)'; % ССК, Абсолютная
    D(:, :, i+1) = quat2dcm(Q(i+1, :)); % ССК -> ИСК
    coil(:, i+1) = mm_coil;
end

RF = repmat(eye(3), 1, 1, N); % Relative Frame - Связанная СК
w0 = zeros(1, N);
w_nrm = zeros(1, N);
for i = 1:N
    RF(:,:,i) = D(:,:,i).' * RF(:,:,i);
    w0(i) = sqrt(params.mu / norm(r(:, i))^3);
    w_nrm(:, i) = norm(w(:, i));
end

RF = permute(RF, [1 3 2]); 

%% Graphics
close all
C = cat(1, linspace(0.0, 1.0, N), zeros(1,N), linspace(0.8,0.5, N));

fig_coil = figure;
plot(t, coil);
legend('x', 'y', 'z')

ang = figure("Name", "Angular velocity");
ang.Position(1:4) = [900, 0, 600, 600];
hold on
grid on
plot(t, w0, Visible="on")
plot(t, w, Visible="on")
legend('orbital', 'absolute - x', 'absolute - y', 'absolute - z')
xlabel("time, sec")
ylabel("w, s^-1");

model = figure("Name", "3D modeling");
model.Position(1:4) = [0, 0, 900, 700];
hold on
[X, Y, Z] = sphere;
mesh(1.0*X, 1.0*Y, 1.0*Z)

scIF = 1.2; % scale Inertial Frame
scRF1 = 0.7; % scale Relative Frame t = 0
scRF = 1.0; % scale Relative Frame

LWIF = 5.0; % LineWidth Inertial Frame
LWRF1 = 1.5; % LineWidth Relative Frame t = 0
LWRF = 0.75; % LineWidth Relative Frame
K = round(50/dt);
start = N - 50*K;
%ИСК
quiver3(0, 0, 0, 1, 0, 0, scIF, LineWidth=LWIF, Color='red')
quiver3(0, 0, 0, 0, 1, 0, scIF, LineWidth=LWIF, Color='green')
quiver3(0, 0, 0, 0, 0, 1, scIF, LineWidth=LWIF, Color='blue')
text(1.2, -0.1, 0, 'X')
text(-0.1, 1.2, 0, 'Y')
text(0, 0.1, 1.2, 'Z')
% ССК
quiver3(r(1,1)/params.R, r(2,1)/params.R, r(3,1)/params.R, RF(1,1,1), RF(2,1,1), RF(3,1,1), scRF1, LineWidth=LWRF1, Color='yellow')
quiver3(r(1,1)/params.R, r(2,1)/params.R, r(3,1)/params.R, RF(1,1,2), RF(2,1,2), RF(3,1,2), scRF1, LineWidth=LWRF1, Color='yellow')
quiver3(r(1,1)/params.R, r(2,1)/params.R, r(3,1)/params.R, RF(1,1,3), RF(2,1,3), RF(3,1,3), scRF1, LineWidth=LWRF1, Color='yellow')
text(r(1,1)/params.R + scRF1 * RF(1,1,1), r(2,1)/params.R + scRF1 * RF(2,1,1), r(3,1)/params.R + scRF1 * RF(3,1,1) - 0.15, 'X')
text(r(1,1)/params.R + scRF1 * RF(1,1,2), r(2,1)/params.R + scRF1 * RF(2,1,2), r(3,1)/params.R + scRF1 * RF(3,1,2) + 0.15, 'Y')
text(r(1,1)/params.R + scRF1 * RF(1,1,3), r(2,1)/params.R + scRF1 * RF(2,1,3), r(3,1)/params.R + scRF1 * RF(3,1,3) - 0.15, 'Z')
quiver3(r(1,start:K:end)/params.R, r(2,start:K:end)/params.R, r(3,start:K:end)/params.R, RF(1,start:K:end,1), RF(2,start:K:end,1), RF(3,start:K:end,1), scRF, LineWidth=LWRF, Color='red', Visible='on')
quiver3(r(1,start:K:end)/params.R, r(2,start:K:end)/params.R, r(3,start:K:end)/params.R, RF(1,start:K:end,2), RF(2,start:K:end,2), RF(3,start:K:end,2), scRF, LineWidth=LWRF, Color='green', Visible='on')
quiver3(r(1,start:K:end)/params.R, r(2,start:K:end)/params.R, r(3,start:K:end)/params.R, RF(1,start:K:end,3), RF(2,start:K:end,3), RF(3,start:K:end,3), scRF, LineWidth=LWRF, Color='blue', Visible='on')
%Траектория
scatter3(r(1, :)/params.R, r(2, :)/params.R, r(3, :)/params.R, [], C', "filled", Visible="on")
%Магнитное поле
scB = 1.5; % scale Magnetic Field
LWB = 6.0; % LineWidth Magnetic Field
quiver3(0, 0, 0, params.k(1), params.k(2), params.k(3), scB, LineWidth=LWB, Color='#00125f', LineStyle='-.', ShowArrowHead='off')
quiver3(0, 0, 0, -params.k(1), -params.k(2), -params.k(3), scB, LineWidth=LWB, Color='#00125f', LineStyle='-.', ShowArrowHead='off')
nfaces = 20;
[Xm, Ym, Zm] = sphere(nfaces);
Xm = params.R * params.scale * reshape(Xm, 1, []);
Ym = params.R * params.scale * reshape(Ym, 1, []);
Zm = params.R * params.scale * reshape(Zm, 1, []);
B_vect = zeros(3, (nfaces+1)^2);
for i=1:(nfaces+1)^2
    B_vect(:, i) = Magnetic_field([Xm(i), Ym(i), Zm(i)], params) / params.B0;
end
quiver3(Xm / params.R, Ym / params.R, Zm / params.R, B_vect(1, :), B_vect(2, :), B_vect(3, :));
legend('Поверхность Земли','ИСК - O_x','ИСК - O_y','ИСК - O_z', 'ССК в t = 0', '', '', 'ССК', '', '', 'Траектория движения спутника на орбите', 'Ось магнитного диполя', '', 'Векторное поле')
axis equal