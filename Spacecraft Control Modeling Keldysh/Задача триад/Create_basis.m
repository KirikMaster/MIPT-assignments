function [A] = Create_basis(V1, V2)
%CREATE_BASIS Builds an orthonormal basis in Eucledean 3D from two given
%vectors and returns a matrix of it's transformation
%   Detailed explanation goes here
V1 = normalized(V1);
V2 = normalized(V2);
r1 = vect2cols(V1);
r2 = vect2cols(normalized(cross(V1, V2)));
r3 = vect2cols(normalized(cross(V1, cross(V1, V2))));
A = [r1, r2, r3];
end

