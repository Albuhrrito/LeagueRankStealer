from flask import Flask, jsonify, request
import sys
from functions import fetch_player_info

app = Flask(__name__)

@app.route('/get_match_history')
def get_match_history():
    summoner_name = request.args.get('name')
    summoner_tag = request.args.get('tag')
    puuid = fetch_player_info(summoner_name, summoner_tag)
    
    if puuid:
        # Further processing, assuming other functions handle match retrieval etc.
        return jsonify({'success': True, 'data': 'Data for ' + summoner_name})
    else:
        return jsonify({'success': False, 'error': 'Failed to retrieve player info'})

if __name__ == '__main__':
    app.run(debug=True)
