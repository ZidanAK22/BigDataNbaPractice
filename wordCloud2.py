import json
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def getPlayerIdAndNames():
    with open('LakersPlayerData.json', 'r') as file:
        lakersPlayers = json.load(file)

    player_dict = {}  # Dictionary to hold player name and player ID

    if 'body' in lakersPlayers and 'roster' in lakersPlayers['body']:
        # Populate the dictionary with player names and their IDs
        player_dict = {player['name']: player['playerId'] for player in lakersPlayers['body']['roster']}
    else:
        player_dict = {}

    return player_dict

def create_wordcloud(player_dict):
    # Dictionary to hold player points per game
    points_dict = {}

    # Iterate through each player name and ID in the dictionary
    for player_name, player_id in player_dict.items():
        # Construct the file name for the player's JSON data
        file_name = f"{player_id}.json"
        
        # Check if the JSON file exists
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                player_data = json.load(file)
                
                # Extract pointsPerGame metric
                points_per_game = float(player_data['body'][0].get('pointsPerGame', 0))
                
                # Add to the dictionary with player name as key
                points_dict[player_name] = points_per_game
        else:
            print(f"File {file_name} does not exist.")

    # Create a word cloud
    if points_dict:  # Check if points_dict is not empty
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(points_dict)

        # Display the word cloud
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')  # Hide the axes
        plt.show()
    else:
        print("No data available to generate a word cloud.")

# Example usage
if __name__ == "__main__":
    player_dict = getPlayerIdAndNames()  # Get a dictionary of player names and IDs
    create_wordcloud(player_dict)  # Create the word cloud based on points per game
