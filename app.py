from flask import Flask, request, render_template, jsonify
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import json

app = Flask(__name__)

# Function to authenticate using OAuth2 credentials
def authenticate():
    # Authenticate using the OAuth2 credentials
    sc = OAuth2(None, None, from_file='json/ouath2.json')
    return sc

# Function to fetch league information using league ID
def fetch_league_info(league_id):
    # Authenticate
    sc = authenticate()
    
    # Access the NBA game
    gm = yfa.Game(sc, 'nba')

    # Access the league using the provided league ID
    lg = gm.to_league(league_id)

    # Get the team key for the league
    teamkey = lg.team_key()

    # Access the team associated with the team key
    team = lg.to_team(teamkey)

    # Get the standings for the league
    standings = lg.standings()

    # Prepare data
    data = {
        "standings": standings
    }

    # Save data to JSON file
    with open('json/fantasy_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Function to read JSON data from file
def read_json_data():
    with open('json/fantasy_data.json', 'r') as json_file:
        data = json.load(json_file)
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        league_id = request.form['league_id']
        fetch_league_info(league_id)
        data = read_json_data()
        standings = data['standings']
        return render_template('index.html', standings=standings)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
