from datetime import datetime, timezone

def dateToUnix(date):
    """
    Converts input to timestamp
    
    @param {string} date - Date + Time in Format "YYYY-MM-DD HH:MM:SS"
    
    @returns {int} - unix timestamp of date
    """
    formattedDate = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    return int(formattedDate.timestamp())

def getFormattedParams(data):
    
    # Set "" values to None
    for key, value in data.items():
        if value == "":
            data[key] = None
    
    # format string to list
    if data.get('status') == None:
        data['status'] = []
    else:
        data['status'] = data['status'].split(",")
    
    startDate_unix = None
    endDate_unix = None
    
    if data['startDate']: startDate_unix = dateToUnix(f'{data['startDate']} 00:00:00') 
    if data['endDate']: endDate_unix = dateToUnix(f'{data['endDate']} 00:00:00')
    
    status = [*data['status'], None, None, None][:3]
    
    venueName = f"%{data.get('venueName')}%" if data.get('venueName') else None
    teamName = f"%{data.get('teamName')}%" if data.get('teamName') else None

    params = {
        'startDate': startDate_unix,
        'endDate': endDate_unix,
        'statusScheduled': status[0],
        'statusOngoing': status[1],
        'statusPlayed': status[2], 
        'venueName': venueName,
        'teamName': teamName,
        'competition': data['competition']
    }
    
    return params