from selenium import webdriver
from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup
import csv

def date_range(start_date, end_date):
    for n in range((end_date - start_date).days):
        yield (start_date + timedelta(n)).strftime('%Y%m%d')

def get_games_id (start_year, start_month, start_day, end_year, end_month, end_day):
    
    games_id = []
    dates = []

    for item in date_range(date(start_year, start_month, start_day), date(end_year, end_month, end_day)):
        dates.append(item)

    driver = webdriver.Chrome()

    for day in dates:
        driver.get('http://www.espn.com.ar/futbol/resultados/_/liga/arg.1/fecha/' + day)

        game_link_driver = driver.find_elements_by_name('&lpos=soccer:scoreboard:resumen')

        game_links = []

        for i in range(len(game_link_driver)):
            game_links.append(game_link_driver[i].get_attribute('href'))

        for game in game_links:
            games_id.append(game[46:53])

        driver.quit

    return games_id

def teams (id):

    url = 'http://www.espn.com.ar/futbol/numeritos?juegoId=' + str(id)

    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')

    teams_html = soup.find_all("div", {"class":"possession"})

    if not teams_html:
    	return None

    # Team Names
    for item in teams_html:
        name = item.find_all('span',{"class":"team-name"})

    team_names = [n.contents[0] for n in name]

    return team_names

def score (id):

    url = 'http://www.espn.com.ar/futbol/numeritos?juegoId=' + str(id)

    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')

    # Home Score
    home_html = soup.find_all("span", {"class":"score icon-font-after"})
    if not len(home_html):
        return None

    home_contents = [p.contents[0] for p in home_html]

    home_score_string = (home_contents[0].strip())

    if not len(home_score_string):
        return None

    home_score = int(home_score_string)

    # Away Score
    away_html = soup.find_all("span", {"class":"score icon-font-before"})

    away_contents = [p.contents[0] for p in away_html]

    away_score_string = (away_contents[0].strip())

    if not len(away_score_string):
        return None

    away_score = int(away_score_string)

    return [home_score, away_score]


def goals (id):

	url = 'http://www.espn.com.ar/futbol/comentario?juegoId=' + str(id)

	r = requests.get(url)
	soup = BeautifulSoup(r.content,'html.parser')

	#goals
	goals_html = soup.find_all("ul", {"data-event-type":"goal"})

	if not len(goals_html):
		return None

	list_html = []

	for tag in goals_html:
   		list_html.append(tag.find_all("li"))

   	goal_scorers = []

	for content in list_html:
		goal_contents = [ p.contents[0] for p in content ]
		for scorer in goal_contents:
			goal_scorers.append(scorer.strip())

	minutes_html = []

	for tag in goals_html:
   		minutes_html.append(tag.find_all("span"))

   	minutes_scored_raw = []

	for content in minutes_html:
		minutes_contents = [ p.contents[0] for p in content ]
		for minute in minutes_contents:
			minutes_scored_raw.append(minute)

	goals_scored_raw = {}
	goals_scored = {}

	for i in range (len(goal_scorers)):
		goals_scored_raw[goal_scorers[i]] = minutes_scored_raw[i]
	
	if not len(players_html):
		return None

	players_contents = [ p.contents[0] for p in players_html ]

	home_players = []
	away_players = []

	for num in range(18):
		home_players.append(players_contents[num].strip())
	for number in range(18,len(players_contents)):
		away_players.append(players_contents[number].strip())

    # goles en tiempo de descuento o en contra

    for key in goals_scored_raw.keys():
        if 'OG' in goals_scored_raw[key]:
            if key in home_players:
                goals_scored[away_players[0]] = goals_scored_raw[key]
            elif key in away_players:
                goals_scored[home_players[0]] = goals_scored_raw[key]
        elif '+' in goals_scored_raw[key]:
            index = goals_scored_raw[key].index('+')
            goals_scored[key] = str(int(goals_scored_raw[key][index-3:index-1]) + int(goals_scored_raw[key][index+1])) + "'"
        else:
            goals_scored[key] = goals_scored_raw[key]

    # Goals Attribution

	home_goals_raw = []
	away_goals_raw = []

	for key in goals_scored.keys():
		if key in home_players:
			home_goals_raw.append(goals_scored[key])
		else:
			away_goals_raw.append(goals_scored[key])

	home_goals = []
	away_goals = []

	for element in home_goals_raw:
		for i in range(len(element)):
			if element[i] == "'":
				if element[i-2] == '(':
					 home_goals.append(int(element[i-1]))
				else:
					home_goals.append(int(element[i-2:i]))

	for element in away_goals_raw:
		for i in range(len(element)):
			if element[i] == "'":
				if element[i-2] == '(':
					 away_goals.append(int(element[i-1]))
				else:
					away_goals.append(int(element[i-2:i]))

	home_goals_sorted = sorted(home_goals)
	away_goals_sorted = sorted(away_goals)

	if len(home_goals_sorted) < 2 and len(away_goals_sorted) < 2:
		return None

	elif not len(home_goals_sorted):
		two_zero = 'away'

	elif not len(away_goals_sorted):
		two_zero = 'home'

	elif len(home_goals_sorted) == 1:
		if away_goals_sorted[1] < home_goals_sorted[0]:
			two_zero = 'away'
		else:
			return None
	elif len(away_goals_sorted) == 1:
		if home_goals_sorted[1] < away_goals_sorted[0]:
			two_zero = 'home'
		else:
			return None
	else:
		if away_goals_sorted[1] < home_goals_sorted[0]:
			two_zero = 'away'
		elif home_goals_sorted[1] < away_goals_sorted[0]:
			two_zero = 'home'
		else:
			return None

	return two_zero

def write_to_csv (games):
      writer = csv.writer(csv_file)
      writer.writerows(games)

#Program

games_id = get_games_id (2014, 1, 1, 2015, 1, 1)

list_of_games_data = []

for game in games_id:
	print game
	goal_data = goals(game)
	score_data = score(game)
	teams_data = teams(game)
	if goal_data and teams_data and score_data:
		score_data.append(goal_data) 
		score_data.append(teams_data[0])
		score_data.append(teams_data[1])
		list_of_games_data.append (score_data)

row_names = ['home_score', 'away_score', 'two_zero', 'home_team', 'away_team']

with open('games_data_score.csv', 'w') as csv_file:
    write_to_csv([row_names])

    for game in list_of_games_data:
        write_to_csv([game])