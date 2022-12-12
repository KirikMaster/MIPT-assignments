clc
clear all
close all

dt = 1e-3;
t = 0:dt:200; %%start:step:end
N = length(t);
x = zeros(2, N);
regime = "Control";

step_wo_deterination = 10;
step_wo_control = 10;

%%initial condition
x(1, 1) = 0;
x(2, 1) = 1;

%%parameters
params = struct();
params.m = 5;
params.l = 0.5;
params.g = 9.8;
params.k1 = 1;
params.k2 = 2;
params.k3 = 3;
params.k4 = params.k1/params.k2;
%%
%%integration
sigma_r = 0.01;
sigma_v = 0.05;
sigma_matrix = 0*diag([sigma_r, sigma_v]);
it4det = step_wo_deterination;
it4ctrl = step_wo_control;
x_meas = [0, 0];
control = 0;

for i = 1:N - 1
    if it4det < 1
        x_meas = x(:, i) + sigma_matrix*randn(2, 1);
        it4det = step_wo_deterination;
    else
        it4det = it4det - 1;
    end
    
    if it4ctrl < 1
        x_ref = getRefMotion(t(i), params);
        control = getControl(x_meas, x_ref, params);
        it4ctrl = step_wo_control;
    else
        it4ctrl = it4ctrl - 1;
    end
    x(:, i + 1) = integrator(x(:, i), t(i), regime, dt, control, params);
end
%%
%%graphics
close all

figure
subplot(2,1,1);
hold on
grid on
title('Phase variables by time')
text(max(t) * 0.6, max(x(1, :)) * 0.8, strcat('deterination step = ', num2str(step_wo_deterination)))
text(max(t) * 0.6, max(x(1, :)) * 0.6, strcat('control step = ', num2str(step_wo_control)))
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