from database import db_operations as dbop
from modules import analysis 
from itertools import combinations
from datetime import datetime
from modules import config
from database import tables_insertions as ti

def generate_ticket(risk, target_AKO, games_count, leagues):
    if risk is None or not leagues or games_count is None or games_count <= 0:
        return None

    games = dbop.get_all_matches_with_odds()
    filtered_games = analysis.time_filter(games)
    accepted_types = []
    tickets = []
    for game in filtered_games:
        if not analysis.league_filter(game["league_name"], leagues):
            continue
        single_game = analysis.count_real_probability(game)
        for odd_name in single_game:
            individual_ev = analysis.count_individual_ev(single_game, odd_name)
            if analysis.individual_ev_filter(individual_ev):
                accepted_types.append({
                    "match_id": single_game[odd_name]["match_id"],
                    "type": odd_name,
                    "real_prob": single_game[odd_name]["real_prob"],
                    "offered_odd": single_game[odd_name]["offered_odd"],
                    "outcome_name": single_game[odd_name]["outcome_name"],
                    "individual_ev": individual_ev,
                })
    for combination in combinations(accepted_types, games_count):
        if not analysis.odd_filter(combination) or not analysis.conflicts_filter(combination):
            continue
        ev = analysis.count_ev(combination)
        kelly = analysis.count_kellys_criterion(risk, ev, games_count)
        if kelly == 0.0 or abs(target_AKO - ev["combined_odd"]) > config.MAX_AKO_DIFF:
            continue
        tickets.append({
            "types": combination,
            "ev": ev["ev"],
            "combined_odd": ev["combined_odd"],
            "kelly": kelly,
        })
    sorted_tickets = sorted(tickets, key=lambda x: x['ev'], reverse=True)
    if not sorted_tickets:
        return None
    ticket_id = ti.insert_ticket(config.DB_NAME, {
        "target_ako": target_AKO,
        "actual_ako": sorted_tickets[0]["combined_odd"],
        "risk_level": risk,
        "created_at": datetime.now(),
        "status": "generated"
    })
    for bet in sorted_tickets[0]["types"]:
        odd_id = dbop.get_odd_id(bet["match_id"], bet["outcome_name"])
        ti.insert_ticket_item(config.DB_NAME, ticket_id, odd_id)
    return sorted_tickets[0]
