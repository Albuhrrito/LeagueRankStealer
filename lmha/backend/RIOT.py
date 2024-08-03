from functions import get_summoner_puuid, get_matches, get_match_data, part_index, did_win, win_rate, fetch_player_info
import os
from dotenv import load_dotenv
import requests

# FLASK
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory(os.path.abspath(os.path.dirname(__file__)), 'index.html')

def format_match_info(api_key, region, match_id, puuid):
    match_data = get_match_data(api_key, region, match_id)
    part_idx = part_index(match_data, puuid)
    win_status = did_win(match_data, part_idx)
    kda = {
        "kills": match_data['info']['participants'][part_idx]['kills'],
        "deaths": match_data['info']['participants'][part_idx]['deaths'],
        "assists": match_data['info']['participants'][part_idx]['assists']
    }
    return {
        "match_id": match_id,
        "part_idx": part_idx,
        "KDA": kda,
        "did_win": win_status
    }

@app.route('/fetch_player_info', methods=['GET'])
def fetch_player_info_route():
    name = request.args.get('name')
    tag = request.args.get('tag')
    
    if not name or not tag:
        return jsonify({'success': False, 'error': 'Missing name or tag'}), 400
    
    try:
        puuid = fetch_player_info(name, tag)
        if puuid == 'N/A':
            return jsonify({'success': False, 'error': 'Player not found'}), 404
        
        api_key = os.getenv("API_KEY")
        region = 'americas'  # Adjust region as needed
        match_ids = get_matches(api_key, region, puuid)
        
        if match_ids is None:
            return jsonify({'success': False, 'error': 'Failed to retrieve matches'}), 500
        
        # Collect detailed match information
        matches = []
        win_count = 0
        game_no = 0
        
        for match_id in match_ids:
            match_info = format_match_info(api_key, region, match_id, puuid)
            matches.append(match_info)
            if match_info["did_win"]:
                win_count += 1
            game_no += 1
        
        win_rate_percentage = win_rate(game_no, win_count)
        
        return jsonify({
            'success': True, 
            'data': matches, 
            'win_count': win_count, 
            'win_rate': win_rate_percentage
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

#GUI CODE##############
# root = tk.Tk()
# root.title("Riot API GUI")

# username_label = ttk.Label(root, text="Enter username:")
# username_label.pack(pady=10)

# username_entry = ttk.Entry(root, width=30)
# username_entry.pack(pady=5)

# fetch_button = ttk.Button(root, text="Fetch Data", command=did_win)
# fetch_button.pack(pady=10)

# output_label = ttk.Label(root, text="")
# output_label.pack(pady=10)

# root.mainloop()
load_dotenv()
SUMMONER_NAME = input("Enter username: ")
SUMMONER_TAG = input("Enter tagline: ")
region = "americas"
api_key = os.getenv("API_KEY")

if api_key is None:
    print("API key not found. Please set the API_KEY environment variable.")
    exit()


api_url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{SUMMONER_NAME}/{SUMMONER_TAG}?api_key={api_key}"
#api_url = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/albruh/VAL?api_key=RGAPI-7d859125-0bb1-4daa-b08b-3bea04c39a06'
resp = requests.get(api_url)

if resp.status_code != 200:
    print(f"Failed to get player info. Status Code: {resp.status_code}")
    exit()
    
player_info = resp.json()
player_account_id = player_info.get('accountId', 'N/A')
puuid = resp.json().get('puuid', 'N/A')
print("PUUID for " + str(SUMMONER_NAME) + "#" + str(SUMMONER_TAG) + ": " + str(puuid))

matches = get_matches(api_key, region, puuid)
match_id = matches[0]

match_data = get_match_data(api_key, region, match_id)
if 'metadata' not in match_data:
    print("metadata not found in match_data")
    exit()

part_idx = part_index(match_data, puuid)
win_status = did_win(match_data, part_idx)

matches = get_matches(api_key, region, puuid)

game_no = 0
win_count = 0

for match_id in matches:
    match_data = get_match_data(api_key, region, match_id)
    part_idx = part_index(match_data, puuid)
    win_status = did_win(match_data, part_idx)
    print("game number = " + str(game_no + 1))
    print(f"Part Index: {part_idx}")
    print("KDA = " + str((match_data['info']['participants'][part_idx]['kills'], 
                          match_data['info']['participants'][part_idx]['deaths'], 
                          match_data['info']['participants'][part_idx]['assists'])))
    print(f"Did Win: {win_status}")
    print(match_id)
    print("")
    if win_status:
        win_count += 1
    game_no += 1
print("Win Count: " + str(win_count))
print("Win Rate: " + str(win_rate(game_no, win_count)))
if win_count <= 7:
    print("YOU SUCK")


