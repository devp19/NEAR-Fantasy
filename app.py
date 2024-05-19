from flask import Flask, request, render_template, jsonify
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import json
# from jinja2 import Environment

app = Flask(__name__)

# Function to authenticate using OAuth2 credentials
def authenticate():
    # Authenticate using the OAuth2 credentials
    sc = OAuth2(None, None, from_file='json/ouath2.json')
    return sc


# # Define a custom filter for multiplication
# def multiply(value, factor):
#     return value * factor

# # Add the custom filter to the Jinja2 environment
# app.jinja_env.filters['multiply'] = multiply


def fetch_league_info(league_id):
    # Authenticate
    sc = authenticate()
    
    # Access the NBA game
    gm = yfa.Game(sc, 'nba')

    # Access the league using the provided league ID
    lg = gm.to_league(league_id)

    # Get the standings for the league
    standings = lg.standings()

    # Prepare data
    data = {"standings": standings}

    # Initialize a dictionary to store team rosters
    team_data = {}

    # Iterate over each team in the standings
    for team_standings in standings:
        team_key = team_standings['team_key']
        # Access the team associated with the team key
        team = lg.to_team(team_key)
        # Get the roster for the team
        team_roster = team.roster()
        # Store the roster in the team_data dictionary
        team_data[team_key] = team_roster

    # Save data to JSON file
    with open('json/fantasy_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
        
    # Save team roster data to JSON file
    with open('json/fantasy_team_data.json', 'w') as json_file:
        json.dump(team_data, json_file, indent=4)



# Function to read JSON data from file
def read_json_data():
    with open('json/fantasy_data.json', 'r') as json_file:
        data = json.load(json_file)
    return data

def read_json_team_data():
    with open('json/fantasy_team_data.json', 'r') as json_file:
        team_data = json.load(json_file)
    return team_data



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        league_id = request.form['league_id']
        fetch_league_info(league_id)
        data = read_json_data()
        standings = data['standings']
        team_data = read_json_team_data()

        return render_template('index.html', standings=standings, team_data=team_data)
    return render_template('index.html')

   

if __name__ == '__main__':
    app.run(debug=True)
