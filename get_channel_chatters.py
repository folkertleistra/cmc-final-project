## This file is used to obtain the active chatters for a streamer

import requests



def chatters_endpoint(channel):
    """
    Function used to obtain the chatters for a twitch stream
    :param channel: twitch streamer channel name
    :return: status code, data
    """
    response = requests.get(f'https://tmi.twitch.tv/group/user/{channel}/chatters')
    if response.status_code == 400:
        return response.status_code, ''

    else:
        return response.status_code, response.json()


