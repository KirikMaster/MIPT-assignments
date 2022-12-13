function [Mctrl] = ControlMoment(x, t, instruction, params)
switch params.scenario
    case "Euler"
        Mctrl = zeros(3, 1);
    case "Lagrange"
        switch instruction
            case 'Euler Angles'
                A = EulerMatrix(x);
                g = A * params.g;
            case 'MoGC'
                g = x * params.g;
            case 'Quat'
                A = quat2dcm(x);
                g = A * params.g;
        end
        Mctrl = params.m * params.l * cross([0, 0, 1], g);
end
end