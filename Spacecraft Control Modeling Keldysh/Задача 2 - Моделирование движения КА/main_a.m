clc
clear all
close all

%%parameters
params = struct();
params.mu = 3.98e5; % км^3/с^2
params.J2 = 0.0010827;
params.R = 6371; % км
params.V = sqrt(params.mu / params.R); % км/с
params.alpha = params.mu * params.J2 * params.R^2 / 2;
params.j2 = false;

dt = 1e-1;
t = 0:dt:24000; %%start:step:end
N = length(t);
x = zeros(6, N);
xj2 = zeros(6, N);
r = zeros(1, N);
rj2 = zeros(1, N);
v = zeros(1, N);
vj2 = zeros(1, N);

%%initial condition
x(1, 1) = 1.0 * params.R;
x(2, 1) = 0.0 * params.R;
x(3, 1) = 0.0 * params.R;
x(4, 1) = 0.0 * params.V;
x(5, 1) = 1.1 * params.V;
x(6, 1) = 0.1 * params.V;
r(1) = norm(x(1:3, 1));
v(1) = norm(x(4:6, 1));

xj2 = x;
rj2 = r;
vj2 = v;

%% integration
% Central Newton Gravity Field
for i = 1:N - 1
    x(:, i + 1) = integrator(@CentralNewtonOrbit, x(:, i), t(i), dt, params);
    r(i + 1) = norm(x(1:3, i+1));
    v(i + 1) = norm(x(4:6, i+1));
end
%%integrals
h_int = zeros(1, N);
c_int = zeros(3, N);
f_int = zeros(3, N);
for i = 1:N
    h_int(:, i) = h_integral(x(:, i), params);
    c_int(:, i) = c_integral(x(:, i), params);
    f_int(:, i) = f_integral(x(:, i), params);
end
h_int = h_int - h_int(1);
c_int = c_int - c_int(:, 1);
f_int = f_int - f_int(:, 1);
% Gravity Field with J2
params.j2 = true;
for i = 1:N - 1
    xj2(:, i + 1) = integrator(@CentralNewtonOrbit, xj2(:, i), t(i), dt, params);
    rj2(i + 1) = norm(xj2(1:3, i+1));
    vj2(i + 1) = norm(xj2(4:6, i+1));
end

%% Osculating elements
oscul = zeros(6, N);
check_oscul = zeros(6, N);

for i = 1:N
    oscul(:, i) = rv2osc(xj2(:,i), params)';
    check_oscul(:,i) = xj2(:, i) - osc2rv(rv2osc(xj2(:,i), params)', params)';
end
disp(max(check_oscul,[],2)) 

%% Graphics
close all

figure
subplot(3,1,1);
hold on
grid on
title('First_integrals')
text(max(t) * 0.6, max(h_int) * 0.8, "Energy integral")
xlabel('time, seconds')
ylabel('energy, J')
plot(t, h_int, "blue");

subplot(3,1,2);
hold on
grid on
text(max(t) * 0.6, max(c_int,[],'all') * 0.8, "Area integral")
xlabel('time, seconds')
ylabel('area, m^2/s')
plot(t, c_int);

subplot(3,1,3);
hold on
grid on
text(max(t) * 0.6, max(f_int,[],'all') * 0.8, "Laplace integral")
xlabel('time, seconds')
ylabel('m^3/s^-2')
plot(t, f_int);

figure
hold on
grid on
title('Энергия в движении с J2')
xlabel('time, seconds')
ylabel('energy, Joules')
plot(t, centralize(vj2.^2./2 - params.mu./rj2 + params.alpha*(3*xj2(3, :).^2 / rj2.^2 - 1)./rj2.^3));

figure
hold on
grid on
title('Trajectory')
xlabel('x, km')
ylabel('y, km')
x_max = max(abs(x),[],"all" )*1.2;
axis([-x_max x_max -x_max x_max])
plot(x(1,:), x(2,:));
plot(xj2(1, :), xj2(2,:));
legend('Central Gravity Field', 'J2 Perturbations')

figure("Name", "Osculating elements")
subplot(2, 2, 1)
hold on
grid on
title('Osculating Elements (deg)')
xlabel('t, s')
ylabel('degrees')
plot(t, rad2deg(oscul(3, :)))
plot(t, rad2deg(oscul(5, :)))
plot(t, rad2deg(oscul(6, :)))
legend('Equinox', 'Inclination', 'Pericenter Aeg.')

subplot(2, 2, 2)
hold on
grid on
title('Osculating Transformation check')
xlabel('t, s')
ylabel('degrees')
plot(t, check_oscul(1, :))
plot(t, check_oscul(2, :))
plot(t, check_oscul(3, :))
plot(t, check_oscul(4, :))
plot(t, check_oscul(5, :))
plot(t, check_oscul(6, :))

subplot(2, 2, 3)
hold on
grid on
title('Eccentricity')
xlabel('t, s')
ylabel('degrees')
plot(t, oscul(1, :))

subplot(2, 2, 4)
hold on
grid on
title('Large semi-axis')
xlabel('t, s')
ylabel('degrees')
plot(t, oscul(2, :))