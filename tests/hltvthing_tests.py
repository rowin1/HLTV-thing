# These should be equal
test_team.print_against_opponent_win_ratio('Natus Vincere')
test_team.print_against_opponent_win_ratio(selected_teams[1]['name'])


 teams = get_teams()
 show_team_menu(teams)
 selected_teams = select_teams(teams)
 show_map_menu(get_maps())
 selected_map = select_map(get_maps())
 test_team = Team(selected_teams[0])

 test_team.print_map_win_ratio('inferno')
 test_team.print_map_win_ratio(selected_map)


 test_team.print_against_opponent_win_ratio_on_map(selected_teams[1]['name'], selected_map)
