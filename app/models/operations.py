# INSERT INTO TABLES


def addSport(cursor: object, data: dict):
    """
    Inserts sport into sports

    @param {Object} cursor - object to execute queries
    @param {Object} data - data with sports details

    """

    query: str = """
    INSERT OR IGNORE INTO sports (sport_name)
    VALUES (?)
    """
    cursor.execute(query, data["sportName"])


def addCompetition(cursor: object, data: dict):
    """
    Inserts competition into competitions

    @param {Object} cursor - object to execute queries
    @param {Object} data - data with competition details

    """
    
    query: str = """
    INSERT OR IGNORE INTO competitions (competition_id, competition_name)
    VALUES (?, ?)
    """
    cursor.execute(
        query,
        (
            data["competitionId"],
            data["competitionName"],
        ),
    )


def addStage(cursor: object, data: dict):
    """
    Inserts stage into stages

    @param {Object} cursor - object to execute queries
    @param {Object} data - data with stage details

    """

    query: str = """
    INSERT OR IGNORE INTO stages (stage_id, stage_name, stage_ordering)
    VALUES (?, ?, ?)
    """
    cursor.execute(
        query,
        (
            data["id"],
            data["name"],
            data["ordering"],
        ),
    )


def addTeam(cursor: object, data: dict, foreignIds: dict):
    """
    Inserts team into teams

    @param {Object} cursor - object to execute queries
    @param {Object} data - data with team details
    @param {Object} foreignIds - primary keys of stages and sports

    """

    query: str = """
    INSERT OR IGNORE INTO teams (name, official_name, slug, abbreviation, team_country_code, _stage_id, _sport_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(
        query,
        (
            data["name"],
            data["officialName"],
            data["slug"],
            data["abbreviation"],
            data["teamCountryCode"],
            foreignIds["stageId"],
            foreignIds["sportId"],
        ),
    )

    teamId = cursor.lastrowid

    return teamId


def addMatch(cursor: object, data: dict):
    """
    Inserts match into matches

    @param {Object} cursor - object to execute queries
    @param {Object} data - data with match details

    """

    query: str = """
    INSERT OR IGNORE INTO matches (season, status, stadium, time_venue_utc, date_venue, _home_team_id, _away_team_id, _stage_id, _sport_id, _competition_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(
        query,
        (
            data["season"],
            data["status"],
            data["stadium"],
            data["timeVenueUTC"],
            data["dateVenue"],
            data["homeTeamId"],
            data["awayTeamId"],
            data["stageId"],
            data["sportId"],
            data["competitionId"],
        ),
    )

    matchId = cursor.lastrowid
    return matchId


def addMatchResults(cursor: object, data: dict, matchId: int):
    """
    Inserts match results

    @param {Object} cursor - object to execute queries
    @param {Object} data - data with match results
    @param {int} matchId - primary key of match

    """
    query: str = """
    INSERT OR IGNORE INTO match_results (home_goals, away_goals, message, _winner_team_id, _match_id)
    VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(
        query,
        (
            data["homeGoals"],
            data["awayGoals"],
            data["message"],
            data["winner"],
            matchId,
        ),
    )

    pass


# READ


def getSportId(cursor: object, sport_name: str):
    """
    Returns sport ID on sport name

    @param {Object} cursor - object to execute queries
    @param {str} sport_name - name of competition

    @returns {int, None} - returns sport id if found else None
    """
    query: str = """
    SELECT sport_id FROM sports WHERE sport_name = ?
    """
    cursor.execute(query, (sport_name,))

    sportId = cursor.fetchone()
    if sportId:
        return sportId[0]

    return None


def getCompetitionId(cursor: object, competition_name: str):
    """
    Returns competition ID on competition name

    @param {Object} cursor - object to execute queries
    @param {str} competition_name - name of competition

    @returns {int, None} - returns competition id if found else None
    """
    query: str = """
    SELECT stage_id FROM stages WHERE competition_name = ?
    """
    cursor.execute(query, (competition_name,))

    competitionId = cursor.fetchone()
    if competitionId:
        return competitionId[0]

    return None


def getStageId(cursor: object, stage_name: str):
    """
    Returns stage ID on stage name

    @param {Object} cursor - object to execute queries
    @param {str} stage_name - name of stage

    @returns {int, None} - returns stage id if found else None
    """
    query: str = """
    SELECT stage_id FROM stages WHERE stage_name = ?
    """
    cursor.execute(query, (stage_name,))

    stageId = cursor.fetchone()
    if stageId:
        return stageId[0]

    return None


def getTeamId(cursor: object, name: str):
    """
    Returns Team ID on team name

    @param {Object} cursor - object to execute queries
    @param {str} name - name of team

    @returns {int, None} - returns team id if found else None
    """
    query: str = """
    SELECT team_id FROM teams WHERE name = ?
    """
    cursor.execute(query, (name,))

    teamId = cursor.fetchone()
    if teamId:
        return teamId[0]

    return None


def checkMatchExists(cursor: object, home_team_id, away_team_id, timeVenue, dateVenue):
    """
    Checks if a match already exists based on if team is already playing on the same date + time

    @param {int} home_team_id - ID of home team
    @param {int} away_team_id - ID of away team
    @param {int} timeVenue - unix timestamp of datetime # YYYY-mm-dd HH-MM-SS
    @param {int} dateVenue - unix timestamp of date # YYYY-mm-dd 00:00:00

    @returns {bool} - returns True of match already exists else False
    """
    query: str = """
    SELECT match_id FROM matches WHERE
    ((_home_team_id = ?) OR (_away_team_id = ?)) AND (time_venue_utc = ?) AND (date_venue = ?)
    """

    cursor.execute(
        query,
        (
            home_team_id,
            away_team_id,
            timeVenue,
            dateVenue,
        ),
    )
    matches = cursor.fetchall()

    if matches:
        return True
    return False


def printAllMatches(connection):
    """
    prints all matches from table matches
    
    @param {Object} connection - connection to database
    """
    cursor = connection.cursor()
    query = """
    SELECT * FROM matches
    """
    cursor.execute(query)

    rows = cursor.fetchall()

    for row in rows:
        print(row)


def getCompetitionNames(connection: object):
    """
    Returns all competition names from competitions

    @param {Object} connection - connection to database

    @returns {Object} - returns List of all competition names
    """
    cursor: object = connection.cursor()

    query: str = """
    SELECT competition_name FROM competitions
    """

    cursor.execute(query)

    competitions = cursor.fetchall()
    if competitions:
        return competitions

    return []


def getMatchesWithParameter(connection: object, data):
    """
    Returns all specified matches

    @param {Object} connection - connection to database
    @param {Object} data - dict with all parameters
    
    @returns {Object} - returns List of all specified matches
    """
    cursor = connection.cursor()

    query: str = """
    SELECT 
    m.season,
    m.status,
    m.stadium,
    m.time_venue_utc,
    m.date_venue,
    ht.official_name,
    at.official_name,
    sport.sport_name,
    comp.competition_name,
    stages.stage_name,
    mr.home_goals,
    mr.away_goals
    FROM matches m
    LEFT JOIN teams ht ON m._home_team_id = ht.team_id
    LEFT JOIN teams at ON m._away_team_id = at.team_id
    LEFT JOIN sports sport ON m._sport_id = sport.sport_id
    LEFT JOIN competitions comp ON m._competition_id = comp.competition_id
    LEFT JOIN stages stages ON m._stage_id = stages.stage_id
    LEFT JOIN match_results mr ON m.match_id = mr._match_id
    WHERE
    (m.date_venue BETWEEN ? AND ? OR ? IS NULL OR ? IS NULL) AND
    (m.status IN (?, ?, ?)) AND
    (m.stadium LIKE ? OR ? IS NULL) AND
    (ht.official_name LIKE ? OR at.official_name LIKE ? OR ? IS NULL) AND
    (comp.competition_name = ? OR ? IS NULL)
    ORDER BY m.time_venue_utc ASC
    LIMIT ? OFFSET ?;
    """

    cursor.execute(
        query,
        (
            data["startDate"],
            data["endDate"],
            data["startDate"],
            data["endDate"],
            data["statusScheduled"],
            data["statusOngoing"],
            data["statusPlayed"],
            data["venueName"],
            data["venueName"],
            data["teamName"],
            data["teamName"],
            data["teamName"],
            data["competition"],
            data["competition"],
            data["limit"],
            data["offset"]
        )
    )
    matches = cursor.fetchall()

    return matches


# UPDATE

# DELETE
