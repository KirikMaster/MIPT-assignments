function [y] = centralize(x)
if ismatrix(x)
    y = x - x(:,1);
elseif ndims(x) == 3
    y = x - x(:,:,1);
end