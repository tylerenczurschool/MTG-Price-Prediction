import pandas as pd
import json

def parseEdhrecJson(file_path):
    with open(file_path, 'r') as file:
        file_content = json.load(file)
    data_objects = file_content['cardviews']
    df = pd.json_normalize(data_objects)
    return df[['name', 'num_decks', 'potential_decks']]

dfs = []
for i in range(1, 100):
    dfs.append(parseEdhrecJson(f'edhrecDump/year-past2years-{i}.json'))
for i in range(1, 10):
    dfs.append(parseEdhrecJson(f'edhrecDump/lands-toplands(past2years)-{i}.json'))

with open('edhrecDump/year-past2years-0.json', 'r') as file:
    file_content = json.load(file)
first_object = file_content['container']['json_dict']['cardlists'][0]['cardviews']
dfs.append((pd.json_normalize(first_object))[['name', 'num_decks', 'potential_decks']])

with open('edhrecDump/lands-toplands(past2years)-0.json', 'r') as file:
    file_content = json.load(file)
first_object = file_content['container']['json_dict']['cardlists'][0]['cardviews']
dfs.append((pd.json_normalize(first_object))[['name', 'num_decks', 'potential_decks']])

df = pd.concat(dfs, ignore_index=True)

df['Percent'] = (100 * df['num_decks'] / df['potential_decks']).astype(int)
df.sort_values(by='Percent', ascending=False, inplace=True)

df.to_csv('edhrecCleaned.csv', index=False)

