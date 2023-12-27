function [rand_num] = randn2(avg, sigma)
%RANDN2 returns normally distributed data with given mathematical
%expectation and variance of the same type, as the expectation variable.
    rand_num = randn(size(avg, 1), size(avg, 2)) * sigma + avg;
end