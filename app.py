import aiohttp
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from queries import odds_api_query as q
from database import db_config as dbc
from modules import config
from modules import ticket_creator as tc

app = Flask(__name__, template_folder='static/html', static_folder='static/assets')
CORS(app)

@app.route('/', methods=['GET'])
async def index():
    return render_template('index.html')


@app.route('/generate', methods=['GET', 'POST'])
async def create_ticket():
    if not request.is_json:
        return jsonify({'error': 'Request must contain JSON'}), 415
    data = request.get_json(silent=True) or {}
    try:
        risk = data.get('risk')
        target_ako = data.get('targetAKO')
        games = data.get('games')
        leagues = data.get('leagues')
        mapped_leagues = []
        for league in leagues:
            mapped_leagues.append(config.LEAGUES_MAP[league])
        
        db_name = dbc.create_db()
        if db_name is None:
            raise RuntimeError("Could not create or connect to the bet-builder database")
        dbc.create_tables(db_name)
        odds = await q.get_odds()
        if odds is not None:
            q.send_query_data_to_db(odds)
        ticket = tc.generate_ticket(risk, target_ako, games, mapped_leagues)
        if ticket is None:
            return jsonify({'error': 'No valid ticket found for the selected parameters'}), 400
        return jsonify(ticket), 200
    except Exception:
        app.logger.exception("Ticket generation failed")
        return jsonify({'error': 'Something went wrong'}), 500


    
if __name__ == "__main__":
    app.run(debug=True)
    
