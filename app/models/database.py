import sqlite3
import os
from typing import Dict, List


from models.operations import *
from utility.utility import dateToUnix

def addSportIfNeeded(cursor: object, gameData: dict):
    """
    Add sport if not None and not already exists

    @param {Object} cursor - object to execute queries
    @param {dict} gameData - Data of game
    """
    if "sport" in gameData:
        print("CREATE NEW SPORT")
        addSport(cursor, gameData["sport"])


def addCompetitionIfNeeded(cursor: object, gameData: dict):
    """
    Add competition if it not exists and returns it

    @param {Object} cursor - object to execute queries
    @param {dict} gameData - Data of game

    @returns {dict} competition - dict with competition id and name
    """
    competition = {
        "competitionId": gameData["originCompetitionId"],
        "competitionName": gameData["originCompetitionName"],
    }
    
    competitionId = getCompetitionId(cursor, competition["competitionName"])
    
    if not competitionId:
        competitionId = addCompetition(cursor, competition)
        
    return competition


def addStageIfNeeded(cursor: object, gameData: dict):
    """
    Add new stage if not None and not already exists

    @param {Object} cursor - object to execute queries
    @param {dict} gameData - Data of game
    """
    
    stageId = getStageId(cursor, gameData["stage"]["name"])
    
    if stageId: return
    
    if "stage" in gameData:
        addStage(cursor, gameData["stage"])


def getStageSportId(cursor: object, gameData: dict):
    """
    Get dict with stage and sport ids

    @param {Object} cursor - object to execute queries
    @param {dict} gameData - Data of game

    @returns {dict} stageSportId - dict with stage and sport id
    """
    stageSportId = {
        "stageId": getStageId(cursor, gameData["stage"]["name"]),
        "sportId": getSportId(cursor, gameData["sport"] if "sport" in gameData else ""),
    }

    return stageSportId


def getOrAddTeam(cursor: object, teamData: dict, stageSportId: dict):
    """
    Gets teamId if team exists else create new team and get its id

    @param {Object} cursor - object to execute queries
    @param {dict} teamData - data of team
    @param {dict} stageSportId - both stage and sport id in a dict

    @returns {int} teamId - Id of team
    """
    teamId = getTeamId(cursor, teamData["name"])

    if not teamId:
        teamId = addTeam(cursor, teamData, stageSportId)
    return teamId



def getMatchData(cursor: object, gameData: dict, competition: dict):
    """
    Configures match data

    @param {Object} cursor - object to execute queries
    @param {dict} gameData - Data of game
    @param {dict} competition - competition id and name in a dict

    @returns {dict} matchData - data that contains all match infos
    """
    
    timeVenueUTC_unix = dateToUnix(f"{gameData["dateVenue"]} {gameData["timeVenueUTC"]}")
    dateVenue_unix = dateToUnix(f"{gameData["dateVenue"]} 00:00:00")
    
    matchData = {
        "season": gameData["season"],
        "status": gameData["status"],
        "timeVenueUTC": timeVenueUTC_unix,
        "dateVenue": dateVenue_unix,
        "stadium": gameData["stadium"],
        "homeTeamId": None,
        "awayTeamId": None,
        "stageId": None,
        "sportId": None,
        "competitionId": competition["competitionId"],
    }


    stageSportId = getStageSportId(cursor, gameData)
    matchData["stageId"] = stageSportId["stageId"]
    matchData["sportId"] = stageSportId["sportId"]

    if gameData.get("homeTeam"):
        matchData["homeTeamId"] = getOrAddTeam(
            cursor, gameData["homeTeam"], stageSportId
        )

    if gameData.get("awayTeam"):
        matchData["awayTeamId"] = getOrAddTeam(
            cursor, gameData["awayTeam"], stageSportId
        )

    return matchData


def addResultsIfNeeded(cursor: object, gameData: dict, matchId: int):
    """
    Add Match results if not None

    @param {Object} cursor - object to execute queries
    @param {dict} gameData - Data of game
    @param {int} matchId - matchId for results

    """
    if gameData.get("result"):
        addMatchResults(cursor, gameData["result"], matchId)


