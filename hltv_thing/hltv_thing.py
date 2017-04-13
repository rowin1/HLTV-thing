""" HLTV.org scraper that calculates various statistics for
    top ranked CSGO teams.
"""
import sys
import datetime

import requests
from lxml import etree
from lxml import html


def get_teams():
    """
    Reads file containing team names and ids.
    @return: list of teams in the form
    [{'name': team_name, 'id': team_id}]
    """
    teams = []
    with open('teamids.txt') as f:
      for line in f:
        if line[0] == '\n': continue
        team_data = line[0:-1]
        team_name = ' '.join(team_data.split()[0:-1])
        team_id = team_data.split()[-1]
        teams.append({'name': team_name, 'id': team_id})
    return teams

def get_maps():
    """
    Reads file containing map names.
    @return: list of maps in the form:
    ['map1, 'map2', 'map3']
    """
    with open('maps.txt.') as f:
        maps = [line[0:-1] for line in f if line[0] != "\n"]
    return maps

def show_team_menu(teams):
    """Prompts user with a select-team menu from a list of teams. """
    print "Please select a team: (enter team number)"

    for i, team in enumerate(teams):
        print ('{}: {}'.format(i + 1, team['name']))

    print ('\n0: Exit program')

def show_map_menu(maps):
    """ Prompts user with a select-map menu from a list of maps. """
    print "Please select a map: (enter map number)"
    for i, map_name in enumerate(maps):
        print ('{}: {}'.format(i + 1, map_name))
    print ('{}: {}'.format (i + 2, 'ALL'))

def select_teams(teams):
    """Returns a list of two dicts of teamdata from user's raw_input"""
    teams_selected = []
    while len(teams_selected) < 2:
        if len(teams_selected) == 0:
            teamnumber = raw_input('Team : ')
        else:
            teamnumber = raw_input('Opponent: ')

        if teamnumber.isdigit():
            teamnumber = int(teamnumber)
        else:
            print "Please enter a valid teamid number."
            continue

        if teamnumber == 0:
            print "Exiting HLTV-thing..."
            sys.exit()
        elif teamnumber <= len(teams):
            if teamnumber not in teams_selected:
                teams_selected.append(teams[teamnumber-1])
            else:
                print "Please enter a non-duplicate team."
        else:
            print "Please enter a valid teamid number."

    return teams_selected[0], teams_selected[1]

def select_map(maps):
    map_selected = ''
    while not map_selected:
        mapnumber = raw_input('Map: ')
        if mapnumber.isdigit():
            mapnumber = int(mapnumber)
        if mapnumber == 0:
            print "Exiting HLTV-thing..."
            sys.exit()
        elif mapnumber <= len(maps):
            map_selected = maps[mapnumber-1]
        elif mapnumber == len(maps) + 1:
            map_selected = 'ALL'
        else:
            print "Please enter a valid map number."
    return map_selected




class Team(object):

    def __init__(self, team):
        """
        Takes a dict for a given team in the form:
        {'name': team_name, 'id': team_id}
        """
        self.name = team['name']
        self.id = team['id']
        self.match_data = self.get_matches()


    def get_matches(self):
        """
        Retrieves list of match data from HLTV.org.
        Returns a list of match data dicts
        """
        page = requests.get('http://www.hltv.org/?pageid=188&teamid=' + self.id)
        # Add '&requiredPlayers=5' to the end of the url for current lineup only
        tree = html.fromstring(page.content) # alternatively can use etree.HTML(page.text)
        games = tree.xpath('//div[@style="padding-left:5px;padding-top:5px;"]')

        res = []
        for section in games:
            game = etree.HTML(etree.tostring(section))
            content = game.xpath('//text()')
            res.append(self.build_game_dict(content[1:7]))
        return res


    def build_game_dict(self, game):
        """
        Takes a list containing data from a single match in the form:
        ['d/m y', 'team (rounds)', 'opponent (rounds)', map, event, result]
        @return Dict of match data with keys:
        'date', 'team', 'opponent', 'score', 'event', 'result', 'map'
        """
        res = {}
        res['date'] = game[0]
        res['team'] = ' '.join(game[1].split()[0:-1])
        team_rounds_won = game[1].split()[-1]
        opponent_rounds_won = game[2].split()[-1]
        res['score'] = '-'.join([team_rounds_won, opponent_rounds_won])
        res['opponent'] = ' '.join(game[2].split()[0:-1])
        res['event'] = game[4]
        res['result'] = game[5]
        res['map'] = game[3]

        return res

    def display_latest_game(self):
        print self.match_data[0]

    def print_map_win_ratio(self, map_name):
        wins = 0
        losses = 0
        for game in self.match_data:
            if game['map'] == map_name:
                if game['result'] == 'W':
                    wins += 1
                else:
                    losses += 1
            else:
                None
        print "%s: %dW-%dL (%.0f%%)" % (map_name, wins, losses, 100 * float(wins)/(wins+losses))

    def print_against_opponent_win_ratio(self, opponent):
        wins = 0
        losses = 0
        for game in self.match_data:
            if game['opponent'] == opponent:
                if game['result'] == 'W':
                    wins += 1
                else:
                    losses += 1
            else:
                None
        print "Against %s: %dW-%dL (%.0f%%)" % (opponent, wins,losses, 100 * float(wins)/(wins+losses))

    def print_against_opponent_win_ratio_on_map(self, opponent, map_name):
        wins = 0
        losses =0
        for game in self.match_data:
            if game['opponent'] == opponent and game['map'] == map_name:
                if game['result'] == 'W':
                    wins += 1
                else:
                    losses += 1
            else:
                None
        print "Against %s on %s: %dW-%dL (%.0f%%)" % (opponent, map_name, wins, losses, 100 * float(wins)/(wins+losses))

    def print_map_individual_results(self, opponent, map_name):
        for game in self.match_data:
            if game['opponent'] == opponent and game['map'] == map_name:
                print game

def main(*argv):

      ##display_stats(team)


      teams = get_teams()
      show_team_menu(teams)
      team, opponent= select_teams(teams)
      selected_team = Team(team)

      maps = get_maps()
      show_map_menu(maps)
      selected_map = select_map(maps)

      selected_team.print_against_opponent_win_ratio(opponent['name'])
      selected_team.print_map_win_ratio(selected_map)
      selected_team.print_against_opponent_win_ratio_on_map(opponent['name'], selected_map)
      selected_team.print_map_individual_results(opponent['name'], selected_map)


if __name__ == "__main__":
    main(sys.argv)
