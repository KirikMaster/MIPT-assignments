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
params.m = 0.01;
params.l = 1;
params.J = J;
params.J_inv = inv(J);
params.scenario = "Lagrange";

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
K1i = zeros(3, N);
E1 = zeros(1, N);
phi1 = zeros(1, N);
costheta1 = zeros(1, N);
theta1 = zeros(1, N);
x1 = repmat(xl, 1, N);
zl1 = repmat(Oz, 1, N);
for i = 1:N
    w1i(:,i) = A(:,:,i).' * w1(:, i);
    x1(:,i) = A(:,:,i).' * x1(:,i);
    zl1(:,i) = A(:,:,i) * zl1(:,i);
    phi1(i) = atan2(-dot(x1(:,i), Oy), -dot(x1(:,i), Ox)) + pi;
    theta1(i) = asin(dot(x1(:,i), Oz));
    K1(:,i) = J * w1(:, i);
    K1i(:, i) = A(:,:,i).' * K1(:, i);
    E1(i) = dot(w1(:,i), J * w1(:, i))/2 + params.m * norm(params.g) * params.l * sin(theta1(i));
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
K2i = zeros(3, N);
E2 = zeros(1, N);
phi2 = zeros(1, N);
costheta2 = zeros(1, N);
theta2 = zeros(1, N);
x2 = repmat(xl, 1, N);
zl2 = repmat(Oz, 1, N);
for i = 1:N
    w2i(:,i) = A2(:,:,i).' * w2(:, i);
    x2(:,i) = A2(:,:,i).' * x2(:,i);
    zl2(:,i) = A2(:,:,i) * zl2(:,i);
    phi2(i) = atan2(-dot(x2(:,i), Oy), -dot(x2(:,i), Ox)) + pi;
    theta2(i) = asin(dot(x2(:,i), Oz));
    K2(:,i) = J * w2(:, i);
    K2i(:, i) = A2(:,:,i).' * K2(:, i);
    E2(i) = dot(w2(:,i), J * w2(:, i))/2 + params.m * norm(params.g) * params.l * sin(theta2(i));
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
K3i = zeros(3, N);
E3 = zeros(1, N);
phi3 = zeros(1, N);
costheta3 = zeros(1, N);
theta3 = zeros(1, N);
x3 = repmat(xl, 1, N);
zl3 = repmat(Oz, 1, N);
for i = 1:N
    temp = quatmultiply(quatconj(Q(:, i).'), quatmultiply(cat(1, 0, w3(:, i)).', Q(:, i).'));
    w3i(:,i) = temp(2:4);
    temp = quatmultiply(Q(:, i).', quatmultiply(cat(1, 0, x3(:, i)).', quatconj(Q(:, i).')));
    x3(:,i) = temp(2:4);
    zl3(:,i) = quat2dcm(Q(:,i).') * zl3(:,i);
    phi3(i) = atan2(-dot(x3(:,i), Oy), -dot(x3(:,i), Ox)) + pi;
    theta3(i) = asin(dot(x3(:,i), Oz));
    K3(:,i) = J * w3(:, i);
    K3i(:, i) = quat2dcm(Q(:, i).').' * K3(:, i);
    E3(i) = dot(w3(:,i), J * w3(:, i))/2 + params.m * norm(params.g) * params.l * sin(theta3(i));
end 

%% Graphics
close all

phase = figure("Name", "Angle and angular speed in time");
phase.Position = [0, 0, 1120, 840];subplot(2,3,1)
hold on
grid on
title('Angle of the body in XY plane')
xlabel('time, seconds')
ylabel('angle, rad')
plot(t, rad2deg(phi1) + 360, "blue", LineWidth=3.0);
plot(t, rad2deg(phi2) + 360, "red", LineWidth=1.5);
plot(t, rad2deg(phi3) + 360, "yellow");
legend('MoGC', 'Euler Angles', 'Quaternions')

subplot(2,3,4)
hold on
grid on
start = 5;
finish = 6000*dt;
title(string(['Difference of angles (', int2str(start * dt), ' - ', int2str(finish * dt), ' sec)']))
xlabel('time, seconds')
ylabel('angle, rad')
plot(t(start:finish), rad2deg(phi1(start:finish) - phi2(start:finish)), "blue");
plot(t(start:finish), rad2deg(phi2(start:finish) - phi3(start:finish)), "red");
plot(t(start:finish), rad2deg(phi3(start:finish) - phi1(start:finish)), "yellow");
legend('MoGC - EA', 'EA - Quat', 'Quat - MoGC')

subplot(2,3,2)
hold on
grid on
title('Angle of inclination')
xlabel('time, seconds')
ylabel('angle, rad')
plot(t, rad2deg(theta1), "blue", LineWidth=3.0);
plot(t, rad2deg(theta2), "red", LineWidth=1.5);
plot(t, rad2deg(theta3), "yellow");
legend('MoGC', 'Euler Angles', 'Quaternions')

subplot(2,3,5)
hold on
grid on
title('Difference of inclination angles')
xlabel('time, seconds')
ylabel('angle, rad')
plot(t, rad2deg(theta1 - theta2), "blue");
plot(t, rad2deg(theta2 - theta3), "red");
plot(t, rad2deg(theta3 - theta1), "yellow");
legend('MoGC - EA', 'EA - Quat', 'Quat - MoGC')

subplot(2,3,3)
hold on
grid on
title('Angular Speed')
xlabel('time, seconds')
ylabel('angle, rad')
plot(t, w1, LineWidth=3.0);
plot(t, w2, LineWidth=1.5);
plot(t, w3);
legend('wx, MoGC', 'wy, MoGC', 'wz, MoGC', 'wx, Euler A.', 'wy, Euler A.', ...
    'wz, Euler A.', 'wx, Quats', 'wy, Quats', 'wz, Quats');

subplot(2,3,6)
hold on
grid on
title('Difference of angular speeds')
xlabel('time, seconds')
ylabel('angle, rad')
plot(t, w1 - w2);
plot(t, w2 - w3);
plot(t, w3 - w1);
legend('wx, MoGC - EA', 'wy, MoGC - EA', 'wz, MoGC - EA', 'wx, EA - Quat', 'wy, EA - Quat', ...
    'wz, EA - Quat', 'wx, Quat - MoGC', 'wy, Quat - MoGC', 'wz, Quat - MoGC');

KM = figure("Name", "First integrals: Kinetic moment");
KM.Position(1:2) = [1000, 0];
subplot(2,1,1);
hold on
grid on
title('K*Oz')
xlabel('time, seconds')
ylabel('Angular moment, kg*m^2/s')
plot(t, centralize(dot(K1i, repmat(Oz, 1, N))), LineWidth=3.0);
plot(t, centralize(dot(K2i, repmat(Oz, 1, N))), LineWidth=1.5);
plot(t, centralize(dot(K3i, repmat(Oz, 1, N))));
legend('MoGC', 'Euler Angles', 'Quaternions')

subplot(2,1,2);
hold on
grid on
title('K*e3')
xlabel('time, seconds')
ylabel('Angular moment, kg*m^2/s')
plot(t, centralize(dot(K1, zl1)), LineWidth=3.0);
plot(t, centralize(dot(K2, zl2)), LineWidth=1.5);
plot(t, centralize(dot(K3, zl3)));
legend('MoGC', 'Euler Angles', 'Quaternions')

Enfig = figure("Name", "First integrals: Energy");
Enfig.Position(1:2) = [1000, 450];
hold on
grid on
title('First_integrals: Energy')
xlabel('time, seconds')
ylabel('energy, J')
plot(t, centralize(E1), "blue", LineWidth=3.0);
plot(t, centralize(E2), "red", LineWidth=1.5);
plot(t, centralize(E3), "yellow");
legend('MoGC', 'Euler Angles', 'Quaternions')

figure("Name", "3D modeling")
hold on
[X, Y, Z] = sphere(18);
mesh(0.9*X,0.9*Y,0.9*Z)
C = cat(1, linspace(0.0, 1.0, N), zeros(1,N), linspace(0.8,0.5, N));
scatter3(x3(1, :), x3(2, :), x3(3, :), [], C', "filled")
%scatter3(x2(1, :), x2(2, :), x2(3, :), [], winter(N), "filled")
quiver3(0, 0, 0, w(1), w(2), w(3), 1.1/norm(w), LineWidth=2.0, Color='black')
%legend('', 'Quat', 'Euler', 'w(t = 0)')
axis equal