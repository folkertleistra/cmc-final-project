## This file is used to compare the viewers of each streamer.
import pandas as pd
import pickle
import itertools

sources, targets, weights = [], [], []
nodes_to_check = set()

with open('data/streamers_dict.p', 'rb') as fp:
    data = pickle.load(fp)

users = list(data.keys())
print(f'Found {len(users)} twitch streamers')

skipped = 0
for streamer1, streamer2 in itertools.combinations(users, 2):
    intersect = data[streamer1]['viewers'].intersection(data[streamer2]['viewers'])
    weight = len(intersect)

    if len(intersect) >= 500:
        nodes_to_check.add(streamer1)
        nodes_to_check.add(streamer2)

        sources.append(streamer1)
        targets.append(streamer2)
        weights.append(weight)

    else:
        skipped += 1

print(f'Done set intersections, {skipped} instances skipped of total {len(users)}')
print('Creating Nodes and Edges lists')

# Creation of edges list
df_data_weights = {'Source': sources,
                   'Target': targets,
                   'Weight': weights}

df_weights = pd.DataFrame.from_records(df_data_weights, columns=['Source', 'Target', 'Weight'])
df_weights.to_csv('data/twitch-gephi-data_edges_list.csv', index=False)

# Creation of nodes list
nodes_to_check = list(nodes_to_check)
languages, games, node_counts = [], [], []

for streamer in nodes_to_check:
    node_counts.append(len(data[streamer]['viewers']))
    lan = list(data[streamer]['languages'])
    lan.sort()
    languages.append(lan)
    game = list(data[streamer]['games'])
    game.sort()
    games.append(game)

df_data_nodes = {'Id': nodes_to_check,
                 'Label': nodes_to_check,
                 'Count': node_counts,
                 'Languages': languages,
                 'Games': games}

df_nodes = pd.DataFrame.from_records(df_data_nodes, columns=['Id', 'Label', 'Count', 'Languages', 'Games'])
df_nodes.to_csv('data/twitch-gephi-data-nodes_list.csv', index=False)
