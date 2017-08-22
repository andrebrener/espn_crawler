# Football Analytics

Get information from football games for different competitions and other graphs to analyze teams & players. The scripts are written and intended to use with Python 3.

## Getting Started

### 1. Clone Repo

`git clone https://github.com/andrebrener/football_data.git`

### 2. Install Packages Required

Go in the directory of the repo and run:
```pip install -r requirements.txt```

### 3. Enjoy the repo :)

## What can you do?

### 1. Get Games Data
- Insert Constants in constants.py
  - Select start & end dates.
   Select competition from the competition dictionary.
- Run [game_data.py](https://github.com/andrebrener/football_data/blob/master/game_data.py).
- A directory named `game_data` will be created in the repo with a csv file named `games_data_<start_date>_<end_date>.csv`.
- This csv will contain the data for the games of the selected competition and dates including:
  - Date of the game.
  - Home & away teams.
  - Result of the game.
  - Total shots and shots on goal.
  - Percentage ball possessions.
  - Fouls and yellow & red cards.
  - Team who made the first goal.
  - Team that was 2-0 in any moment of the game. This value is null if no team complies with this condition.
  - Number of penalties per team.
