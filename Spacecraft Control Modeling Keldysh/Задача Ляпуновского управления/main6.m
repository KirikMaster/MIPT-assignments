%% Setup
clc
clear all
close all

global task
global Qref_init
task = 'orbital'; % orbital inertial

%%Parameters
A_ = 1.2;
B_ = 2.1;
C_ = 3.2;
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
params.delta = deg2rad(12);
params.lam = deg2rad(0);
params.mu0 = 7.812e6; % кг * км^3 * А^-1 * с^-2
params.B0 = params.mu0 / (params.R * params.scale)^3; % Тл
params.k = [sin(params.delta) * cos(params.lam), sin(params.delta) * sin(params.lam), cos(params.delta)]';
params.mm = 1e-2 * [0.0, 0.0, 5.0]'; % А * м^2, ССК

%%Initializing
dt = 1e0;
T =8000;
t = 0:dt:T; %%start:step:end
N = length(t);

%%Kinematics
r = zeros(3, N);
v = zeros(3, N);
Q = zeros(N, 4);
w = zeros(3, N);
wabs = zeros(3, N);
A0 = zeros(3, 3, N); % ИСК -> ОСК
D = zeros(3, 3, N); % ССК -> ИСК

r_init = params.R * params.scale * normalized([0.0, 1.0, 0.0]'); % ИСК
v_init = params.V * 1/sqrt(params.scale) * normalized([-1.0, 0.0, 0.0]'); % ИСК
%v_init = params.V * 1/sqrt(params.scale) * normalized([-1.0, 0.0, 0.1]'); % ИСК
A0(:, 3, 1) = normalized(r_init);
A0(:, 2, 1) = normalized(cross(r_init, v_init));
A0(:, 1, 1) = cross(A0(:, 2, 1), A0(:, 3, 1));

incl_init = deg2rad(80);
rotvect = A0(:,:,1)*normalized([0 1 0])'; % ИСК
Q_init = quatnormalize([cos(incl_init/2), sin(incl_init/2)*rotvect.']); % ИСК -> ССК
D_init = quat2dcm(Q_init); % ССК -> ИСК
w_init = 1e-4 * [3.0, -2.0, 8.0]'; % Относительная угловая скорость (ССК относительно ОСК), ССК
%w_init = params.w0 * A0(:,:,1).' * [0 1 0];
wabs_init = w_init - params.w0 * D_init * A0(:,:,1) * [0 1 0]'; % Абсолютная угловая скорость (ССК относительно ИСК), ССК

r(:, 1) = r_init;
v(:, 1) = v_init;
Q(1, :) = Q_init;
D(:, :, 1) = D_init;
w(:, 1) = w_init;
wabs(:, 1) = wabs_init;

incl_ref = deg2rad(0);
    switch task
        %Stabilization in orbital SK
        case 'orbital'
            rotvect_ref = normalized([1.0 1.0 0.0]'); % ОСК
            B = quat2dcm(quatnormalize([cos(incl_ref/2), sin(incl_ref/2)*rotvect_ref.'])); % ОСК -> ОпСК
            R = D_init.' * A0(:,:,1).' * B.';
            Q_ref = dcm2quat(R); % ОпСК -> ССК
        %Stabilization in inertial SK
        case 'inertial'
            rotvect_ref = normalized([1.0 1.0 0.0]'); % ИСК
            D_ref = quat2dcm(quatnormalize([cos(incl_ref/2), sin(incl_ref/2)*rotvect_ref.'])); % ИСК -> ОпСК
            R = D_init.' * D_ref.';
            Q_ref = dcm2quat(R); % ОпСК -> ССК
    end
    Qref_init = Q_ref;

M_ctrl = zeros(3, N);
global TMP
temp = zeros(N, 4);

%% Integration
data = struct();
for i = 1:N - 1
    rc = r(:, i); % ИСК
    Dc = D(:, :, i); % ССК -> ИСК
    A0c = A0(:, :, i); % ИСК -> ОСК
    wc = wabs(:, i); % ССК
    data.B = Magnetic_field(rc, params); % ИСК
    data.M_grav = 3*params.mu / norm(rc)^5*cross(Dc*rc, J*Dc*rc); % ССК
    data.M_magn = cross(params.mm, Dc * data.B); % ССК
    data.u = Lyapunov(rc, A0c, Dc, wc, J, data, params); % ССК
    temp(i, :) = TMP;
   
    ret = integrator(@Moment3, [r(:, i)', v(:, i)', Q(i, :), wabs(:,i)'], t(i), dt, data, params);
    r(:, i+1) = ret(1:3)'; % ИСК
    v(:, i+1) = ret(4:6)'; % ИСК
    Q(i+1, :) = ret(7:10); % ИСК -> ССК
    wabs(:, i+1) = ret(11:13)'; % ССК, Абсолютная
    A0(:, 3, i+1) = normalized(r(:, i+1)); % ОСК -> ИСК
    A0(:, 2, i+1) = normalized(cross(r(:, i+1), v(:, i+1)));
    A0(:, 1, i+1) = cross(A0(:, 2, i+1), A0(:, 3, i+1));
    D(:, :, i+1) = quat2dcm(Q(i+1, :)); % ССК -> ИСК
end

RF = repmat(eye(3), 1, 1, N); % Relative Frame - Связанная СК
w0 = zeros(1, N);
wabs_nrm = zeros(1, N);
w_nrm = zeros(1, N);
for i = 1:N
    Drel = A0(:,:,i).' * D(:,:,i).'; % ОСК -> ССК
    RF(:,:,i) = D(:,:,i).' * RF(:,:,i);
    E2 = Drel.' * [0 1 0]'; % E2, ССК
    E3 = Drel.' * [0 0 1]'; % E3, ССК
    w0(i) = sqrt(params.mu / norm(r(:, i))^3);
    w(:, i) = wabs(:, i) - w0(i) * E2; % ССК, Относительная
    wabs_nrm(:, i) = norm(wabs(:, i));
    w_nrm(:, i) = norm(w(:, i));
end

A0 = permute(A0, [1 3 2]);
RF = permute(RF, [1 3 2]); 

%% Graphics
close all
C = cat(1, linspace(0.0, 1.0, N), zeros(1,N), linspace(0.8,0.5, N));

ang = figure("Name", "Data");
ang.Position(1:4) = [900, 0, 600, 600];
subplot(2, 1, 1)
hold on
grid on
plot(t, w0, Visible="on")
plot(t, wabs, Visible="off")
plot(t, w, Visible="on")
legend('orbital', 'absolute - x', 'absolute - y', 'absolute - z', 'relative - x', 'relative - y', 'relative - z')
xlabel("time, sec")
ylabel("angular velocity w, s^-1");

subplot(2, 1, 2)
hold on
grid on
plot(t, M_ctrl, Visible="on")
xlabel("time, sec")
ylabel("control moment, N*m")
legend('M_x', 'M_y', 'M_z')

tmp = figure;
plot(t, temp(:, 1))
legend()

model = figure("Name", "3D modeling");
model.Position(1:4) = [0, 0, 900, 700];
hold on
[X, Y, Z] = sphere;
mesh(1.0*X, 1.0*Y, 1.0*Z)

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
K = round(50/dt);
start = K;
%ИСК
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
quiver3(r(1,start:K:end)/params.R, r(2,start:K:end)/params.R, r(3,start:K:end)/params.R, A0(1,start:K:end,1), A0(2,start:K:end,1), A0(3,start:K:end,1), scOF, LineWidth=LWOF, Color='black', Visible='off')
quiver3(r(1,start:K:end)/params.R, r(2,start:K:end)/params.R, r(3,start:K:end)/params.R, A0(1,start:K:end,2), A0(2,start:K:end,2), A0(3,start:K:end,2), scOF, LineWidth=LWOF, Color='black', Visible='off')
quiver3(r(1,start:K:end)/params.R, r(2,start:K:end)/params.R, r(3,start:K:end)/params.R, A0(1,start:K:end,3), A0(2,start:K:end,3), A0(3,start:K:end,3), scOF, LineWidth=LWOF, Color='black', Visible='off')
% ССК
quiver3(r(1,1)/params.R, r(2,1)/params.R, r(3,1)/params.R, RF(1,1,1), RF(2,1,1), RF(3,1,1), scRF1, LineWidth=LWRF1, Color='yellow')
quiver3(r(1,1)/params.R, r(2,1)/params.R, r(3,1)/params.R, RF(1,1,2), RF(2,1,2), RF(3,1,2), scRF1, LineWidth=LWRF1, Color='yellow')
quiver3(r(1,1)/params.R, r(2,1)/params.R, r(3,1)/params.R, RF(1,1,3), RF(2,1,3), RF(3,1,3), scRF1, LineWidth=LWRF1, Color='yellow')
text(r(1,1)/params.R + scRF1 * RF(1,1,1), r(2,1)/params.R + scRF1 * RF(2,1,1), r(3,1)/params.R + scRF1 * RF(3,1,1) - 0.15, 'X')
text(r(1,1)/params.R + scRF1 * RF(1,1,2), r(2,1)/params.R + scRF1 * RF(2,1,2), r(3,1)/params.R + scRF1 * RF(3,1,2) + 0.15, 'Y')
text(r(1,1)/params.R + scRF1 * RF(1,1,3), r(2,1)/params.R + scRF1 * RF(2,1,3), r(3,1)/params.R + scRF1 * RF(3,1,3) - 0.15, 'Z')
quiver3(r(1,start:K:end)/params.R, r(2,start:K:end)/params.R, r(3,start:K:end)/params.R, RF(1,start:K:end,1), RF(2,start:K:end,1), RF(3,start:K:end,1), scRF, LineWidth=LWRF, Color='blue', Visible='on')
quiver3(r(1,start:K:end)/params.R, r(2,start:K:end)/params.R, r(3,start:K:end)/params.R, RF(1,start:K:end,2), RF(2,start:K:end,2), RF(3,start:K:end,2), scRF, LineWidth=LWRF, Color='blue', Visible='on')
quiver3(r(1,start:K:end)/params.R, r(2,start:K:end)/params.R, r(3,start:K:end)/params.R, RF(1,start:K:end,3), RF(2,start:K:end,3), RF(3,start:K:end,3), scRF, LineWidth=LWRF, Color='blue', Visible='on')
%Траектория
scatter3(r(1, :)/params.R, r(2, :)/params.R, r(3, :)/params.R, [], C', "filled", Visible="on")
%Магнитная ось
scB = 1.5; % scale Magnetic Field
LWB = 6.0; % LineWidth Magnetic Field
quiver3(0, 0, 0, params.k(1), params.k(2), params.k(3), scB, LineWidth=LWB, Color='#00125f', LineStyle='-.', ShowArrowHead='off')
quiver3(0, 0, 0, -params.k(1), -params.k(2), -params.k(3), scB, LineWidth=LWB, Color='#00125f', LineStyle='-.', ShowArrowHead='off')
legend('Поверхность Земли','ИСК - O_x','ИСК - O_y','ИСК - O_z', 'ОСК в t = 0', '', '', 'ОСК', '', '', 'ССК в t = 0', '', '', 'ССК', '', '', 'Траектория движения спутника на орбите', 'Ось магнитного диполя', '')
axis equal