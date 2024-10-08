import json
import http.client
import os

import dotenv
dotenv.load_dotenv()

api_key = os.getenv("x-rapidapi-key")
api_host = os.getenv("x-rapidapi-host")

conn = http.client.HTTPSConnection(api_host)

headers = {
    'x-rapidapi-key': api_key,
    'x-rapidapi-host': api_host
}

def getPlayerId():

    with open('LakersPlayerData.json', 'r') as file:
        lakersPlayers = json.load(file)

    playerId = []

    if 'body' in lakersPlayers and 'roster' in lakersPlayers['body']:
        playerId = [player['playerId'] for player in lakersPlayers['body']['roster']]
    else:
        playerId = []

    return playerId

# Function to get player data and save as JSON file
def fetchSavePlayerData(headers):    
    playerId = getPlayerId()
    folder_name = 'playerLakers23-24'

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for pid in playerId:
        # Construct the request URL using the playerId

        req_url = f"/players/{pid}/stats/PerGame?seasonType=Regular&seasonId=2023-2024"
        conn.request("GET", req_url, headers=headers)

        # Get the response from the API
        res = conn.getresponse()
        data = res.read()
        decoded_data = data.decode("utf-8")
        json_data = json.loads(decoded_data)

        # Save the response data to a JSON file named after the playerId
        file_name = os.path.join(folder_name, f"{pid}.json")
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        print(f"Data for player {pid} saved to {file_name}")

    # Close the connection after all requests
    conn.close()

fetchSavePlayerData(headers)