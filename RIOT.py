import requests
import os
import time

from dotenv import load_dotenv
#import dearpygui.dearpygui as dpg
#VARIABLE DECLARATIONS
#//////////
load_dotenv()
SUMMONER_NAME = "zakiVAL"
region = "americas"
api_key = os.getenv("API_KEY")
if api_key is None:
    print("API key not found. Please set the API_KEY environment variable.")
    exit()
puuid = "PnnfqQB40RSFSkzpl7Cv53eadUTwsMMK-RYeQXztDNTPExwzkgCmrdJ7znM2QqD6tIdmp0a0p47p2g"
api_url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/zakiVAL"
api_url = api_url + '?api_key=' + api_key
resp = requests.get(api_url)
player_info = resp.json()
player_account_id = player_info['accountId']
api_url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/PnnfqQB40RSFSkzpl7Cv53eadUTwsMMK-RYeQXztDNTPExwzkgCmrdJ7znM2QqD6tIdmp0a0p47p2g/ids?start=0&count=20"
api_url = api_url + "&api_key=" + api_key
resp = requests.get(api_url)
matches = resp.json()
match_id = matches[0]
#print(match_id)
api_url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/PnnfqQB40RSFSkzpl7Cv53eadUTwsMMK-RYeQXztDNTPExwzkgCmrdJ7znM2QqD6tIdmp0a0p47p2g/ids?type=ranked&start=0&count=1"
api_url = "https://americas.api.riotgames.com/lol/match/v5/matches/" + match_id
api_url = api_url + "?api_key=" + api_key
resp = requests.get(api_url)
match_data = resp.json()
#print(match_data)
match_data.keys()
part_index = match_data['metadata']['participants'].index(puuid)
puuid = "PnnfqQB40RSFSkzpl7Cv53eadUTwsMMK-RYeQXztDNTPExwzkgCmrdJ7znM2QqD6tIdmp0a0p47p2g"
#print(match_data['info']['participants'][part_index]['kills'], match_data['info']['participants'][part_index]['deaths'], match_data['info']['participants'][part_index]['assists'])
kdaRatio = (match_data['info']['participants'][part_index]['kills'] + match_data['info']['participants'][part_index]['assists']) / match_data['info']['participants'][part_index]['deaths']
kdaRatioText = "KDA RATIO = " + str(kdaRatio)
#/////////////////
#GUI CODE
#/////////////////
'''
dpg.create_context()
dpg.create_viewport(title='KDA', width=600, height=300)

with dpg.window(label="KDA"):
    dpg.add_text(match_data['info']['participants'][part_index]['kills'])
    dpg.add_text(match_data['info']['participants'][part_index]['deaths'])
    dpg.add_text(match_data['info']['participants'][part_index]['assists'])
    dpg.add_text(kdaRatioText)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
'''
#/////////////////
#FUNCTIONS
#/////////////////
def getMatchData(region, match_data, api_key):
    api_url = ("https://" + 
               region + 
               ".api.riotgames.com/lol/match/v5/matches/" + 
               match_id + "?api_key=" + 
               api_key)
    while True:
        resp = requests.get(api_url)
        if resp.status_code == 429:
            print("sleeping")
            time.sleep(10)
            continue
        data = resp.json()
        return data
match_data = getMatchData(region, match_id, api_key)
getMatchData(region, match_data, api_key)

print(part_index)
def partIndex(match_data):
    return match_data['metadata']['participants'].index(puuid)

def didWin(puuid, match_data):
    match_data = getMatchData(region, match_id, api_key)
    return match_data['info']['participants'][part_index]['win']

def get_summoner_account_id(summoner_name):
    url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}"
    response = requests.get(url)
    data = response.json()
    return data['accountId']

def calculate_win_rate(count):
    win_rate = "%" + str((count/20) * 100)
    print("You have a " + str(win_rate) + " win rate.")
    if(count <= 5):
        print("You are DOGSHIT")

account_id = get_summoner_account_id(SUMMONER_NAME)
count = 0

def get_match_history(puuid):
    url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=10&api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
game_no = 1
count = 0
for match_id in matches:
    match_data = getMatchData(region, match_id, api_key)
    part_index = partIndex(match_data)
    print("game number = " + str(game_no))
    print("part index = " + str(part_index))
    print("KDA = " + str((match_data['info']['participants'][part_index]['kills'], match_data['info']['participants'][part_index]['deaths'], match_data['info']['participants'][part_index]['assists'])))
    print(didWin(puuid, match_data))
    print(match_id)
    print("")
    if(didWin(puuid, match_data) == True):
        count += 1
    game_no += 1
        

get_match_history(puuid)
calculate_win_rate(count)


#////////////////
'''
def get_match_history(account_id, count=20):
    url = "https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?endIndex={count}&api_key={api_key}"
    response = requests.get(url)
    data = response.json()
    return data['match_id']
get_match_history(account_id, count=20)


def get_matches(region, puuid, count, api_key):
    api_url=(
        "https://" +
        region +
        ".api.riotgames.com/lol/match/v5/matches/by-puuid/" +
        puuid +
        "/ids" +
        "?type=ranked&" +
        "start=0&" +
        "count=" + 
        str(count) +
        "&api_key=" +
        api_key
    )
    resp = requests.get(api_url)
    return resp.json()
matches = get_matches(region, puuid, 110, api_key)


match_data['info']['participants'][0]['win']
player_info['puuid']
didWin(puuid, match_data)

getMatchData(region, match_data, api_key)

'''
