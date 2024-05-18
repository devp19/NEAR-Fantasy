from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import json


# Authenticate using the OAuth2 credentials
sc = OAuth2(None, None, from_file='oauth2.json')


# Access the NBA game
gm = yfa.Game(sc, 'nba')

# Get the list of league IDs associated with the authenticated user
leagues = gm.league_ids()
print("Leagues:", leagues)

# Access a specific league by its ID (example ID '428.l.184608')
lg = gm.to_league('428.l.184608')

# Get the team key for the league
teamkey = lg.team_key()
print("Team Key:", teamkey)

# Access the team associated with the team key
team = lg.to_team(teamkey)

# Get the rostser for the team
roster = team.roster()
# print("Roster:", roster)


standings = lg.standings()


data = { 
    "leagues": leagues,
    "team_key": teamkey,
    "roster": roster,
    "standings": standings

}

with open('fantasy_data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

