from flask import Flask, render_template
from datetime import date, timedelta
import requests

app = Flask(__name__)

@app.route('/')

def get_this_weeks_boss():
    try:
        response = requests.get("https://data.ninjakiwi.com/btd6/bosses")
        response.raise_for_status() #Raise HTTPError if status code was unseccessful
        bosses = response.json()['body']
        
        today = date.today()
        start_of_week, end_of_week = today - timedelta(today.weekday()), today + timedelta(6 - today.weekday()) #Calculate start of the week and end of the week monday = 0 and sunday = 6
        
        for boss in bosses:
            boss_start, boss_end = date.fromtimestamp(boss['start'] / 1000), date.fromtimestamp(boss['end'] / 1000) #Unix timestamp in miliseconds
            
            #Ensure the boss period dosent overlap
            if boss_start <= end_of_week and boss_end >= start_of_week:
                boss_name = boss['name']
                boss_date_range = f"{boss_start} to {boss_end}"
                boss_image = boss['bossTypeURL']
                return render_template('boss.html', boss_name=boss_name, boss_date_range=boss_date_range, boss_image=boss_image)
            
        return "No boss this week."

    except requests.RequestException:
        return "Error fetching the boss data"
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
