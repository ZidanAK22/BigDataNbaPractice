import json
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def getPlayerIdAndNames():

    with open('LakersPlayerData.json', 'r') as file:
        lakersPlayers = json.load(file)

    playerId = []
    playerNames = []

    if 'body' in lakersPlayers and 'roster' in lakersPlayers['body']:
        playerId = [player['playerId'] for player in lakersPlayers['body']['roster']]
        playerNames = [player['name'] for player in lakersPlayers['body']['roster']]
    else:
        playerId = []

    return playerId, playerNames

def create_wordcloud(player_ids, player_name):
    # Dictionary to hold player points per game
    points_dict = {}

    # Iterate through each player ID
    for player_id in player_ids:
        # Construct the file name for the player's JSON data
        file_name = f"{player_id}.json"
        
        # Check if the JSON file exists
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                player_data = json.load(file)
                
                # Extract pointsPerGame metric
                points_per_game = float(player_data['body'][0].get('pointsPerGame', 0))
                                

                # Add to the dictionary with player ID as key
                points_dict[player_id] = points_per_game
        else:
            print(f"File {file_name} does not exist.")

    # Create a word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(points_dict)

    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # Hide the axes
    plt.show()

# Example usage
if __name__ == "__main__":
    player_ids, player_names = getPlayerIdAndNames()  # Get player IDs from the existing function
    create_wordcloud(player_ids)  # Create the word cloud based on points per game