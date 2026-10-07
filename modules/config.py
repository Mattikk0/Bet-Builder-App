# API configuration
API_KEY = "INSERT_API_KEY"
API_URL = "https://api.the-odds-api.com"

# Supported leagues
LEAGUES = [
    "soccer_epl",
    "soccer_spain_la_liga",
    "soccer_italy_serie_a",
    "soccer_germany_bundesliga",
    "soccer_france_ligue_one",
    "soccer_uefa_champs_league",
    "soccer_uefa_europa_league",
    "soccer_uefa_europa_conference_league",
]

LEAGUES_MAP = {
    "Bundesliga": "soccer_germany_bundesliga",
    "Premier League": "soccer_epl",
    "Ligue 1": "soccer_france_ligue_one",
    "Serie A": "soccer_italy_serie_a",
    "La Liga": "soccer_spain_la_liga",
    "Champions League": "soccer_uefa_champs_league",
    "Europa League": "soccer_uefa_europa_league",
    "Conference League": "soccer_uefa_europa_conference_league",
}

# Database configuration
DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "host": "localhost",
    "password": "12345678",
    "port": 5432
}

DB_NAME = "bet-builder-db"

# Betting constants 
BANKROLL = 10000.0
MAX_BET_PERCENT = 0.03
MIN_SINGLE_EV = -0.08
MAX_ODDS_RATIO = 2.0
MAX_AKO_DIFF = 1.5
