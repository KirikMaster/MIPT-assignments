function [mm] = b_dot(w, B, params)
%B_DOT calculates desired control magnetic moment for b-dot algorithm
%   Detailed explanation goes here
k = params.b_dot_ctrl;

mm_id = k * cross(w, B); %
mm = mag_coil(mm_id);
end