def addAllBasedOnOneEvent(connection: object, gameData: dict):
    """
    Inserts new sports, competitions, stages, matches, results based on game given if these don´t exist already

    @param {Object} connection - connection object to database
    @param {dict} gameData - information about game

    @returns {dict} - success: bool, message: info text, data: matchData
    """
    cursor: object = connection.cursor()

    try:

        addSportIfNeeded(cursor, gameData)
        competition = addCompetitionIfNeeded(cursor, gameData)
        addStageIfNeeded(cursor, gameData)

        matchData = getMatchData(cursor, gameData, competition)
        
        matchExists = checkMatchExists(cursor, matchData["homeTeamId"], matchData["awayTeamId"], matchData["timeVenueUTC"], matchData["dateVenue"])
        
        if matchExists:
            print("Match already exists!")
            return {'success': False, 'message': "Match already exists / Team already plays at same time.", 'data': matchData}
            
        matchId = addMatch(cursor, matchData)
        addResultsIfNeeded(cursor, gameData, matchId)
        
        return {'success': True, 'message': "Match inserted successfully.", 'data': matchData}

    except Exception as error:
        print(f"Error: {repr(error)}")
        cursor.close()
        connection.rollback()

    finally:
        connection.commit()


def createAllTables(connection: object):
    """
    Creates all tables if not already exists based on ERD
    
    @param {Object} connection - connection to database
    """

    cursor: object = connection.cursor()

    sportsQuery: str = """
    CREATE TABLE IF NOT EXISTS sports (
        sport_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sport_name TEXT NOT NULL
    );
    """
    cursor.execute(sportsQuery)

    competitionsQuery: str = """
    CREATE TABLE IF NOT EXISTS competitions (
        competition_id TEXT PRIMARY KEY,
        competition_name TEXT NOT NULL
    );
    """
    cursor.execute(competitionsQuery)

    stagesQuery: str = """
    CREATE TABLE IF NOT EXISTS stages (
        stage_id TEXT PRIMARY KEY,
        stage_name TEXT NOT NULL,
        stage_ordering INTEGER NOT NULL
    );
    """
    cursor.execute(stagesQuery)

    teamsQuery: str = """
    CREATE TABLE IF NOT EXISTS teams (
        team_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        official_name TEXT NOT NULL,
        slug TEXT NOT NULL,
        abbreviation TEXT NOT NULL,
        team_country_code TEXT,
        _stage_id INTEGER,
        _sport_id INTEGER,
        FOREIGN KEY (_stage_id) REFERENCES stages(stage_id),
        FOREIGN KEY (_sport_id) REFERENCES sports(sport_id)
    );
    """
    cursor.execute(teamsQuery)

    matchesQuery: str = """
    CREATE TABLE IF NOT EXISTS matches (
        match_id INTEGER PRIMARY KEY AUTOINCREMENT,
        season INTEGER,
        status TEXT NOT NULL,
        stadium TEXT,
        time_venue_utc INTEGER NOT NULL,
        date_venue INTEGER NOT NULL,
        _home_team_id INTEGER,
        _away_team_id INTEGER,
        _stage_id INTEGER,
        _sport_id INTEGER,
        _competition_id TEXT,
        FOREIGN KEY (_home_team_id) REFERENCES teams(team_id),
        FOREIGN KEY (_away_team_id) REFERENCES teams(team_id),
        FOREIGN KEY (_stage_id) REFERENCES stages(stage_id),
        FOREIGN KEY (_sport_id) REFERENCES sports(sport_id),
        FOREIGN KEY (_competition_id) REFERENCES competitions(competition_id)
    );
    """
    cursor.execute(matchesQuery)

    matchResultsQuery: str = """
    CREATE TABLE IF NOT EXISTS match_results (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        home_goals INTEGER,
        away_goals INTEGER,
        message TEXT,
        _winner_team_id INTEGER,
        _match_id INTEGER NOT NULL,
        FOREIGN KEY (_winner_team_id) REFERENCES teams(team_id),
        FOREIGN KEY (_match_id) REFERENCES matches(match_id)
    );
    """
    cursor.execute(matchResultsQuery)

    cursor.close()

    return


def initDatabase(database_path: str):
    """
    Initialize database
    Creates all tables if not already exists and commits them
    Rollback any changes if error occurs
    """
    databaseExists: bool = os.path.isfile(database_path)

    if databaseExists:
        return

    try:
        connection = sqlite3.connect(database_path)
        createAllTables(connection)
        connection.commit()

    except Exception as e:
        print(f"Error in init: {repr(e)}")
        connection.rollback()

    finally:
        connection.close()

    return
