import requests
from datetime import date

def get_this_weeks_boss():
    bosses = requests.get("https://data.ninjakiwi.com/btd6/bosses").json()['body']
    current_time = date.today()
    
    for boss in bosses:
        start_date = date.fromtimestamp(boss['start'] / 1000)
        end_date = date.fromtimestamp(boss['end'] / 1000)
        
        if start_date <= current_time <= end_date:
            return f"This week's boss is {boss['name']}. Last day for this boss is {end_date}."

    return "No boss found for this week."

print(get_this_weeks_boss())

