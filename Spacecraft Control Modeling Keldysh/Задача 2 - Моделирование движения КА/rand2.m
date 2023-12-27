function [rand_num] = rand2(start, finish)
    rand_num = start + rand(1) * (finish - start); 
end