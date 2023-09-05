import requests
import time

def get_summoner_puuid(api_key, username, region):
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("puuid")
    else:
        return f"An error occurred: {response.status_code}"

def get_matches(api_key, region, puuid, count=20):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    headers = {"X-Riot-Token": api_key}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print("Rate limited. Please wait before trying again.")
        elif response.status_code == 403:
            print("API key invalid or expired.")
        elif response.status_code == 404:
            print("Data not found.")
        else:
            print(f"An error occurred: {response.status_code}")
        return None
    except Exception as e:
        print(f"An exception occurred: {e}")
        return None

def get_match_data(api_key, region, match_id):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": api_key}
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 429:
            print("sleeping")
            time.sleep(10)
            continue
        return response.json()

def part_index(match_data, puuid):
    return match_data['metadata']['participants'].index(puuid)

def did_win(match_data, part_index):
    return match_data['info']['participants'][part_index]['win']

def win_rate(game_no, win_count):
    if(game_no == 100):
        return str(win_count) + "%"
    else:
        return str(win_count/game_no * 100) + "%"

def fetch_data():
    return 