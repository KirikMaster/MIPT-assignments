%% Setup
clc
clear all
close all

%%parameters
A_ = 1.0;
B_ = 1.0;
C_ = 1.0;
J = [A_, 0, 0;
     0, B_, 0;
     0, 0, C_];

params = struct();
params.g = [0, 0, -9.8]';
params.m = 3;
params.l = 1;
params.J = J;
params.J_inv = inv(J);
params.scenario = "Euler";

Ox = [1.0, 0.0, 0.0]';
Oy = [0.0, 1.0, 0.0]';
Oz = [0.0, 0.0, 1.0]';

%%Initializing
xl = [0 0 params.l]';
incl_init = deg2rad(60);
e_start = Oy;
Q_init = quatnormalize(cat(1, cos(incl_init/2), sin(incl_init/2)*e_start)');
x = quat2dcm(Q_init).' * xl; % A = quat2dcm(Q)
w = [0.3, -0.2, 0.8]';       % A'= quat2dcm(Q)'

dt = 1e-3;
t = 0:dt:20; %%start:step:end
N = length(t);

%% Matrixes of Guiding (Directing) Cosines
A = zeros(3, 3, N);
w1 = zeros(3, N);
A(:,:,1) = quat2dcm(Q_init);
w1(:,1) = A(:,:,1) * w;

%%Integration
for i = 1:N - 1
    ret = integrator(@MoGC, [A(:,:,i), w1(:,i)], t(i), dt, params);
    A(:,:,i+1) = ret(1:3, 1:3);
    w1(:, i+1) = ret(:, 4);
end

%%FirsrtIntegrals and other
w1i = zeros(3, N);
K1 = zeros(3, N);
Knorm1 = zeros(1, N);
E1 = zeros(1, N);
phi1 = zeros(1, N);
x1 = repmat(xl, 1, N);
for i = 1:N
    w1i(:,i) = A(:,:,i).' * w1(:, i);
    x1(:,i) = A(:,:,i).' * x1(:,i);
    phi1(i) = atan2(-dot(x1(:,i), Oy), -dot(x1(:,i), Ox)) + pi;
    K1(:,i) = A(:,:,i).' * J * w1(:, i);
    Knorm1(i) = norm(K1(:,i));
    E1(i) = dot(w1(:,i), J * w1(:, i))/2;
end

%% Euler angles
A2 = zeros(3, 3, N);
w2 = zeros(3,N);
A2(:, :, 1) = quat2dcm(Q_init);
w2(:, 1) = A2(:, :, 1) * w;
psi = zeros(1, N);
theta = zeros(1, N);
phi = zeros(1, N);
[psi(1), theta(1), phi(1)] = quat2angle(Q_init, "XZX");
Y2 = cat(1, psi, theta, phi, w2);

%%Integration
for i = 1:N - 1
    Y2(:, i+1) = integrator(@EulerAngles, Y2(:, i), t(i), dt, params);
    psi(i+1) = Y2(1, i);
    theta(i+1) = Y2(2, i);
    phi(i+1) = Y2(3, i);
    w2(:, i+1) = Y2(4:6, i);
    A2(:, :, i+1) = EulerMatrix(psi(i+1), theta(i+1), phi(i+1)).';
end

%%First integrals and other
w2i = zeros(3, N);
K2 = zeros(3, N);
Knorm2 = zeros(1, N);
E2 = zeros(1, N);
phi2 = zeros(1, N);
x2 = repmat(xl, 1, N);
angles_dot = zeros(3, N);
temp2 = zeros(6, 1);
for i = 1:N
    temp2 = EulerAngles(Y2(:, i), t(i), params);
    angles_dot(:, i) = temp2(1:3)';

    w2i(:,i) = A2(:,:,i).' * w2(:, i);
    x2(:,i) = A2(:,:,i).' * x2(:,i);
    phi2(i) = atan2(-dot(x2(:,i), Oy), -dot(x2(:,i), Ox)) + pi;
    K2(:,i) = A2(:,:,i).' * J * w2(:, i);
    Knorm2(i) = norm(K2(:,i));
    E2(i) = dot(w2(:,i), J * w2(:, i))/2;
end

%% Quaternions
Q = zeros(4, N);
w3 = zeros(3, N);
Q(:, 1) = Q_init;
temp = quatmultiply(quatconj(Q(:, 1).'), quatmultiply(cat(1, 0, w).', Q(:, 1).'));
w3(:, 1) = temp(2:4);

%%Integration
for i = 1:N - 1
    ret = integrator(@Quaternions, cat(1, Q(:, i), w3(:, i)), t(i), dt, params);
    Q(:,i+1) = ret(1:4);
    w3(:,i+1) = ret(5:7);
end

%%First integrals and other
w3i = zeros(3, N);
K3 = zeros(3, N);
Knorm3 = zeros(1, N);
E3 = zeros(1, N);
phi3 = zeros(1, N);
x3 = repmat(xl, 1, N);
for i = 1:N
    temp = quatmultiply(quatconj(Q(:, i).'), quatmultiply(cat(1, 0, w3(:, i)).', Q(:, i).'));
    w3i(:,i) = temp(2:4);
    temp = quatmultiply(Q(:, i).', quatmultiply(cat(1, 0, x3(:, i)).', quatconj(Q(:, i).')));
    x3(:,i) = temp(2:4);
    phi3(i) = atan2(-dot(x3(:,i), Oy), -dot(x3(:,i), Ox)) + pi;
    K3(:,i) = quat2dcm(Q(:, i).').' * J * w3(:, i);
    Knorm3(i) = norm(K3(:,i));
    E3(i) = dot(w3(:,i), J * w3(:, i))/2;
end 

%% Graphics
close all

phase = figure("Name", "Angle and angular speed in time");
phase.Position = [0, 0, 1120, 840];
subplot(2,2,1)
hold on
grid on
title('Angle of the body in XY plane')
xlabel('time, seconds')
ylabel('angle, deg')
plot(t, rad2deg(phi1), "blue", LineWidth=3.0);
plot(t, rad2deg(phi2), "red", LineWidth=1.5);
plot(t, rad2deg(phi3), "yellow");
legend('MoGC', 'Euler Angles', 'Quaternions')

subplot(2,2,2)
hold on
grid on
start = 5;
finish = 700;
title(string(['Difference of angles (', int2str(start * dt), ' - ', int2str(finish * dt), ' sec)']))
xlabel('time, seconds')
ylabel('angle, rad')
plot(t(start:finish), phi1(start:finish) - phi2(start:finish), "blue");
plot(t(start:finish), phi2(start:finish) - phi3(start:finish), "red");
plot(t(start:finish), phi3(start:finish) - phi1(start:finish), "yellow");
legend('MoGC - EA', 'EA - Quat', 'Quat - MoGC')

subplot(2,2,3)
hold on
grid on
title('Angular Speed')
xlabel('time, seconds')
ylabel('w, rad/s')
plot(t, w1, LineWidth=3.0);
plot(t, w2, LineWidth=1.5);
plot(t, w3);
legend('wx, MoGC', 'wy, MoGC', 'wz, MoGC', 'wx, Euler A.', 'wy, Euler A.', ...
    'wz, Euler A.', 'wx, Quats', 'wy, Quats', 'wz, Quats');

subplot(2,2,4)
hold on
grid on
title('Difference of angular speeds')
xlabel('time, seconds')
ylabel('Δw')
plot(t, w1 - w2);
plot(t, w2 - w3);
plot(t, w3 - w1);
legend('wx, MoGC - EA', 'wy, MoGC - EA', 'wz, MoGC - EA', 'wx, EA - Quat', 'wy, EA - Quat', ...
    'wz, EA - Quat', 'wx, Quat - MoGC', 'wy, Quat - MoGC', 'wz, Quat - MoGC');

KM = figure("Name", "First integrals: Kinetic moment");
KM.Position(1:2) = [1000, 0];
subplot(2,2,1);
hold on
grid on
title('Kx')
xlabel('time, seconds')
ylabel('Angular moment, kg*m^2/s')
plot(t, centralize(K1(1, :)), LineWidth=3.0);
plot(t, centralize(K2(1, :)), LineWidth=1.5);
plot(t, centralize(K3(1, :)));
legend('MoGC', 'Euler Angles', 'Quaternions')

subplot(2,2,2);
hold on
grid on
title('Ky')
xlabel('time, seconds')
ylabel('Angular moment, kg*m^2/s')
plot(t, centralize(K1(2, :)), LineWidth=3.0);
plot(t, centralize(K2(2, :)), LineWidth=1.5);
plot(t, centralize(K3(2, :)));
legend('MoGC', 'Euler Angles', 'Quaternions')

subplot(2,2,3);
hold on
grid on
title('Kz')
xlabel('time, seconds')
ylabel('Angular moment, kg*m^2/s')
plot(t, centralize(K1(3, :)), LineWidth=3.0);
plot(t, centralize(K2(3, :)), LineWidth=1.5);
plot(t, centralize(K3(3, :)));
legend('MoGC', 'Euler Angles', 'Quaternions')

subplot(2,2,4);
hold on
grid on
title('norm(K)')
xlabel('time, seconds')
ylabel('Angular moment, kg*m^2/s')
plot(t, centralize(Knorm1), LineWidth=3.0);
plot(t, centralize(Knorm2), LineWidth=1.5);
plot(t, centralize(Knorm3));
legend('MoGC', 'Euler Angles', 'Quaternions')

Enfig = figure("Name", "First integrals: Energy");
Enfig.Position(1:2) = [1000, 450];
hold on
grid on
title('First_integrals: Energy')
xlabel('time, seconds')
ylabel('energy, J')
plot(t, centralize(E1), "blue", LineWidth=1.5);
plot(t, centralize(E2), "red");
plot(t, centralize(E3), "yellow");
legend('MoGC', 'Euler Angles', 'Quaternions')

figure("Name", "3D modeling")
hold on
[X, Y, Z] = sphere;
mesh(0.9*params.l*X,0.9*params.l*Y,0.9*params.l*Z)
C = cat(1, linspace(0.0, 1.0, N), zeros(1,N), linspace(0.8,0.5, N));
scatter3(x3(1, :), x3(2, :), x3(3, :), [], C', "filled")
%scatter3(x2(1, :), x2(2, :), x2(3, :), [], winter(N), "filled")
quiver3(0, 0, 0, w(1), w(2), w(3), 1.1/norm(w), LineWidth=2.0, Color='black')
%quiver3(0, 0, 0, xl(1), xl(2), xl(3), 1.1/norm(w), LineWidth=2.0, Color='red')
%legend('', 'Кватернион', 'Углы Эйлера', 'Начальный вектор угловой скорости')
axis equal

if A_ == B_
    figure("Name", "Axis-symmetric body")
    hold on
    grid on
    title('Check of results for axis-symmetric body')
    xlabel('time, seconds')
    ylabel('angular velocity, s^-1')
    plot(t, angles_dot)
    plot(t, theta)
    legend('psi', 'theta', 'phi')
end