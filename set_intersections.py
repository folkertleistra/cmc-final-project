## This file is used to compare the viewers of each streamer.
import pandas as pd
import pickle
import itertools
from collections import defaultdict
import sys

new_sources, new_targets, weights = [], [], []
nodes_to_check = set()

filtered_data = defaultdict(set)

with open('data/streamers_dict.p', 'rb') as fp:
    data = pickle.load(fp)

users = list(data.keys())
print(f'Found {len(users)} twitch streamers')
skipped = 0
for streamer1, streamer2 in itertools.combinations(users, 2):
    # als deze lengte groter is dan 300: behoud de viewers van beide streamers -> houd alleen deze chatters voor de streamers
    intersect = data[streamer1]['viewers'].intersection(data[streamer2]['viewers'])
    weight = len(intersect)

    if len(intersect) >= 500:
        print('found intersection larger than 300')
        # Id -> streamers
        # Label -> streamers
        # count -> unique viewers
        nodes_to_check.add(streamer1)
        nodes_to_check.add(streamer2)

        filtered_data[streamer1] = filtered_data[streamer1].union(intersect)
        filtered_data[streamer2] = filtered_data[streamer2].union(intersect)

        new_sources.append(streamer1)
        new_targets.append(streamer2)
        weights.append(weight)
        #break
    else:
        skipped += 1
        print('Skipping')

print(f'Done set intersections, {skipped} instances skipped of total {len(users)}')
print('Creating Dataframe')
#print(filtered_data)

sources = [chatter for value in filtered_data.values() for chatter in value]

#targets = [[key] * len(sources) for key, value in filtered_data.items()]
targets = []
for key, value in filtered_data.items():
    targets.extend([key] * len(value))
print(len(sources), len(targets))
#sys.exit(0)
# final dataset creation
df_data = {'Source': sources,
           'Target': targets
           }

df_data_weights = {'Source': new_sources,
                   'Target': new_targets,
                   'Weight': weights}

ids_and_labels = [streamer for streamer in nodes_to_check]
node_counts = [len(data[streamer]['viewers']) for streamer in nodes_to_check]
df_data_nodes = {'Id': ids_and_labels,
                 'Label': ids_and_labels,
                 'Count': node_counts}

df = pd.DataFrame.from_records(df_data, columns=['Source', 'Target'])
df.to_csv('data/twitch-gephi-data_1000.csv', index=False)

df_weights = pd.DataFrame.from_records(df_data_weights, columns=['Source', 'Target', 'Weight'])
df_weights.to_csv('data/twitch-gephi-data_edges_list.csv', index=False)

df_nodes = pd.DataFrame.from_records(df_data_nodes, columns=['Id', 'Label', 'Count'])
df_nodes.to_csv('data/twitch-gephi-data-nodes_list.csv', index=False)
