### RISK ANALYSIS
def count_real_probability(game_odds):
    odds = {option: odd for option, odd in game_odds.items() if option != "id" and option != "league_name" and option != "commence_time"}
    implied_probs = {option: 1 / float(odd) for option, odd in odds.items()}
    sum_prob = sum(implied_probs.values())
    return {
        option: {
            "match_id": game_odds["id"],
            "outcome_name": option,
            "real_prob": prob / sum_prob, 
            "offered_odd": odds[option],
        }
        for option, prob in implied_probs.items()
    }

def count_ev(bets):
    combined_prob = 1.0
    combined_odd = 1.0
    for bet in bets:
        combined_prob *= bet['real_prob']
        combined_odd *= bet['offered_odd']
    ev = (combined_prob * combined_odd) - 1.0
    return {
        'combined_prob': combined_prob,
        'combined_odd': combined_odd,
        'ev': ev
    }

def count_kellys_criterion(risk, d, games_count, expected_market_margin=0.08):
    ev = (d['combined_prob'] * d['combined_odd']) - 1
    bankroll_percentage = (ev + (expected_market_margin * games_count)) / (d['combined_odd'] - 1)
    return max(risk * bankroll_percentage, 0.0)

def count_individual_ev(game_odds, bet):
    return (game_odds[bet]["offered_odd"] * game_odds[bet]["real_prob"]) - 1

### TICKET FILTERS

def conflicts_filter(types):
    match_ids = [bet["match_id"] for bet in types]
    return len(match_ids) == len(set(match_ids))


def individual_ev_filter(individual_ev):
    from modules import config
    return individual_ev > config.MIN_SINGLE_EV

def odd_filter(bet):
    from modules import config
    max_odd = max(item["offered_odd"] for item in bet)
    min_odd = min(item["offered_odd"] for item in bet)
    return max_odd/min_odd <= config.MAX_ODDS_RATIO


def time_filter(games):
    from datetime import datetime, timedelta, timezone

    now = datetime.now(timezone.utc)
    filtered_games = []

    for game in games:
        commence_time = game["commence_time"]
        if isinstance(commence_time, str):
            commence_time = datetime.fromisoformat(commence_time.replace("Z", "+00:00"))
        if commence_time.tzinfo is None:
            commence_time = commence_time.replace(tzinfo=timezone.utc)

        if now - commence_time < timedelta(hours=2):
            filtered_games.append(game)

    return filtered_games

def league_filter(league, chosen_leagues):
    if not league in chosen_leagues:
        return False
    return True