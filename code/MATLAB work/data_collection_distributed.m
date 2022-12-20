for ind1 = 1:100
    congestion_game_welfare;
    J_vals(ind1)=sum(sum(J_total()))/(20000);
    J_i_vals(ind1,:)=sum(J_total())/(100);
end