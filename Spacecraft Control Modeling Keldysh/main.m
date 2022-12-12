clc
clear all
close all

dt = 0.001;
t = 0:dt:100; %%start:step:end
N = length(t);
x = zeros(2, N);

step_wo_deterination = 10;
step_wo_control = 10;

%%initial condition
x(1, 1) = 0;
x(2, 1) = 1;

params = struct();
params.m = 5;
params.c = 4;
params.k1 = 0.1;
params.k2 = 2;

%%integration
it4det = step_wo_deterination;
it4ctrl = step_wo_control;
control = 0;
x_meas = [0; 0];
sigma_r = 0.01;
sigma_v = 0.05;
sigma_matrix = diag ([sigma_r, sigma_v]);

for i = 1:N - 1
    if it4det < 1
        x_meas = x(:, i) + sigma_matrix*randn(2, 1);
        it4det = step_wo_deterination;
    else
        it4det = it4det - 1;
    end
    
    if it4ctrl < 1
        x_ref = getRefMotion(t, params);
        control = getCtrlPD(x_meas, x_ref, params);
        it4ctrl = step_wo_control;
    else
        it4ctrl = it4ctrl - 1;
    end
        
    k1 = rightSideCtrl(x(:, i), t(i), params, control);
    k2 = rightSideCtrl(x(:, i) + dt/2*k1, t(i) + dt/2, params, control);
    k3 = rightSideCtrl(x(:, i) + dt/2*k2, t(i) + dt/2, params, control);
    k4 = rightSideCtrl(x(:, i) + dt*k3, t(i) + dt/2, params, control);
    x(:, i + 1) = x(:, i) +  dt/6*(k1 + 2*k2 + 2*k3 + k4);
end

figure
hold on
grid on
xlabel('time, seconds')
ylabel('velocity, m/s')
plot(t, x(2, :), '-b');
plot(t, x(1, :), '-r');

x_ideal = zeros(2, N);
omega = sqrt(params.c/params.m);
A = x(2, 1)/omega;
B = x(1, 1);
for i = 1:N
    x_ideal(:, i) = [A*sin(omega*t(i)) + B*cos(omega*t(i));
                     A*omega*cos(omega*t(i)) - B*omega*sin(omega*t(i))];
end

delta_x = x - x_ideal;

figure
hold on
grid on
plot(t, delta_x(1,:), '-r', 'LineWidth', 2);
plot(t, delta_x(2,:), '-b', 'LineWidth', 2);

%%first integral

energy = zeros(1, N);
for i = 1:N
    energy(i) = params.m*x(2, i)^2/2 + params.c*x(1, i)^2/2;
end

figure
hold on
grid on
plot(t, energy - energy(1), '-r', 'LineWidth', 2);