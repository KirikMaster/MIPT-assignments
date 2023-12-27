function [B] = create_SK(rs)
B = zeros(3, 3);
B(1:3, 3) = rs;
tmp = cross([0 0 1], rs);
if norm(tmp) > 0.5
    B(1:3, 2) = normalized(tmp);
else
    tmp = cross([0 1 0], rs);
    B(1:3, 2) = normalized(tmp);
end
B(1:3, 1) = cross(B(1:3, 2), B(1:3, 3));
end