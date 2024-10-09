import json
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image
from wordcloud import WordCloud

def getPlayerIdAndNames():
    with open('LakersPlayerData.json', 'r') as file:
        lakersPlayers = json.load(file)

    player_dict = {}

    if 'body' in lakersPlayers and 'roster' in lakersPlayers['body']:
        # Populate the dictionary with player names and their IDs
        player_dict = {player['name']: player['playerId'] for player in lakersPlayers['body']['roster']}
    else:
        player_dict = {}

    return player_dict

def create_wordcloud_and_pie_chart(player_dict, metric):
    metric_dict = {}

    mask = np.array(Image.open('lakers.png'))

    # Iterate through each player name and ID in the dictionary
    for player_name, player_id in player_dict.items():        
        folder = 'playerLakers23-24'
        file_name = os.path.join(folder, f"{player_id}.json")
                
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                player_data = json.load(file)
                
                # Extract the requested metric
                metric_value = float(player_data['body'][0].get(metric, 0))
                
                # Add to the dictionary with player name as key
                metric_dict[player_name] = metric_value
        else:
            print(f"File {file_name} does not exist.")

    

    # Create a word cloud
    if metric_dict:
                
        df = pd.DataFrame(list(metric_dict.items()), columns=['PlayerName', metric])
        
        # Ensure the directory exists before saving
        save_dir = os.path.join('playerLakers23-24', 'metrics')
        os.makedirs(save_dir, exist_ok=True)  # Create the directory if it doesn't exist

        # Save the DataFrame to a CSV file named after the metric
        df.to_csv(os.path.join(save_dir, f"{metric}.csv"), index=False)  # Use os.path.join for compatibility
        print(f"DataFrame for {metric} saved as {metric}.csv")

        wordcloud = WordCloud(width=800, height=400, background_color='white', mask=mask, contour_color='gold', contour_width=1).generate_from_frequencies(metric_dict)

        # Display the word cloud
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'Word Cloud for {metric}')
        plt.show()

        # Prepare data for pie chart
        labels = list(metric_dict.keys())
        sizes = list(metric_dict.values())

        # Create a larger pie chart
        plt.figure(figsize=(12, 8))  # Increased size
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title(f'{metric} Distribution')
        plt.show()
    else:
        print("No data available to generate a word cloud or pie chart.")

# Example usage
if __name__ == "__main__":
    player_dict = getPlayerIdAndNames()
    
    metrics = ['pointsPerGame', 'assistsPerGame', 'totalReboundsPerGame', 'stealsPerGame', 'blocksPerGame']

    for metric in metrics:
        create_wordcloud_and_pie_chart(player_dict, metric)
