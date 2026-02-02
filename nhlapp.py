from flask import Flask, render_template
from nhlpy import NHLClient

app = Flask(__name__)
client = NHLClient()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/teams")
def teams():
    teams = client.teams.teams()
    
    return render_template("teams.html", teams=teams)

@app.route("/standings/<category>")
def standings(category):
    teams = client.teams.teams()
    standings = client.standings.league_standings()

    conferences = {}
    divisions = {}

    for team in standings["standings"]:
        conference = team["conferenceName"]
        division = team["divisionName"]

        if conference not in conferences: 
            conferences[conference] = [team]
        else:
            conferences[conference].append(team)

        if division not in divisions: 
            divisions[division] = [team]
        else:
            divisions[division].append(team)

    return render_template("standings.html", 
                           teams = teams, 
                           standings = standings, 
                           conferences = conferences, 
                           divisions = divisions,
                           category = category)

if __name__ == "__main__":
    app.run(debug=True)