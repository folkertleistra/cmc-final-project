import pickle

def create():
    print('Creating empty streamer dict')
    streamer_dict = dict()
    with open('streamers_dict.p', 'wb') as fp:
        pickle.dump(streamer_dict, fp, protocol=pickle.HIGHEST_PROTOCOL)

    print('Creatin runtime log')
    with open('runtime_log.txt', 'w') as f:
        f.write('Creation of runtime Log')
