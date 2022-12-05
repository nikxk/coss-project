AC = @(n_AC)15 + (0.1*n_AC);
CB = 40;
AD = 40;
DB = @(n_DB)15 + (0.1*n_DB);
CD = 0;
% Actions: 1 - AC+CB; 2 - AD+DB; 3 - AC+CD+DB; 4 - AD+DC+CB
n = 200;
Action(1:n/4) = 1;
Action((n/4)+1:n/2) = 2;
Action((n/2)+1:(3*n/4)) = 3;
Action((3*n/4)+1:n) = 4;
n_AC = n/2;
n_DB = n/2;
J = zeros(1,n);
for i = 1:n
    if Action(i) == 1
        J(i) = AC(n_AC)+CB;
    elseif Action(i) == 2
        J(i) = AD+DB(n_DB);
    elseif Action(i) == 3
        J(i) = AC(n_AC)+CD+DB(n_DB);
    elseif Action(i) == 4
        J(i) = AD+CD+CB;
    end
end
%Inducing cooperation/interaction between players known initial actions and
%social optimum
% A = zeros(200);
% A(1:25,1:25) = eye(25);
% A(26:50,101:125) = eye(25);
% A(51:75,51:75) = eye(25);
% A(76:100,126:150) = eye(25);
% A(101:200,101:200) = eye(100);

Prev_Action(1:n) = 0;
while nnz((Prev_Action~=Action) ~=0)
    disp("Iteration")
    Prev_Action = Action;
    Current_Action = A*Action';
    Action = Current_Action';
    n_AC = 0;
    n_DB = 0;
    for i = 1:n
        if Action(i) == 1 || Action(i) == 3
            n_AC = n_AC+1;
        end
        if Action(i) == 2 || Action(i) == 3
            n_DB = n_DB+1;
        end
    end
    for i = 1:n
        if Action(i) == 1
            J(i) = AC(n_AC)+CB;
        elseif Action(i) == 2
            J(i) = AD+DB(n_DB);
        elseif Action(i) == 3
            J(i) = AC(n_AC)+CD+DB(n_DB);
        elseif Action(i) == 4
            J(i) = AD+CD+CB;
        end
    end
end

