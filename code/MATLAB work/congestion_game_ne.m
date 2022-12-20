AC = @(n_AC)15 + (0.1*n_AC);
CB = 40;
AD = 40;
DB = @(n_DB)15 + (0.1*n_DB);
CD = 0;
% Actions: 1 - AC+CB; 2 - AD+DB; 3 - AC+CD+DB; 4 - AD+DC+CB
n = 100;
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
Prev_Action(1:n) = 0;
while nnz((Prev_Action~=Action) ~=0)
    disp("Iteration")
    Prev_Action = Action;
    for i = 1:n
        Current_Action = Action(i);
        if Current_Action == 1 || Current_Action == 3
            n_AC = n_AC-1;
        end
        if Current_Action == 2 || Current_Action == 3
            n_DB = n_DB-1;
        end
        costs = [AC(n_AC+1)+CB,AD+DB(n_DB+1),AC(n_AC+1)+CD+DB(n_DB+1),AD+CD+CB];
        Action(i) = find(costs == min(costs));
        if Action(i) == 1 || Action(i) == 3
            n_AC = n_AC+1;
        end
        if Action(i) == 2 || Action(i) == 3
            n_DB = n_DB+1;
        end
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
i = 1;
tot1 = zeros(n,n);
tot2 = zeros(n,n);
tot3 = zeros(n,n);
tot4 = zeros(n,n);
for n_AC_1 = 1:1:n
    for n_DB_1 = 1:1:n
        tot1(n_AC_1,n_DB_1) = AC(n_AC_1) + CB;
        tot2(n_AC_1,n_DB_1) = AD + DB(n_DB_1);
        tot3(n_AC_1,n_DB_1) = AC(n_AC_1) + CD + DB(n_DB_1);
        tot4(n_AC_1,n_DB_1) = AD+CD+CB;
    end
end
        

