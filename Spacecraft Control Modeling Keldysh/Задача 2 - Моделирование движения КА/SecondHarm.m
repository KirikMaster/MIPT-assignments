function [aj2] = SecondHarm(r_vect, params)
if params.j2 == false
    aj2 = [0, 0, 0]';
else
r = norm(r_vect);
x = r_vect(1);
y = r_vect(2);
z = r_vect(3);
ax = -15*params.alpha * x * z^2 / r^7 + 3*params.alpha * x / r^5;
ay = -15*params.alpha * y * z^2 / r^7 + 3*params.alpha * y / r^5;
az = -15*params.alpha * z^3 / r^7 + 9*params.alpha * z / r^5; 
aj2 = [ax, ay, az]';
end
end