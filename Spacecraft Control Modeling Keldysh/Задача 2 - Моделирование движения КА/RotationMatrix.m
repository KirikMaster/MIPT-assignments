function [A] = RotationMatrix(n, i)
A = eye(3);
if n == 1
    A(2:3, 2:3) = [[cos(i), -sin(i)]; [sin(i), cos(i)]];
elseif n == 2
    A(1, 1) = cos(i);
    A(1, 3) = sin(i);
    A(3, 1) = -sin(i);
    A(3, 3) = cos(i);
elseif n == 3
    A(1:2, 1:2) = [[cos(i), -sin(i)]; [sin(i), cos(i)]];
end
end