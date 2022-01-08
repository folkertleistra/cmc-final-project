## This file is used to compare the viewers of each streamer.
import pandas as pd
import pickle
import itertools
sources, targets, games, languages = [], [], [], []



with open('streamers_dict.p', 'rb') as fp:
    data = pickle.load(fp)

users = list(data.keys())
print(users)
for a, b in itertools.combinations(users, 2):
    print(len(data[a]['viewers'].intersection(data[b]['viewers'])))

# sources.extend(viewers)
# targets.extend([user] * len(viewers))
# games.extend([game] * len(viewers))
# languages.extend([language] * len(viewers))


# final dataset creation
df_data = {'Source': sources,
           'Target': targets,
           'Game': games,
           'Language': languages}

df = pd.DataFrame.from_records(df_data, columns=['Source', 'Target', 'Game', 'Language'])
df.to_csv('twitch-gephi-data.csv', index=False)