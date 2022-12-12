function [y] = MoGC(x, t, params)
    J = params.J;
    A = x(1:3, 1:3);
    w = x(:,4);
    A_dot = -CrossMatrix(w) * A;
    w_dot = -cross(J^-1 * w, J * w) + J^-1 * ControlMoment(t, x, params);
    y = [A_dot, w_dot];
end