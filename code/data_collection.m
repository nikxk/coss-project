var1_vals = 0:0.02:1;
var2_vals = 0:2:100;
J_vals = zeros(length(var1_vals),length(var2_vals));
for ind1 = 1:length(var1_vals)
    for ind2 = 1:length(var2_vals)
        var1 = var1_vals(ind1);
        var2 = var2_vals(ind2);
        congestion_game_welfare;
        J_vals(ind1,ind2)=sum(sum(J_total()))/(20000);
    end
end