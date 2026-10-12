# Bet Builder App

A Python-based betting ticket generator that combines live sports odds, database persistence, and probability analysis to suggest optimized multi-selection bets for selected football leagues.

This project is currently a work in progress. The core backend logic, live odds ingestion, and data model are in place, but the application still needs refinement, validation, polish, and additional features before being considered production-ready.

## Overview

The application is built around a simple idea:

- fetch current odds from a sports data provider,
- store the data in a PostgreSQL database,
- analyze each betting outcome based on implied probability,
- filter and combine selections into a valid bet ticket,
- generate a ticket with the best expected value based on the user settings.

The app exposes a small Flask API and a browser-based UI to configure a ticket by risk level, target AKO, number of games, and league selection.

## Features

### Current functionality

- League and risk configuration from the frontend
- User preference controls for:
  - target AKO,
  - number of games on the ticket,
  - risk level,
  - selected leagues
- API data fetching from The Odds API for supported football competitions
- PostgreSQL database initialization and table creation
- Match and odds persistence for scheduled games
- Probability and expected value calculations
- Ticket generation using combinations of valid bets
- Filtering for:
  - time validity,
  - league relevance,
  - no conflicting selections from the same match,
  - minimum individual expected value,
  - odds ratio constraints

### Betting logic included

The project calculates:

- implied probabilities from odds,
- expected value (EV) for individual outcomes,
- combined EV across a selection ticket,
- Kelly-style staking suggestion based on risk profile,
- filtering for tickets that match the configured AKO target within a tolerance range.

This logic lives mainly in:

- `modules/analysis.py`
- `modules/ticket_creator.py`

## Project structure

```text
Bet-Builder-App/
├── app.py
├── .gitignore
├── database/
│   ├── db_auto_updates.py
│   ├── db_config.py
│   ├── db_operations.py
│   └── tables_insertions.py
├── modules/
│   ├── analysis.py
│   ├── config.py
│   └── ticket_creator.py
├── queries/
│   └── odds_api_query.py
├── static/
│   ├── assets/
│   │   ├── animations+assets.js
│   │   ├── data.js
│   │   └── styles.css
│   └── html/
│       └── index.html
└── README.md
```

## File-by-file overview

### `app.py`

This is the main Flask application entry point.

It does the following:

- serves the frontend page at `/`
- accepts POST requests at `/generate`
- creates or initializes the database,
- fetches live odds,
- generates a ticket using the configured user inputs,
- returns JSON output to the frontend.

### `modules/config.py`

Contains all central configuration values, including:

- The Odds API key and base URL,
- supported football leagues,
- database connection parameters,
- betting constants such as bankroll, risk thresholds, and AKO tolerance.

Important: `API_KEY` is currently a placeholder and must be populated before using live data.

### `queries/odds_api_query.py`

Handles fetching odds from The Odds API.

Responsibilities:

- queries league endpoints for selected sports,
- checks whether a league needs refreshing,
- normalizes bet data,
- inserts match and odd records into the database.

The data is currently focused on `h2h` markets and European football leagues.

### `database/db_config.py`

Creates the PostgreSQL database and all required tables.

Tables created include:

- `sync_logs`
- `matches`
- `odds`
- `generated_tickets`
- `ticket_items`

This is the persistence layer for all analyzed and generated betting data.

### `database/db_operations.py`

Contains database queries used across the project.

Examples:

- checking whether a league needs an update,
- retrieving all matches with odds,
- looking up the correct odd ID for a generated ticket item.

### `database/tables_insertions.py`

Handles insertion logic for all database records.

It saves:

- sync timestamps,
- match info,
- odds,
- generated tickets,
- selected ticket items.

### `modules/analysis.py`

This is the core analytical layer.

It contains functions for:

- estimating true probability from odds,
- calculating expected value,
- applying score filters,
- checking ticket conflicts,
- validating timing conditions,
- filtering by league and individual value thresholds.

### `modules/ticket_creator.py`

Creates a ticket from a filtered set of valid bet selections.

The process includes:

- loading all available matches with odds,
- applying time and league filters,
- evaluating each possible betting outcome,
- combining favorable outcomes into ticket candidates,
- sorting by expected value,
- generating the final ticket and saving it to the database.

### `static/html/index.html`

This is the frontend page for the app.

Users can choose:

- target AKO,
- ticket size (number of games),
- risk level,
- leagues.

The page includes a simple loading state and triggers a request to the backend when the user clicks the ticket-generation button.

### `static/assets/data.js`

Handles the JavaScript logic that:

- reads the user selections,
- packs them into JSON,
- sends the request to `/generate`,
- handles the server response.

### `static/assets/animations+assets.js`

Controls the visual behavior of the page, including:

- slider value updates,
- checkbox state behavior,
- mutual exclusion between risk options,
- button hover animation.

### `static/assets/styles.css`

Defines the styling of the interface, including the custom ticket configuration panel, controls, buttons, and overall layout.

## Supported leagues

The app currently targets the following competitions:

- Bundesliga
- Premier League
- Ligue 1
- Serie A
- La Liga
- Champions League
- Europa League
- Conference League

These are mapped in `modules/config.py` and used for odds queries and filtering.

## How the app works

1. The user opens the app in the browser.
2. They choose the betting parameters:
   - desired AKO,
   - number of games,
   - risk profile,
   - preferred leagues.
3. The frontend sends this configuration to the Flask backend.
4. The backend creates the PostgreSQL database if needed.
5. It fetches current odds from The Odds API.
6. Data is inserted into the database.
7. The analyzer filters and ranks valid betting opportunities.
8. The system builds a valid multi-game ticket based on expected value and constraints.
9. The generated ticket is saved and returned to the user.

## Local setup

### Requirements

- Python 3.9+
- PostgreSQL running locally
- Access to a valid The Odds API key

### Install dependencies

```bash
pip install flask flask-cors aiohttp psycopg
```

### Configuration

Edit `modules/config.py` and set:

- `API_KEY` to your The Odds API key
- `DB_PARAMS` to match your local PostgreSQL credentials if needed

Example:

```python
API_KEY = "your_api_key_here"

DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "host": "localhost",
    "password": "your_password",
    "port": 5432,
}
```

### Run the app

```bash
python app.py
```

Then open the app in the browser at:

```text
http://localhost:5000/
```

## Current status and limitations

This project is not finished yet. At the moment it is best described as an evolving betting-analysis prototype.

### What is already working

- Live odds retrieval
- Database initialization and storage
- Core probability/EV calculations
- Basic ticket generation
- Simple frontend configuration panel

### What still needs work

- Production-grade error handling
- Better UX and clearer ticket output in the frontend
- Better API validation and request feedback
- More robust odds filtering and selection logic
- Improved risk modeling and staking strategy
- Database cleanup and maintenance tooling
- Deployment configuration
- Tests and reproducible setup scripts
- Clearer documentation for operating the project in a real environment

## Future improvements

The next major milestones could include:

- UI presentation of generated ticket details and calculations
- support for more betting markets beyond `h2h`
- scheduler for live odds refreshes
- better database schema normalization
- improved user profile and bankroll tracking
- better user-facing explanations of why a ticket was selected
- deployment to a cloud service
- unit tests for analysis and ticket generation

## Notes

This repository is a technical prototype and should not be treated as a finished gambling product. The system is designed as a research and automation project for odds analysis and ticket generation, and it still requires substantial testing, validation, and refinement before broader use.

## License

No license file is currently included in the repository, so the project is effectively unlicensed unless otherwise specified by the repository owner.


This README reflects the current state of the project: a working prototype with a strong foundation, but still under active development.
