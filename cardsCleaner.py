import pandas as pd
import json

df = pd.read_csv('cards.csv')
#dates hardcoded according to my dataset
xCol = list(df.loc[:, '2024-09-07':'2024-12-07']) + ['uuid','rarity', 'printings']
df[xCol].to_csv('cleanedCards.csv', index=False)
