from flask import Flask, request, render_template, jsonify, g
import sqlite3
import json
import yaml


from models.database import initDatabase, addAllBasedOnOneEvent, printAllMatches, getCompetitionNames

database_path: str = ""


app = Flask(__name__, template_folder="views", static_folder="static")


def getDatabaseConnection():
    """
    Creates database connection and returns it
    More: https://flask.palletsprojects.com/en/stable/appcontext/
    """
    if "db" not in g:
        g.db = sqlite3.connect(database_path)
    return g.db


@app.teardown_appcontext
def closeDatabaseConnection(error):
    """
    Closes database connection after request
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/", methods=["GET"])
def index():
    """
    Renders index.html for base url
    """
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    
    """
    Process uploaded file
    Get games from JSON and insert them into matches

    @returns {dict} - error message

    JSON format:
    {
        data: {
            {
                gameDetails
            },
            {
                gameDetails
            },
            .
            .
            .
        }
    }
    """
    
    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["file"]

    if not file:
        return jsonify({"message": "No selected file"}), 400

    if not file.filename.endswith(".json"):
        return (
            jsonify({"message": "Invalid file format. Please upload a .json file."}),
            400,
        )

    try:
        data: dict = json.load(file)

        if not "data" in data:
            return jsonify({"message": "File has no data keyword"}), 400

        connection = getDatabaseConnection()

        games: dict = data["data"]
        
        log = []
        for gameData in games:
            info = addAllBasedOnOneEvent(connection, gameData)
            log.append(info)
        
        printAllMatches(connection)

        return jsonify(log), 200
    except json.JSONDecodeError:
        return jsonify({"message": "Invalid JSON format"}), 400


@app.route("/getCompetitions", methods=["GET"])
def getCompetitions():
    """
    Query all competitions and return them

    @returns {dict} - Returns all available competitions or error message

    """
    connection = getDatabaseConnection()
    competitionNames = getCompetitionNames(connection)
    
    competitions = []
    for name in competitionNames:
        competitions.append(name)
    print(competitions)
    return competitions



if __name__ == "__main__":

    with open("config/config.yaml", "r") as file:
        data: dict = yaml.safe_load(file)
        database_path: str = data["database_path"]

    # Only run once when app is starting
    initDatabase(database_path)

    app.run(debug=True, port=5000)
