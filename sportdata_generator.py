import random
from datetime import datetime, timedelta
import json
import sys

football_teams = [
    ["Al Shabab", "Al Shabab FC", "al-shabab-fc", "SHA", "KSA"],
    ["Manchester United", "Manchester United FC", "manchester-united-fc", "MUN", "ENG"],
    ["Real Madrid", "Real Madrid CF", "real-madrid-cf", "RMA", "ESP"],
    ["Bayern Munich", "FC Bayern Munchen", "fc-bayern-munich", "FCB", "GER"],
    ["Paris Saint-Germain", "Paris Saint-Germain FC", "paris-saint-germain-fc", "PSG", "FRA"],
    ["Juventus", "Juventus FC", "juventus-fc", "JUV", "ITA"],
    ["Al Hilal", "Al Hilal Saudi FC", "al-hilal-fc", "HIL", "KSA"],
    ["Liverpool", "Liverpool FC", "liverpool-fc", "LIV", "ENG"],
    ["Barcelona", "FC Barcelona", "fc-barcelona", "BAR", "ESP"],
    ["AC Milan", "AC Milan", "ac-milan", "MIL", "ITA"],
    ["Inter Milan", "FC Internazionale Milano", "inter-milan", "INT", "ITA"],
    ["Chelsea", "Chelsea FC", "chelsea-fc", "CHE", "ENG"],
    ["Arsenal", "Arsenal FC", "arsenal-fc", "ARS", "ENG"],
    ["Tottenham Hotspur", "Tottenham Hotspur FC", "tottenham-hotspur-fc", "TOT", "ENG"],
    ["Atletico Madrid", "Atletico de Madrid", "atletico-madrid", "ATM", "ESP"],
    ["Sevilla", "Sevilla FC", "sevilla-fc", "SEV", "ESP"],
    ["Borussia Dortmund", "Borussia Dortmund", "borussia-dortmund", "BVB", "GER"],
    ["RB Leipzig", "RasenBallsport Leipzig", "rb-leipzig", "RBL", "GER"],
    ["Marseille", "Olympique de Marseille", "olympique-marseille", "MAR", "FRA"],
    ["Lyon", "Olympique Lyonnais", "olympique-lyonnais", "LYO", "FRA"],
    ["Napoli", "SSC Napoli", "ssc-napoli", "NAP", "ITA"],
    ["Roma", "AS Roma", "as-roma", "ROM", "ITA"],
    ["Ajax", "AFC Ajax", "afc-ajax", "AJA", "NED"],
    ["PSV Eindhoven", "PSV Eindhoven", "psv-eindhoven", "PSV", "NED"],
    ["Feyenoord", "Feyenoord Rotterdam", "feyenoord", "FEY", "NED"],
    ["Benfica", "SL Benfica", "sl-benfica", "BEN", "POR"],
    ["Porto", "FC Porto", "fc-porto", "POR", "POR"],
    ["Sporting CP", "Sporting Clube de Portugal", "sporting-cp", "SCP", "POR"],
    ["Celtic", "Celtic FC", "celtic-fc", "CEL", "SCO"],
    ["Rangers", "Rangers FC", "rangers-fc", "RAN", "SCO"],
    ["Al Nassr", "Al Nassr FC", "al-nassr-fc", "NAS", "KSA"],
    ["Flamengo", "CR Flamengo", "cr-flamengo", "FLA", "BRA"],
    ["Palmeiras", "SE Palmeiras", "se-palmeiras", "PAL", "BRA"],
    ["River Plate", "Club Atletico River Plate", "river-plate", "RIV", "ARG"],
    ["Boca Juniors", "Club Atletico Boca Juniors", "boca-juniors", "BOC", "ARG"],
    ["Gremio", "Gremio Foot-Ball Porto Alegrense", "gremio", "GRE", "BRA"],
    ["Santos", "Santos FC", "santos-fc", "SAN", "BRA"],
    ["Galatasaray", "Galatasaray SK", "galatasaray", "GAL", "TUR"],
    ["Fenerbahce", "Fenerbahce SK", "fenerbahce", "FEN", "TUR"]
]


