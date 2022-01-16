## This file is used to obtain the top 100 streams from twitch

import requests
from get_channel_chatters import chatters_endpoint
import pickle
from create_streamers_dict import create
import json
import datetime

def run_scraper():

    currentDT = datetime.datetime.now()
    print(str(currentDT))

    with open('logging/unique_streamers.txt', 'w') as f:
        f.write(str(set(' ')))

    with open('logging/unique_streamers.txt', 'r') as f:
        streamers = eval(f.read())



    ## Adjust this var for less results
    top_n = 100
    #TODO: eerste keer runnen moet streamers_dict.p een lege dict bevatten
    first_run = True
    error_seen = False
    if error_seen:
        # only used for testing
        error = 'Test: can be ignored'

    if first_run:
        create()

    with open('streamers_dict.p', 'rb') as fp:
        #TODO: fututr work store all data into seperate files, this method has potential risks.
        streamer_dict = pickle.load(fp)

    with open('credentials.json') as f:
        credentials = json.load(f)

    headers = {'Authorization': credentials['Authorization'],
              'Client-Id': credentials['Client-Id']}

    params = {'first': str(top_n)}

    response = requests.get('https://api.twitch.tv/helix/streams', headers=headers, params=params)

    if response.status_code != '200':
        response = response.json()
        data = response['data']

        for i, channel in enumerate(data):
            user = channel['user_login']
            print(f'Analyzing streamer: -{user}-  ({i + 1}/{len(data)})')
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
                error_seen = True
                error = f'Obtained Chatters Error: {response.txt}'
                print('Could not retrieve chatters for streamer')

    else:
        error_seen = True
        error = f'Obtained Twitch streams Error: {response.text}'
        print(f'request returned error status: {response.status_code} with message {response.text}')



    with open('logging/unique_streamers.txt', 'w') as f:
        streamers.remove(' ')
        f.write(str(streamers))


    with open('streamers_dict.p', 'wb') as fp:
        pickle.dump(streamer_dict, fp, protocol=pickle.HIGHEST_PROTOCOL)

    with open('logging/runtime_log.txt', 'a') as f:
        f.write(f'\nCompleted runtime at {currentDT} \n')
        if error_seen:
            f.write(f'Encountered error: {error} \n')
        else:
            f.write('No error Encountered \n')
        f.write('-' * 100)


