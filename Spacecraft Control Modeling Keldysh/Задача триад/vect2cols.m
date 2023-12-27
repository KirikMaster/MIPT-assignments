function [col] = vect2cols(vect)
%VECT2COLS returns the [3 x 1] vector
%   If the inputed vector is a column (i.e. its shape is n x 1) then this
%   function returns it as it is. Else if it is a row (i.e. its shape is 1
%   x n) then the function transposes it.
if size(vect, 2) > 1
    col = vect';
else
    col = vect;
end
end

