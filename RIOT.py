import tkinter as tk
from tkinter import ttk
from functions import get_summoner_puuid, get_matches, get_match_data, part_index, did_win, win_rate, fetch_data
import os
from dotenv import load_dotenv
import requests

load_dotenv()

#GUI CODE##############
root = tk.Tk()
root.title("Riot API GUI")

username_label = ttk.Label(root, text="Enter username:")
username_label.pack(pady=10)

username_entry = ttk.Entry(root, width=30)
username_entry.pack(pady=5)

fetch_button = ttk.Button(root, text="Fetch Data", command=did_win)
fetch_button.pack(pady=10)

output_label = ttk.Label(root, text="")
output_label.pack(pady=10)

root.mainloop()

SUMMONER_NAME = input("Enter username: ")
region = "americas"
api_key = os.getenv("API_KEY")

if api_key is None:
    print("API key not found. Please set the API_KEY environment variable.")
    exit()

api_url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{SUMMONER_NAME}"
api_url = api_url + '?api_key=' + api_key
resp = requests.get(api_url)

if resp.status_code != 200:
    print(f"Failed to get player info. Status Code: {resp.status_code}")
    exit()
    
player_info = resp.json()
player_account_id = player_info.get('accountId', 'N/A')
puuid = resp.json().get('puuid', 'N/A')
print("PUUID for " + str(SUMMONER_NAME) + ": " + str(puuid))

matches = get_matches(api_key, region, puuid)
match_id = matches[0]

match_data = get_match_data(api_key, region, match_id)
if 'metadata' not in match_data:
    print("metadata not found in match_data")
    exit()

part_idx = part_index(match_data, puuid)
win_status = did_win(match_data, part_idx)

matches = get_matches(api_key, region, puuid)

game_no = 1
win_count = 0

for match_id in matches:
    match_data = get_match_data(api_key, region, match_id)
    part_idx = part_index(match_data, puuid)
    win_status = did_win(match_data, part_idx)
    print("game number = " + str(game_no))
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


