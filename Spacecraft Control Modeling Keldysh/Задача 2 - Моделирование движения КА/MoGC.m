function [y] = MoGC(x, t, params)
    J = params.J;
    J_inv = params.J_inv;
    A = x(1:3, 1:3);
    w = x(:,4);
    A_dot = -CrossMatrix(w) * A;
    w_dot = -J_inv * cross(w, J * w) + J_inv * ControlMoment(A, t, 'MoGC', params);
    y = [A_dot, w_dot];
end