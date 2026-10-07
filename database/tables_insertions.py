import psycopg
from modules.config import DB_PARAMS

def insert_sync_log(db_name, data):
    params = {**DB_PARAMS, "dbname": db_name}
    query = """
        INSERT INTO sync_logs
            (league_name, last_update)
        VALUES (%s, %s)
    """
    values = (
        data["league_name"],
        data["last_update"],
    )
    with psycopg.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)

def insert_match(db_name, data):
    params = {**DB_PARAMS, "dbname": db_name}
    query = """
        INSERT INTO matches
            (league_name, home_team, away_team, commence_time, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """
    values = (
        data["league_name"],
        data["home_team"],
        data["away_team"],
        data["commence_time"],
        data["status"],
    )

    with psycopg.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            return cur.fetchone()[0]


def insert_odd(db_name, match_id, data):
    if match_id is None:
        raise ValueError("match_id is required to insert an odd")

    params = {**DB_PARAMS, "dbname": db_name}
    query = """
        INSERT INTO odds
            (match_id, market, outcome_name, price, updated_at)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """
    values = (
        match_id,
        data["market"],
        data["outcome_name"],
        data["price"],
        data["updated_at"],
    )

    with psycopg.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            return cur.fetchone()[0]


def insert_ticket(db_name, data):
    params = {**DB_PARAMS, "dbname": db_name}
    query = """
        INSERT INTO generated_tickets
            (target_ako, actual_ako, risk_level, created_at, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """
    values = (
        data["target_ako"],
        data["actual_ako"],
        data["risk_level"],
        data["created_at"],
        data["status"],
    )

    with psycopg.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            return cur.fetchone()[0]


def insert_ticket_item(db_name, ticket_id, odd_id):
    if ticket_id is None:
        raise ValueError("ticket_id is required to insert a ticket item")
    if odd_id is None:
        raise ValueError("odd_id is required to insert a ticket item")

    params = {**DB_PARAMS, "dbname": db_name}
    query = """
        INSERT INTO ticket_items
            (ticket_id, odd_id)
        VALUES (%s, %s)
        RETURNING id
    """
    values = (ticket_id, odd_id)

    with psycopg.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            return cur.fetchone()[0]


