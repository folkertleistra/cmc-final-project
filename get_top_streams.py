## This file is used to obtain the top 100 streams from twitch

import requests
from get_channel_chatters import chatters_endpoint
import pickle

## Adjust this var for less results
top_n = 5

with open('unique_streamers.txt', 'w') as f:
    f.write(str(set(' ')))

with open('unique_streamers.txt', 'r') as f:
    streamers = eval(f.read())

with open('streamers_dict.p', 'rb') as fp:
    streamer_dict = pickle.load(fp)

headers = {'Authorization': 'Bearer p43f4krhtrvh7w68wg2oecrty5t6jw',
          'Client-Id': 'r302hx3wf9a3fj481d3qqq47fik7g4'}

params = {'first': str(top_n)}

response = requests.get('https://api.twitch.tv/helix/streams', headers=headers, params=params)

if response.status_code != '200':
    response = response.json()
    data = response['data']

    for i, channel in enumerate(data):
        print(f'Analyzing streamer {i + 1} of total {len(data)}')
        user = channel['user_login']
        game_set, language_set = set(), set()
        game = channel['game_name']
        language = channel['language']
        game_set.add(game)
        language_set.add(language)

        print('Extracting chatters')
        chatters_response, chatters_data = chatters_endpoint(user)

        if chatters_response == 200:
            print('Valid response, storing gephi data')
            streamers.add(user)
            viewers = chatters_data['chatters']['viewers']
            viewers = set(viewers)
            # In case it is not the first time we find this streamer
            if user in streamer_dict:
                streamer_dict[user]['languages'].add(language)
                streamer_dict[user]['games'].add(game)
                streamer_dict[user]['viewers'] = streamer_dict[user]['viewers'].union(viewers)

            else:
                streamer_dict[user] = {
                    'languages': language_set,
                    'games': game_set,
                    'viewers': set(viewers)
                }

        else:
            print('Could not retrieve chatters for streamer')

else:
    print(f'request returned error status: {response.status_code} with message {response.text}')


with open('unique_streamers.txt', 'w') as f:
    streamers.remove(' ')
    f.write(str(streamers))


with open('streamers_dict.p', 'wb') as fp:
    pickle.dump(streamer_dict, fp, protocol=pickle.HIGHEST_PROTOCOL)

