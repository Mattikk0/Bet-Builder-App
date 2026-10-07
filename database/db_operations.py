import psycopg
from modules.config import DB_PARAMS


def check_update_time(league_name):
	params = {**DB_PARAMS, "dbname": "bet-builder-db"}
	query = """
		SELECT last_update < CURRENT_DATE
		FROM sync_logs
		WHERE league_name = %s
			AND last_update IS NOT NULL
		ORDER BY last_update DESC
		LIMIT 1
	"""

	with psycopg.connect(**params) as conn:
		with conn.cursor() as cur:
			cur.execute(query, (league_name,))
			result = cur.fetchone()

	return result is None or bool(result[0])


def get_all_matches_with_odds():
	params = {**DB_PARAMS, "dbname": "bet-builder-db"}
	query = """
		SELECT DISTINCT ON (m.id, o.outcome_name)
			m.id, m.league_name, m.home_team, m.away_team, m.commence_time,
			o.outcome_name, o.price
		FROM matches AS m
		LEFT JOIN odds AS o ON o.match_id = m.id AND o.market = 'h2h'
		ORDER BY m.id, o.outcome_name, o.updated_at DESC NULLS LAST, o.id DESC
	"""
	matches = {}

	with psycopg.connect(**params) as conn:
		with conn.cursor() as cur:
			cur.execute(query)
			for match_id, league_name, home_team, away_team, commence_time, outcome_name, price in cur.fetchall():
				match_odds = matches.setdefault(
					match_id,
					{
						"id": match_id,
						"league_name": league_name,
						"commence_time": commence_time,
					},
				)
				if outcome_name is None:
					continue
				if outcome_name == home_team:
					match_odds[home_team] = price
				elif outcome_name == away_team:
					match_odds[away_team] = price
				elif outcome_name.lower() == "draw":
					match_odds["Draw"] = price

	return list(matches.values())


def get_odd_id(match_id, outcome_name):
	params = {**DB_PARAMS, "dbname": "bet-builder-db"}
	query = """
		SELECT id
		FROM odds
		WHERE match_id = %s AND outcome_name = %s
		LIMIT 1
	"""
	

	with psycopg.connect(**params) as conn:
		with conn.cursor() as cur:
			cur.execute(query, (match_id, outcome_name))
			result = cur.fetchone()

	return result[0] if result else None