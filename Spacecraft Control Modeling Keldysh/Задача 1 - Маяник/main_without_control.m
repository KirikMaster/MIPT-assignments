clc
clear all
close all

dt = 1e-4;
t = 0:dt:10; %%start:step:end
N = length(t);
x = zeros(2, N);
regime = "None";

step_wo_deterination = 10;
step_wo_control = 10;

%%initial condition
x(1, 1) = pi/3;
x(2, 1) = 1;

%%parameters
params = struct();
params.m = 5;
params.l = 0.5;
params.g = 9.8;
params.k1 = 0.1;
params.k2 = 2;
params.k3 = 3;
params.k4 = params.k1/params.k2;
%%
%%integration
for i = 1:N - 1
    x(:, i + 1) = integrator(x(:, i), t(i), regime, dt, nan, params);
end
%%
%%graphics
close all

figure
subplot(2,1,1);
hold on
grid on
title('Phase variables by time')
xlabel('time, seconds')
ylabel('angle, rad')
plot(t, x(1, :));

subplot(2,1,2);
hold on
grid on
xlabel('time, seconds')
ylabel('velocity, rad/s')
plot(t, x(2, :));

figure
hold on
grid on
title('Trajectory')
xlabel('x, m')
ylabel('y, m')
axis([-params.l params.l 0 2*params.l])
plot(params.l*sin(x(1, :)), params.l*(1-cos(x(1, :))));

%%first integral

energy = zeros(1, N);
for i = 1:N
    energy(i) = params.m*params.l^2*x(2, i)^2/2 + params.m*params.g*params.l*(1-cos(x(1, i)));
end

figure
hold on
grid on
title('Complete mechanical energy by time')
xlabel('time, seconds')
ylabel('energy, Joules')
plot(t, energy - energy(1), '-r', 'LineWidth', 2);