stadiums = [
    "Old Trafford",
    "Santiago Bernabeu",
    "Allianz Arena",
    "Parc des Princes",
    "San Siro",
    "Camp Nou",
    "Anfield",
    "Signal Iduna Park",
    "Emirates Stadium",
    "Stamford Bridge",
    "Maracana",
    "Estadio da Luz",
    "Johan Cruyff Arena",
    "King Fahd International Stadium",
    "Ataturk Olympic Stadium",
    "Celtic Park",
    "Estadio Monumental",
    "Stadio Olimpico",
    "Tottenham Hotspur Stadium",
    "Red Bull Arena"
]


competitions = [
    ["afc-champions-league", "AFC Champions League"],
    ["uefa-champions-league", "UEFA Champions League"],
    ["super-league", "Super League"],
    ["ultra-super-league", "Ultra Super League"],
]

stages = [
    ["ROUND OF 32", "ROUND OF 32", 4],
    ["ROUND OF 16", "ROUND OF 16", 4],
    ["QUARTERFINALS", "QUARTERFINALS", 4],
    ["SEMIFINALS", "SEMIFINALS", 4],
    ["FINALE", "FINALE", 4],
]




start_date = datetime(1990, 1, 1)
end_date = datetime(2025, 12, 31, 23, 59, 59)

ongoing_start_date = datetime(2005, 1, 1)
ongoing_end_date = datetime(2010, 12, 31, 23, 59, 59)

def get_team_dict(team):
    return {
        "name": team[0],
        "officialName": team[1],
        "slug": team[2],
        "abbreviation": team[3],
        "teamCountryCode": team[4],
        "stagePosition": None,
    }

def get_results(home_team, away_team, status):
    if status == "scheduled":
        home_goals = away_goals = 0
        winner = None
    elif status == "ongoing":
        home_goals = random.randint(0, 6)
        away_goals = random.randint(0, 6)
        winner = None
    else:
        home_goals = random.randint(0, 6)
        away_goals = random.randint(0, 6)
        winner = None if home_goals == away_goals else home_team if home_goals > away_goals else away_team

    return {
        "homeGoals": home_goals,
        "awayGoals": away_goals,
        "winner": winner,
        "message": None,
        "goals": [],
        "yellowCards": [],
        "secondYellowCards": [],
        "directRedCards": [],
    }

def create_match():
    delta = end_date - start_date
    random_seconds = random.randint(0, int(delta.total_seconds()))
    game_datetime = start_date + timedelta(seconds=random_seconds)

    if ongoing_start_date <= game_datetime <= ongoing_end_date:
        status = "ongoing"
    elif game_datetime < ongoing_end_date:
        status = "played"
    else:
        status = "scheduled"

    date, time = game_datetime.date(), game_datetime.time()
    season = game_datetime.year

    stadium = random.choice(stadiums)

    team1 = random.choice(football_teams)
    team2 = random.choice(football_teams)
    while team1 == team2:
        team2 = random.choice(football_teams)

    home_team = get_team_dict(team1)
    away_team = get_team_dict(team2)

    result = get_results(home_team["name"], away_team["name"], status)

    competition = random.choice(competitions)
    stage = random.choice(stages)

    match = {
        "season": season,
        "status": status,
        "timeVenueUTC": str(time),
        "dateVenue": str(date),
        "stadium": stadium,
        "homeTeam": home_team,
        "awayTeam": away_team,
        "result": result,
        "stage": {"id": stage[0], "name": stage[1], "ordering": stage[2]},
        "group": None,
        "originCompetitionId": competition[0],
        "originCompetitionName": competition[1],
    }

    return match

def main(amount):
    matches = [create_match() for _ in range(amount)]
    data = {"data": matches}
    
    with open('matches.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        amount =  int(sys.argv[1])
    else:
        exit("Specify amount of matches to be created:\n-python sportdata_generator.py [INT]AMOUNT")
    main(amount)