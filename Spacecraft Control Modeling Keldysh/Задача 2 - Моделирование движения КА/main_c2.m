%% Setup
clc
clear all
close all

%%parameters
A_ = 1.0;
B_ = 2.3;
C_ = 2.6;
J = [A_, 0, 0;
     0, B_, 0;
     0, 0, C_];

params = struct();
params.J = J;
params.J_inv = inv(J);
params.w0 = 7e-07; % с^-1

%%Initializing
dt = 1e-1;
T =100;
t = 0:dt:T; %%start:step:end
N = length(t);

for i = 1:3
    for j = 1:3, j~=i;
        for isign = -1:2:1
            for jsign = -1:2:1
                e1 = [0 0 0];
                e2 = [0 0 0];
                e1(i) = isign;
                e2(j) = jsign;
                e3 = cross(e1, e2);
                Drel = [e1; e2; e3]; % ССК -> ОСК
                eps = 1e-1;
                sigma = 1e-5;
                R = chol(sigma);
                wrel = randn(1,3)*R;
                dq = randn(3,1)*R;
                dQ = quatnormalize(cat(1, sqrt(1 - norm(dq)^2), dq)');
                Q_init = dcm2quat(Drel);
                Q = quatmultiply(dQ, Q_init);
                for k = 1:N
                    ret = integrator(@GravMoment_red, [Q, wrel], t(i), dt, params);
                    Q = ret(1:4);
                    wrel = ret(5:7);
                    unstable = false;
                    dQ_n = quatdivide(Q, Q_init);
                    if norm(wrel) > eps || norm(dQ_n(2:4)) > eps
                        disp(["eps ", eps])
                        disp(["wrel ", norm(wrel)])
                        disp(["dq", norm(dQ_n(2:4))])
                        unstable = true;
                        break
                    end
                end
                if unstable
                    disp(["i = ", isign*i, "j = ", jsign*j, " - unstable, t = ", k * dt])
                else
                    disp(["i = ", isign*i, "j = ", jsign*j, " - stable, for t = ", T])
                end
            end
        end
    end
end