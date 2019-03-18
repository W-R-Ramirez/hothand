from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Team
from datetime import timezone

def utc_to_local(utc):
    return utc.replace(tzinfo=timezone.utc).astimezone(tz=None)

URL = ""
team2acr = {"CLEVELAND CAVALIERS": "CLE", 'ATLANTA HAWKS': "ATL", 'BOSTON CELTICS': 'BOS', 'BROOKLYN NETS': 'NJN','NEW YORK KNICKS': 'NYK', 'NEW ORLEANS PELICANS': 'NOH', 'LOS ANGELES LAKERS': 'LAL', 'CHICAGO BULLS': 'CHI', 'ATLANTA HAWKS': 'ATL', 'PORTLAND TRAIL BLAZERS': 'POR','OKLAHOMA CITY THUNDER': 'OKC', 'MEMPHIS GRIZZLIES': 'MEM', 'HOUSTON ROCKETS': 'HOU', 'MINNESOTA TIMBERWOLVES': 'MIN','DENVER NUGGETS': 'DEN','DALLAS MAVERICKS': 'DAL', 'CHARLOTTE HORNETS': 'CHA', 'DETROIT PISTONS': 'DET', 'GOLDEN STATE WARRIORS': 'GSW', 'LOS ANGELES CLIPPERS': 'LAC', 'MIAMI HEAT': 'MIA', 'MILWAUKEE BUCKS': 'MIL', 'ORLANDO MAGIC': 'ORL', 'PHILADELPHIA 76ERS': 'PHI', 'PHOENIX SUNS': 'PHO', 'SACRAMENTO KINGS' : 'SAC', 'SAN ANTONIO SPURS': 'SAS', 'TORONTO RAPTORS': 'TOR', 'UTAH JAZZ': 'UTA', 'WASHINGTON WIZARDS' : 'WAS', 'INDIANA PACERS': 'IND'}

game_URLS = []

for game in client.season_schedule(season_end_year = 2018):
    start = game['start_time']
    start = utc_to_local(start)## FORMAT SO IT HAS RIGHT DATE
    #print(game['home_team'].value)
    if game['home_team'].value in team2acr:
        URL = str(start.year)+str(start.month).zfill(2)+str(start.day).zfill(2)+"0"+team2acr[game['home_team'].value]
        game_URLS.append(URL)


f = open("games_URLS.txt", "w+")

for game in game_URLS:
    f.write(game + "\n")
