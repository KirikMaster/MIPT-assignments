function [A] = EulerMatrix(psi, theta, phi)
B1 = RotationMatrix(3, psi);
B2 = RotationMatrix(1, theta);
B3 = RotationMatrix(3, phi);
A = B3 * B2 * B1;
end