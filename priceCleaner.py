import pandas as pd
import json

with open('AllPrices.json', 'r') as file:
    # Read the entire file
    file_content = json.load(file)

data_objects = file_content.get('data')


def process_in_chunks(data):
    dfs = []
    cardsUUID = []
    for card, card_data in data.items():
        if ("paper" in card_data and
            "tcgplayer" in card_data["paper"] and
            "retail" in card_data["paper"]["tcgplayer"] and
           "normal" in card_data["paper"]["tcgplayer"]["retail"]):
            dfs.append(card_data["paper"]["tcgplayer"]["retail"]["normal"])
            cardsUUID.append(card)
    final_df = pd.json_normalize(dfs)
    final_df.insert(0, 'uuid', cardsUUID)
    return final_df

df = process_in_chunks(data_objects)
df.to_csv('cleanedPriceHistory.csv', index=False)
