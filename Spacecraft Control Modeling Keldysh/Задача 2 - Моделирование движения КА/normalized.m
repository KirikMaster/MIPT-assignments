function [norm_vector] = normalized(vector)
    norm_vector = vector / norm(vector);
end