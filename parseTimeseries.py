import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder

from darts.timeseries import TimeSeries
from darts.utils.missing_values import fill_missing_values
import pickle


df = pd.read_csv("finalDataset.csv")
xCol = list(df.loc[:, '2024-09-07':'2024-12-07'])

df = df[df[xCol].min(axis=1) > 5]
df = df[df[xCol].max(axis=1) < 200]
df['printings'] = df['printings'].apply(lambda x: len(x.split(',')))
rarity_mapping = {
    'common': 1,
    'uncommon': 2,
    'rare': 3,
    'mythic': 4
}
df['rarity'] = df['rarity'].map(rarity_mapping)
df['rarity'] = df['rarity'].fillna(1)
df.set_index('uuid', inplace=True)

modified_df = df[xCol]
modified_df = modified_df.transpose()
modified_df.index = pd.to_datetime(modified_df.index)
modified_df.dropna(axis=1, how='any', inplace=True)
modified_df.reset_index(names='time', inplace=True)
#Reshaping new dataframe for TimeSeries
df_long = modified_df.melt(
    id_vars="time",          # Keep the time column as-is
    var_name="group",        # Name for the new group column (card names)
    value_name="value"       # Name for the new value column (prices)
)

staticCol = ['rarity', 'printings']

df_long = pd.merge(df_long, df[staticCol], how='left', left_on='group',
                   right_index=True)

df_long['group'] = LabelEncoder().fit_transform(df_long['group'])
print(df_long.head())
print(df_long.isnull().values.any())

series_list = TimeSeries.from_group_dataframe(df=df_long, time_col='time',
                                              static_cols=staticCol,
                                          group_cols='group', value_cols='value',
                                         fill_missing_dates=True, freq=None,  n_jobs=-1)

#final check
series_list = [fill_missing_values(series) for series in series_list]

with open("pruned_five_timeseries_list_static.pkl", "wb") as file:
    pickle.dump(series_list, file)
