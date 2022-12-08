AC = @(n_AC)15 + (0.1*n_AC);
CB = 40;
AD = 40;
DB = @(n_DB)15 + (0.1*n_DB);
CD = 0;
% Actions: 1 - AC+CB; 2 - AD+DB; 3 - AC+CD+DB; 4 - AD+DC+CB
n = 200;
idx = 1:1:n;
neighbours = [1:n 1:n 1:n];
%con(1:50) = 100;
%con(51:150) = 1;
%con(151:200) = 100;
%con = [n/2:-1:1 n/2:-1:1];
con = round((((n/2)-1)*rand(1,200))+1);
%con = n/2*ones(1,200); %Replace with this for full connectivity
%gamma = 1:(-1/200):0; %Uncomment for gradual increase of selfishness
gamma = rand(1,200); %Uncomment for random selfishness
%gamma = ones(1,200); %Replace with this for zero selfishness
%gamma(151:200) = 0;
for stage = 1:1:1000
    %Stage Game
    disp(stage);
    %Initialization 
    %Action(idx(1:n)) = 4;
    Action(idx(1:n/4)) = 1;
    Action(idx((n/4)+1:n/2)) = 2;
    Action(idx((n/2)+1:3*n/4)) = 3;
    Action(idx((3*n/4)+1:n)) = 4;
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
    
    if stage > 1
        for i = 1:n
            %avg_i = sum(J_total(:,i))/(stage-1);
            diff = J_total(stage-1,i) - 65;
            if diff > 0                
                gamma(i) = max(0,gamma(i)/(diff));
                con(i) = max(1,round(con(i)/(diff)));
                %Working heuristic
                %gamma(i) = max(0,gamma(i)/4);
                %con(i) = max(1,round(con(i)/4));
            else
                gamma(i) = min(1,gamma(i)*(-diff));
                con(i) = min(n/2,round(con(i)*(-diff)));
                %gamma(i) = min(1,gamma(i)*2);
                %con(i) = min(n/2,round(con(i)*2));
            end
        end
    end

    Prev_Action(1:n) = 0;
    
    while nnz((Prev_Action~=Action) ~=0)
        
        Prev_Action = Action;
        for i = 1:n
            J1 = zeros(1,n);
            J2 = zeros(1,n);
            J3 = zeros(1,n);
            J4 = zeros(1,n);
            Current_Action = Action(idx(i));
            if Current_Action == 1 || Current_Action == 3
                n_AC = n_AC-1;
            end
            if Current_Action == 2 || Current_Action == 3
                n_DB = n_DB-1;
            end
            Action(idx(i)) = 1;
            for k = neighbours(n+i-(con(i)):n+i+(con(i))-1) 
                if Action(k) == 1
                    J1(k) = AC(n_AC+1)+CB;
                elseif Action(k) == 2
                    J1(k) = AD+DB(n_DB);
                elseif Action(k) == 3
                    J1(k) = AC(n_AC+1)+CD+DB(n_DB);
                elseif Action(k) == 4
                    J1(k) = AD+CD+CB;
                end
            end
            Action(idx(i)) = 2;
            for k = neighbours(n+i-(con(i)):n+i+(con(i))-1)
                if Action(k) == 1
                    J2(k) = AC(n_AC)+CB;
                elseif Action(k) == 2
                    J2(k) = AD+DB(n_DB+1);
                elseif Action(k) == 3
                    J2(k) = AC(n_AC)+CD+DB(n_DB+1);
                elseif Action(k) == 4
                    J2(k) = AD+CD+CB;
                end
            end
            Action(idx(i)) = 3;
            for k = neighbours(n+i-(con(i)):n+i+(con(i))-1)
                if Action(k) == 1
                    J3(k) = AC(n_AC+1)+CB;
                elseif Action(k) == 2
                    J3(k) = AD+DB(n_DB+1);
                elseif Action(k) == 3
                    J3(k) = AC(n_AC+1)+CD+DB(n_DB+1);
                elseif Action(k) == 4
                    J3(k) = AD+CD+CB;
                end
            end
            Action(idx(i)) = 4;
            for k = neighbours(n+i-(con(i)):n+i+(con(i))-1)
                if Action(k) == 1
                    J4(k) = AC(n_AC)+CB;
                elseif Action(k) == 2
                    J4(k) = AD+DB(n_DB);
                elseif Action(k) == 3
                    J4(k) = AC(n_AC)+CD+DB(n_DB);
                elseif Action(k) == 4
                    J4(k) = AD+CD+CB;
                end
            end

            cost1 = [sum(J1),sum(J2),sum(J3),sum(J4)];
            cost2 = [AC(n_AC+1)+CB,AD+DB(n_DB+1),AC(n_AC+1)+CD+DB(n_DB+1),AD+CD+CB];
            costs = (gamma(i)*cost1) + ((1-gamma(i))*cost2);
            a = find(costs == min(costs));
            Action(idx(i)) = a(1);

            if Action(idx(i)) == 1 || Action(idx(i)) == 3
                n_AC = n_AC+1;
            end
            if Action(idx(i)) == 2 || Action(idx(i)) == 3
                n_DB = n_DB+1;
            end
            if Action(idx(i)) == 1
                J(idx(i)) = AC(n_AC)+CB;
            elseif Action(idx(i)) == 2
                J(idx(i)) = AD+DB(n_DB);
            elseif Action(idx(i)) == 3
                J(idx(i)) = AC(n_AC)+CD+DB(n_DB);
            elseif Action(idx(i)) == 4
                J(idx(i)) = AD+CD+CB;
            end
        end
       
    end
    J_total(stage,:) = J;
    tot_gamma(stage,:) = gamma;
    tot_con(stage,:) = con;
    tot_action(stage,:) = Action;
%     [out,idx] = sort(J,'descend');
%     u = unique(J);
%     idx = [];
%     for g = length(u):-1:1
%         h = find(J == u(g));
%         idx = [idx h(randperm(length(h)))];
%     end    
end
%1 - 67.5 : 25
%2 - 67.5 : 25
%3 - 55 : 100
%4 - 80 : 50
