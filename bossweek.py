import requests
from datetime import date, timedelta

def get_this_weeks_boss():
    try:
        response = requests.get("https://data.ninjakiwi.com/btd6/bosses").json()['body']
        response.raise_for_status() #Raise HTTPError if status code was unseccessful
        bosses = response.json()['body']
        
        today = date.today()
        start_of_week, end_of_week = today - timedelta(today.weekday()), today + timedelta(6 - today.weekday()) #Calculate start of the week and end of the week monday = 0 and sunday = 6
        
        for boss in bosses:
            boss_start, boss_end = date.fromtimestamp(boss['start'] / 1000), date.fromtimestamp(boss['end'] / 1000) #Unix timestamp in miliseconds
            
            #Ensure the boss period dosent overlap
            if boss_start <= end_of_week and boss_end >= start_of_week:
                return f"Week's Boss: {boss['name']} ({boss_start} to {boss_end})"
        
        return "No boss this week."

    except requests.RequestException:
        return "Error fetching the boss data"

print(get_this_weeks_boss())