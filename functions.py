import requests
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

def get_puuid_by_riot_id(api_key, game_name, tag_line):
    # URL-encode the game name and tag line
    encoded_game_name = quote(game_name)
    encoded_tag_line = quote(tag_line)
    api_url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{encoded_game_name}/{encoded_tag_line}"
    headers = {"X-Riot-Token": api_key}
    resp = requests.get(api_url, headers=headers)
    print(f"Response Status Code (get_puuid_by_riot_id): {resp.status_code}")
    print(f"Response Content (get_puuid_by_riot_id): {resp.content}")

    if resp.status_code != 200:
        return None, resp.status_code
    
    account_info = resp.json()
    return account_info.get('puuid', 'N/A'), 200

def get_summoner_by_puuid(api_key, puuid):
    api_url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    headers = {"X-Riot-Token": api_key}
    resp = requests.get(api_url, headers=headers)
    print(f"Response Status Code (get_summoner_by_puuid): {resp.status_code}")
    print(f"Response Content (get_summoner_by_puuid): {resp.content}")

    if resp.status_code != 200:
        return None, resp.status_code
    
    summoner_info = resp.json()
    return summoner_info, 200

def get_matches(api_key, puuid):
    # Use the regional routing value for match-v5 endpoint
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    print(f"Response Status Code (get_matches): {response.status_code}")
    print(f"Response Content (get_matches): {response.content}")
    
    if response.status_code != 200:
        return [], response.status_code
    return response.json(), 200

def get_match_data(api_key, match_id):
    # Use the regional routing value for match-v5 endpoint
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    print(f"Response Status Code (get_match_data): {response.status_code}")
    print(f"Response Content (get_match_data): {response.content}")
    
    if response.status_code != 200:
        return {}, response.status_code
    return response.json(), 200

def part_index(match_data, puuid):
    return next((i for i, p in enumerate(match_data['info']['participants']) if p['puuid'] == puuid), None)

def did_win(match_data, part_idx):
    return match_data['info']['participants'][part_idx]['win']

def win_rate(game_no, win_count):
    return (win_count / game_no) * 100 if game_no > 0 else 0

def fetch_data(game_name, tag_line, output_label):
    api_key = os.getenv("API_KEY")

    if api_key is None:
        output_label.config(text="API key not found. Please set the API_KEY environment variable.")
        return

    puuid, status_code = get_puuid_by_riot_id(api_key, game_name, tag_line)
    if status_code != 200 or puuid == 'N/A':
        output_label.config(text=f"Failed to get account info. Status Code: {status_code}")
        return

    summoner_info, status_code = get_summoner_by_puuid(api_key, puuid)
    if status_code != 200 or summoner_info is None:
        output_label.config(text=f"Failed to get summoner info. Status Code: {status_code}")
        return

    matches, status_code = get_matches(api_key, puuid)
    if status_code != 200:
        output_label.config(text=f"Failed to get matches. Status Code: {status_code}")
        return

    if not matches:
        output_label.config(text="No matches found.")
        return

    win_count = 0
    game_no = len(matches)

    for match_id in matches:
        match_data, status_code = get_match_data(api_key, match_id)
        if status_code != 200:
            output_label.config(text=f"Failed to get match data. Status Code: {status_code}")
            return

        if 'metadata' not in match_data:
            output_label.config(text="Metadata not found in match data.")
            return

        part_idx = part_index(match_data, puuid)
        win_status = did_win(match_data, part_idx)
        if win_status:
            win_count += 1

    win_rate_percentage = win_rate(game_no, win_count)

    output_label.config(text=f"\nWin Count: {win_count}\nWin Rate: {win_rate_percentage:.2f}%")
    if win_count <= 7:
        output_label.config(text=f"\nWin Count: {win_count}\nWin Rate: {win_rate_percentage:.2f}%\nYOU SUCK")
