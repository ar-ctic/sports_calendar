# Sports Match Tracking System

A Flask-based web application for tracking and managing sports matches, competitions, and results. The system provides a RESTful API for match data management and a web interface for viewing and filtering matches.

# Features
* Upload match data via JSON files
* Track matches across different sports and competitions
* Filter matches by:
    * Date range
    * Match status (Scheduled, Ongoing, Played)
    * Venue name
    * Team name
    * Competition

# Technical Stack
* Backend: Python/Flask
* Database: SQLite
* Frontend: HTML with JavaScript

# Project Structure
```
├── config/
│   └── config.yaml         # Database configuration
├── models/
│   ├── database.py         # Database initialization and core operations
│   └── operations.py       # Database CRUD operations
├── utility/
│   └── utility.py          # Helper functions
├── views/
│   └── index.html          # Main frontend template
├── static/     
│   ├── index.css           # Main frontend css
│   └── index.js            # Main Fronted JS
│           
└── server.py               # Main Flask application
```

# Database Schema
![ERD](https://github.com/ar-ctic/sports_calendar/blob/main/images/sports_calendar_erd.PNG?raw=true, "Database ERD")

# Setup and Installation
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv/Scripts/activate
   ```
3. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
4. Configure database path in config/config.yaml
5. Run the application:
   ```bash
   python server.py
   ```
The server will start on http://localhost:5000

# JSON Upload Format
Match data should be uploaded in the following format:
```json
{
  "data": [
    {
      "sport": "",
      "originCompetitionId": "",
      "originCompetitionName": "",
      "stage": {
        "id": "",
        "name": "",
        "ordering": 0
      },
      "season": "",
      "status": "",
      "dateVenue": "",
      "timeVenueUTC": "",
      "stadium": "",
      "homeTeam": {
            "name": "",
            "officialName": "",
            "slug": "",
            "abbreviation": "",
            "teamCountryCode": ""
      },
      "awayTeam": {
            "name": "",
            "officialName": "",
            "slug": "",
            "abbreviation": "",
            "teamCountryCode": ""
      },
      "result": {
            "homeGoals": 0,
            "awayGoals": 0,
            "winner": "",
            "message": "",
      }
    }
  ]
}
```

## Generating Data
To generate random sportdata execute:
```bash
python sportdata_generator.py [INT]AMOUNT
```

## Thoughts
For this challenge, I opted for a relational database design, which involves creating separate tables for entities like teams, competitions, stages etc. This structure ensures consistency, reduces redundancy, and establishes clear relationships between events and their associated details. By normalizing the data, I can maintain uniformity, such as consistent team names or venue information across all records. While this approach adds some complexity to queries and data entry, it provides a strong foundation for scalability and maintainability.