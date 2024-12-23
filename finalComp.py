import pandas as pd
import json

df1 = pd.read_csv('cleanedCards.csv')
df2 = pd.read_csv('edhrecCleaned.csv')
df3 = pd.read_csv('cleanedPriceHistory.csv')
result = pd.merge(df1, df2, on='name', how='left')
result = pd.merge(result, df3, on='uuid', how='inner')
result.set_index('uuid', inplace=True)
result.to_csv('finalDataset.csv', index=True)
