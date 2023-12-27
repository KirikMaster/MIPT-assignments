function [mm_re] = mag_coil(mm_id)
%MAG_COIL given the desired moment yields magnetic dipole moment
%   Detailed explanation goes here
global mm_coil
mm_max = 10;
sig_h = 1e-3;
e1 = normalized([1 0 0]');
e2 = normalized([0 1 0]');
e3 = normalized([-1e-3, -1e-3, 1]');
A = [e1, e2, e3];
h1 = randn2(1, sig_h);
h2 = randn2(1, sig_h);
h3 = randn2(1, sig_h);
A_h = [e1 * h1, e2 * h2, e3 * h3];
mm_co = A_h \ mm_id;

if norm(mm_co) > mm_max % Обрезка
    mm_co = normalized(mm_co) * mm_max;
end
mm_re = A * mm_co;
mm_coil = mm_re;
end

