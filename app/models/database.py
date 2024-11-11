import sqlite3
from typing import Dict, List
import yaml
import os

database_path: str = ""

def createAllTables(connection: object):
    
    """
    Creates all tables if not already exists
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
        stage_id INTEGER PRIMARY KEY AUTOINCREMENT,
        stage_name TEXT NOT NULL
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
        stadium TEXT NOT NULL,
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



def initDatabase():
    """
    Initialize database by loading database path from config file
    Creates all tables if not already exists and commits them
    Rollback any changes if error occurs
    """
    global database_path
    
    with open('config/config.yaml', 'r') as file:
        data: Dict = yaml.safe_load(file)
        database_path = data['database_path']
        
    databaseExists: bool = os.path.isfile(database_path)
    
    if databaseExists: return
        
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