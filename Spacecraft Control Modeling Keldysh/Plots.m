clc
clear all
close all

x = 0:0.01:2*pi;
y = zeros(1, length(x));

for i = 1:length(x)
    y(i) = sin(x(i))
end

figure
hold on
grid on
xlabel('x, [m]')
ylabel('sin x')
plot(x, y)