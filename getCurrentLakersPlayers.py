import json
import http.client
import os
import dotenv

dotenv.load_dotenv()

# get api key from rapidapi.com
# and subscribe to https://rapidapi.com/kdb-sports-kdb-sports-default/api/basketball-head
api_key = os.getenv("x-rapidapi-key")
api_host = os.getenv("x-rapidapi-host")

conn = http.client.HTTPSConnection(api_host)

headers = {
    'x-rapidapi-key': api_key,
    'x-rapidapi-host': api_host
}

# Make a request to get the Lakers roster
try:
    conn.request("GET", "/teams/LAL/roster/2023-2024", headers=headers)
    res = conn.getresponse()
        
    data = res.read()    
    decoded_data = data.decode("utf-8")    
    json_data = json.loads(decoded_data)       
        
    with open('LakersPlayerData.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
        
    print("Data saved to 'LakersPlayerData.json' successfully.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    conn.close()