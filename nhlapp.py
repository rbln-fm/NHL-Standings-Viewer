from flask import Flask, render_template
from nhlpy import NHLClient
from datetime import date

app = Flask(__name__)
client = NHLClient()
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/teams")
def teams():
    teams = client.teams.teams()
    teams.sort(key=lambda t: t["name"])
    
    return render_template("teams.html", teams = teams)

@app.route("/teams/<abbr>")
def teams_info(abbr):
    teams = client.teams.teams()
    team = None
    roster = None
    current_season = None
    current_date = str(date.today())
    current_month = date.today().month

    if current_month >= 9:
        current_season = f"{date.today().year}{date.today().year + 1}"
        previous_season = f"{date.today().year - 1}{date.today().year}"
        next_season = f"{date.today().year + 1}{date.today().year + 2}"
    else:
        current_season = f"{date.today().year - 1}{date.today().year}"
        previous_season = f"{date.today().year -2}{date.today().year - 1}"
        next_season = f"{date.today().year}{date.today().year + 1}"

    for team in teams:
        if team['abbr'].lower() == abbr:
            team = team
            roster = client.teams.team_roster(team_abbr = abbr, season = current_season)
            break

    full_schedule = client.schedule.team_season_schedule(team_abbr = abbr, season = current_season)
    prev_season_schedule = client.schedule.team_season_schedule(team_abbr = abbr, season = previous_season)
    next_season_schedule = client.schedule.team_season_schedule(team_abbr = abbr, season = next_season)
    
    return render_template("teaminfo.html", 
                           abbr = abbr,
                           team = team, 
                           roster = roster, 
                           season = current_season,
                           today = current_date,
                           schedule = full_schedule,
                           prev_schedule = prev_season_schedule,
                           next_schedule = next_season_schedule)

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
    app.run(debug = True)