import psycopg
from psycopg import sql
from modules.config import DB_PARAMS

def create_db():
    NEW_DB_NAME = "bet-builder-db"
    try:
        with psycopg.connect(**DB_PARAMS, autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM pg_database WHERE datname = %s",
                    (NEW_DB_NAME,),
                )
                if cur.fetchone() is None:
                    query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(NEW_DB_NAME))
                    cur.execute(query)
                    print(f"Created db: '{NEW_DB_NAME}'")
        return NEW_DB_NAME
    except Exception as error:
        print(f"Cannot create db: {error}")
        return None

def create_tables(db_name):
    params = {**DB_PARAMS, "dbname": db_name}
    with psycopg.connect(**params) as conn:
        with conn.cursor() as cur:
            sync_logs_query = sql.SQL("""
                CREATE TABLE IF NOT EXISTS sync_logs (
                    id SERIAL PRIMARY KEY,
                    league_name VARCHAR,
                    last_update DATE
                );
            """)
            matches_query = sql.SQL("""
                CREATE TABLE IF NOT EXISTS matches (
                    id SERIAL PRIMARY KEY,
                    league_name VARCHAR,
                    home_team VARCHAR,
                    away_team VARCHAR,
                    commence_time TIMESTAMP,
                    status VARCHAR
                );
            """)
            odds_query = sql.SQL("""
                CREATE TABLE IF NOT EXISTS odds (
                    id SERIAL PRIMARY KEY,
                    match_id INTEGER NOT NULL REFERENCES matches(id),
                    market VARCHAR,
                    outcome_name VARCHAR,
                    price FLOAT,
                    updated_at DATE
                );
            """)
            generated_tickets_query = sql.SQL("""
                CREATE TABLE IF NOT EXISTS generated_tickets (
                    id SERIAL PRIMARY KEY,
                    target_ako DECIMAL,
                    actual_ako DECIMAL,
                    risk_level VARCHAR,
                    created_at TIMESTAMP,
                    status VARCHAR
                );
            """)
            ticket_items_query = sql.SQL("""
                CREATE TABLE IF NOT EXISTS ticket_items (
                    id SERIAL PRIMARY KEY,
                    ticket_id INTEGER NOT NULL REFERENCES generated_tickets(id),
                    odd_id INTEGER NOT NULL REFERENCES odds(id)
                );
            """)
            
            cur.execute(sync_logs_query)
            cur.execute(matches_query)
            cur.execute(odds_query)
            cur.execute(generated_tickets_query)
            cur.execute(ticket_items_query)
