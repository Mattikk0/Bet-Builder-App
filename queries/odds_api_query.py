import aiohttp
import asyncio
from datetime import datetime, date
from modules.config import API_KEY, API_URL, LEAGUES
from database.tables_insertions import insert_match, insert_odd, insert_sync_log
from database.db_operations import check_update_time

async def fetch_league_odds(session, league):
    url = f"{API_URL}/v4/sports/{league}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h"
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        return None

async def get_odds():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for league in LEAGUES:
            if check_update_time(league):
                print("Updating database...")
                tasks.append(fetch_league_odds(session, league))
        if tasks:
            results = await asyncio.gather(*tasks)      
            return [res for res in results if res is not None]
        else:
            return None

def send_query_data_to_db(response):
    db_name = "bet-builder-db"

    for league_matches in response:
        ctr = 0
        for match in league_matches:
            match_data = {
                "league_name": match.get("sport_key"),
                "home_team": match.get("home_team"),
                "away_team": match.get("away_team"),
                "commence_time": datetime.fromisoformat(
                    match["commence_time"].replace("Z", "+00:00")
                ),
                "status": "scheduled",
            }
            if ctr == 0:
                sync_log = {
                    "league_name": match.get("sport_key"),
                    "last_update": date.today(),
                }
                insert_sync_log(db_name, sync_log)
            match_id = insert_match(db_name, match_data)

            for bookmaker in match.get("bookmakers", []):
                if bookmaker.get("key") == "betclic_fr":
                    for market in bookmaker.get("markets", []):
                        updated_at = datetime.fromisoformat(
                            market.get(
                                "last_update",
                                bookmaker["last_update"],
                            ).replace("Z", "+00:00")
                        ).date()
                        for outcome in market.get("outcomes", []):
                            odd_data = {
                                "market": market.get("key"),
                                "outcome_name": outcome.get("name"),
                                "price": outcome.get("price"),
                                "updated_at": updated_at,
                            }
                            insert_odd(db_name, match_id, odd_data)
            ctr+=1

